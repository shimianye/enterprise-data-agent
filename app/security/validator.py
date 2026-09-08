"""
SQL 安全校验模块（SQLite 版）
============================

设计参考：fengyede79/text-to-sql-agent-system (MIT License) 的
`app/agent/sql_safety_types.py`。本模块为针对本项目 10 张经营分析表的
精简与 SQLite 方言适配版本。

保留的核心设计（6 项）：
  1. 注释词法分析（手写状态机，正确跳过单/双/反引号内的注释标记）
  2. 多语句拦截（任何 DBMS 都不应让 LLM 生成多语句执行）
  3. 只读 SQL 限制（仅允许 SELECT、WITH(CTE) 与集合运算 UNION/INTERSECT/EXCEPT）
  4. CTE/子查询作用域（虚拟表名与物理表分离校验）
  5. 投影别名识别（ORDER BY 引用 SELECT 别名合法）
  6. 歧义列检测（同名字段多表存在时强制要求限定）

针对本项目的额外能力：
  7. SELECT * 拦截
  8. LIMIT 注入与钳制

相比原项目差异：
  - 方言默认 `sqlite`（保留 `mysql` 切换能力）
  - 函数签名增加 `dialect` 参数
  - 异常类 `SQLValidationError` 暴露 violations，便于上层构造友好错误

用法：
    from app.security.validator import check_sql_safety, SQLValidationError

    schema = [
        {"name": "orders", "columns": [{"name": "order_id"}, ...]},
        ...
    ]
    result = check_sql_safety("SELECT paid_amount FROM orders", table_infos=schema)
    if not result.is_safe:
        raise SQLValidationError(result.violations)
    cursor.execute(result.normalized_sql)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import sqlglot
from sqlglot import exp


# ============================================================
# 公开类型与异常
# ============================================================
@dataclass
class SQLSafetyResult:
    """SQL 安全校验结果。

    Attributes:
        is_safe: 是否通过校验
        normalized_sql: 规范化后的 SQL（已注入 LIMIT 等）
        violations: 违规项列表（如 `unknown_table:users`、`select_star_not_allowed`）
        warnings: 警告项列表（如 `limit_injected`、`limit_clamped`）
        rewritten: 是否对 SQL 做了改写（注入 LIMIT 算改写）
        safety_summary: 简要状态描述，便于日志与调试
    """

    is_safe: bool
    normalized_sql: str
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rewritten: bool = False
    safety_summary: str = ""

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"SQLSafetyResult(safe={self.is_safe}, "
            f"summary={self.safety_summary!r}, "
            f"violations={self.violations})"
        )


class SQLValidationError(Exception):
    """SQL 校验失败异常。包含 violations 列表，便于上层构造友好错误消息。"""

    def __init__(self, violations: list[str]):
        self.violations = violations
        super().__init__(f"SQL validation failed: {', '.join(violations)}")


# ============================================================
# 内部辅助
# ============================================================
def _fail(
    sql: str,
    violations: list[str],
    warnings: list[str] | None = None,
) -> SQLSafetyResult:
    return SQLSafetyResult(
        is_safe=False,
        normalized_sql=sql,
        violations=violations,
        warnings=warnings or [],
        rewritten=False,
        safety_summary="safety_failed",
    )


def _allowed_schema(table_infos: list[dict[str, Any]]) -> dict[str, set[str]]:
    """从 `table_infos` 构造 `{table_name: {column_name}}` 映射。"""
    return {
        table["name"]: {column["name"] for column in table.get("columns", [])}
        for table in table_infos
    }


# ============================================================
# 1. 注释词法分析（独立函数，测试可直接覆盖）
# ============================================================
def _has_comment_markers_outside_literals(sql: str) -> bool:
    """检测 SQL 文本中是否有位于字符串字面量外的注释标记（`--`、`/*`、`#`）。

    状态机遍历：跟踪单/双引号、反引号三种"在字符串内"状态，仅当字符在
    字面量外时检测注释标记。这是 OWASP LLM Top 10 "Excessive Agency" 防护
    的核心细节——若不区分字面量，攻击者可构造 `' OR 1=1 --` 形式的注入。
    """
    in_single = False
    in_double = False
    in_backtick = False
    i = 0
    n = len(sql)
    while i < n:
        char = sql[i]
        next_char = sql[i + 1] if i + 1 < n else ""

        # 单引号字符串
        if in_single:
            if char == "'" and next_char == "'":  # SQL 标准转义：两个单引号
                i += 2
                continue
            if char == "'":
                in_single = False
            i += 1
            continue

        # 双引号字符串（SQLite 中用于标识符，但这里也按字面量处理）
        if in_double:
            if char == '"' and next_char == '"':  # SQL 标准转义：两个双引号
                i += 2
                continue
            if char == '"':
                in_double = False
            i += 1
            continue

        # 反引号（MySQL 标识符，SQLite 也支持）
        if in_backtick:
            if char == "`":
                in_backtick = False
            i += 1
            continue

        # 字面量外
        if char == "'":
            in_single = True
        elif char == '"':
            in_double = True
        elif char == "`":
            in_backtick = True
        elif (
            sql.startswith("--", i)
            or sql.startswith("/*", i)
            or sql.startswith("*/", i)
            or char == "#"
        ):
            return True
        i += 1

    return False


# ============================================================
# 2. CTE / 子查询作用域
# ============================================================
def _virtual_table_names(expression: exp.Expression) -> set[str]:
    """收集 CTE 与子查询的别名（虚拟表名）。这些不是真实物理表。"""
    names: set[str] = set()
    for cte in expression.find_all(exp.CTE):
        alias_node = cte.args.get("alias")
        if alias_node:
            names.add(alias_node.name)
    for sub in expression.find_all(exp.Subquery):
        alias_node = sub.args.get("alias")
        if alias_node:
            names.add(alias_node.name)
    return names


def _inner_scope_column_ids(expression: exp.Expression) -> set[int]:
    """返回位于 CTE 或子查询体内的 Column 节点 id 集合。

    这些列属于内层作用域，校验时按规则特殊处理（内层列不应以外层 schema 校验）。
    """
    ids: set[int] = set()
    for cte in expression.find_all(exp.CTE):
        for col in cte.find_all(exp.Column):
            ids.add(id(col))
    for sub in expression.find_all(exp.Subquery):
        for col in sub.find_all(exp.Column):
            ids.add(id(col))
    return ids


# ============================================================
# 3. 投影别名
# ============================================================
def _projection_aliases(expression: exp.Expression) -> set[str]:
    """收集外层 SELECT 投影列表的显式别名。

    例：`SELECT SUM(paid_amount) AS total` 中的 `total`。
    """
    outer_select = expression if isinstance(expression, exp.Select) else None
    if outer_select is None and isinstance(expression, exp.With):
        outer_select = (
            expression.this if isinstance(expression.this, exp.Select) else None
        )
    if outer_select is None:
        return set()
    aliases: set[str] = set()
    for proj in outer_select.expressions:
        if proj.alias:  # 仅显式别名
            aliases.add(proj.alias)
    return aliases


def _is_in_alias_context(
    column: exp.Column, expression: exp.Expression
) -> bool:
    """检查 Column 节点是否位于可合法引用 SELECT 别名的子句中。

    SQLite 允许在 ORDER BY / GROUP BY / HAVING 中引用投影别名，
    这些位置不应对未限定列报 `unknown_column`。
    """
    parent = column.parent
    while parent is not None:
        if isinstance(parent, (exp.Order, exp.Group, exp.Having)):
            return True
        if isinstance(parent, exp.Select):
            for clause_key in ("order", "group", "having"):
                clause = parent.args.get(clause_key)
                if clause is not None:
                    for col_in_clause in clause.find_all(exp.Column):
                        if id(col_in_clause) == id(column):
                            return True
            return False
        parent = parent.parent
    return False


# ============================================================
# 4. 表/列校验
# ============================================================
def _table_aliases(expression: exp.Expression) -> dict[str, str]:
    """构造 `{alias_or_name: table_name}` 映射，用于解析 `column.table`。"""
    aliases: dict[str, str] = {}
    for table in expression.find_all(exp.Table):
        table_name = table.name
        alias = table.alias_or_name
        aliases[alias] = table_name
        aliases[table_name] = table_name
    return aliases


def _column_table(column: exp.Column, aliases: dict[str, str]) -> str | None:
    """从 Column 节点取其所属表（已用别名解析）。未限定返回 None。"""
    table = column.table
    if not table:
        return None
    return aliases.get(table, table)


def _validate_tables(
    expression: exp.Expression, schema: dict[str, set[str]]
) -> list[str]:
    """表白名单校验。虚拟表（CTE/子查询别名）跳过。"""
    violations: list[str] = []
    virtual = _virtual_table_names(expression)
    for table in expression.find_all(exp.Table):
        if table.name in virtual:
            continue
        if table.name not in schema:
            violations.append(f"unknown_table:{table.name}")
    return violations


def _check_stars(
    expression: exp.Expression, reject_select_star: bool
) -> list[str]:
    """`SELECT *` 拦截。

    仅检测**顶层 SELECT 投影列表**中的 `*`，不去管子查询里的 `COUNT(*)` / `SUM(*)`。
    这是对原版的修正——原版用 `find_all(exp.Star)` 会误伤聚合函数中的 `*`。
    """
    if not reject_select_star:
        return []
    for select in expression.find_all(exp.Select):
        for proj in select.expressions:
            if isinstance(proj, exp.Star):
                return ["select_star_not_allowed"]
    return []


def _cte_output_columns(expression: exp.Expression) -> set[str]:
    """收集所有 CTE 与子查询的输出列名（其 SELECT 列表的列名或别名）。

    这些列对外层 SELECT 而言是"已知"的（不需要再校验是否存在），但因为它们
    属于虚拟表（CTE 别名/子查询别名），外层未限定引用仍应允许。
    """
    cols: set[str] = set()
    for cte in expression.find_all(exp.CTE):
        cte_select = cte.this
        if isinstance(cte_select, exp.Select):
            for proj in cte_select.expressions:
                if proj.alias:
                    cols.add(proj.alias)
                elif isinstance(proj, exp.Column):
                    cols.add(proj.name)
    for sub in expression.find_all(exp.Subquery):
        sub_select = sub.this
        if isinstance(sub_select, exp.Select):
            for proj in sub_select.expressions:
                if proj.alias:
                    cols.add(proj.alias)
                elif isinstance(proj, exp.Column):
                    cols.add(proj.name)
    return cols


def _validate_columns(
    expression: exp.Expression, schema: dict[str, set[str]]
) -> list[str]:
    """列白名单校验，处理 4 类情况：

    1. 内层作用域的列（CTE/子查询体内）：按"是否在虚拟表或物理表中"分别处理
    2. 投影别名在 ORDER BY 中引用：合法
    3. 限定为虚拟表（CTE 别名）：跳过
    4. 未限定的外层列：仅在**当前 SQL 实际引用的物理表**中检查歧义。
       这是对原版"全 schema 检查"的修正——多表场景下 `SELECT order_id FROM orders`
       不会因其他表也有同名字段而被误报。

    歧义判断边界（场景 4）：
      - 当前 SQL 只引用 1 张表 → 同名字段只可能归属该表，不算歧义
      - 当前 SQL 引用 ≥2 张表 → 跨表同名字段强制要求限定
    """
    violations: list[str] = []
    aliases = _table_aliases(expression)
    virtual = _virtual_table_names(expression)
    inner_cols = _inner_scope_column_ids(expression)
    proj_aliases = _projection_aliases(expression)
    cte_cols = _cte_output_columns(expression)

    # 当前 SQL 实际引用的物理表（排除 CTE/子查询别名）
    referenced_tables: set[str] = {
        t.name
        for t in expression.find_all(exp.Table)
        if t.name not in virtual
    }

    for column in expression.find_all(exp.Column):
        column_name = column.name
        table_name = _column_table(column, aliases)

        # 场景 1：内层作用域的列
        if id(column) in inner_cols:
            if table_name is not None and table_name in virtual:
                # 限定为 CTE/子查询别名 → 跳过
                continue
            if table_name is not None:
                # 限定为物理表 → 正常校验
                if table_name not in schema:
                    violations.append(f"unknown_table:{table_name}")
                elif column_name not in schema[table_name]:
                    violations.append(
                        f"unknown_column:{table_name}.{column_name}"
                    )
                continue
            # 未限定的内层列：仅当所有表都不含该列时报错
            if column_name not in {c for cols in schema.values() for c in cols}:
                violations.append(f"unknown_column:{column_name}")
            continue

        # 场景 2：未限定列若匹配投影别名且在别名合法上下文（ORDER/GROUP/HAVING）中 → 跳过
        if table_name is None and column_name in proj_aliases:
            if _is_in_alias_context(column, expression):
                continue

        # 场景 3：限定为虚拟表 → 跳过
        if table_name is not None:
            if table_name in virtual:
                continue
            if table_name not in schema:
                violations.append(f"unknown_table:{table_name}")
            elif column_name not in schema[table_name]:
                violations.append(f"unknown_column:{table_name}.{column_name}")
            continue

        # 场景 4：未限定的外层列 → 仅在当前引用的物理表里查
        if not referenced_tables:
            # 极端情况：无任何物理表被引用（纯 CTE/子查询）
            # 跳过列校验，因为外层列不来自物理表
            continue
        # 优先匹配 CTE/子查询的输出列
        if column_name in cte_cols:
            continue
        owners = [
            t
            for t in referenced_tables
            if column_name in schema.get(t, set())
        ]
        if len(owners) == 0:
            violations.append(f"unknown_column:{column_name}")
        elif len(owners) > 1:
            # 同名字段在当前 SQL 实际引用的多表里都存在 → 强制要求限定
            violations.append(f"ambiguous_column:{column_name}")

    return violations


# ============================================================
# 5. LIMIT 注入与钳制
# ============================================================
def _ensure_limit(
    expression: exp.Expression, default_limit: int, max_limit: int
) -> tuple[exp.Expression, bool, list[str]]:
    """无 LIMIT 时注入默认值；超限时钳制到 max_limit。"""
    warnings: list[str] = []
    current_limit = expression.args.get("limit")
    if current_limit is None:
        expression.set("limit", exp.Limit(expression=exp.Literal.number(default_limit)))
        warnings.append("limit_injected")
        return expression, True, warnings

    limit_expr = current_limit.expression
    if isinstance(limit_expr, exp.Literal) and limit_expr.is_number:
        value = int(limit_expr.name)
        if value > max_limit:
            current_limit.set("expression", exp.Literal.number(max_limit))
            warnings.append("limit_clamped")
            return expression, True, warnings
    return expression, False, warnings


# ============================================================
# 6. 主入口
# ============================================================
def check_sql_safety(
    sql: str,
    *,
    table_infos: list[dict[str, Any]],
    default_limit: int = 1000,
    max_limit: int = 5000,
    reject_comments: bool = True,
    reject_select_star: bool = True,
    dialect: str = "sqlite",
) -> SQLSafetyResult:
    """检查 SQL 是否安全，并返回规范化后的 SQL。

    Args:
        sql: 待校验的 SQL 字符串
        table_infos: 表结构列表，格式 `[{"name": "orders", "columns": [{"name": "id"}, ...]}]`
        default_limit: 无 LIMIT 时注入的默认值
        max_limit: 限制上限，超过则钳制
        reject_comments: 是否拒绝包含注释（`--`、`/*`、`#`）的 SQL
        reject_select_star: 是否拒绝 `SELECT *`
        dialect: SQL 方言，默认 `sqlite`，可显式传 `mysql`

    Returns:
        `SQLSafetyResult`，包含是否通过、规范化 SQL、违规列表、警告列表

    Raises:
        不抛异常。所有错误通过 `SQLSafetyResult.is_safe` 与 `violations` 表达。
    """
    stripped = sql.strip()

    # 1. 注释检测（先于语法解析，节省时间）
    if reject_comments and _has_comment_markers_outside_literals(stripped):
        return _fail(stripped, ["comments_not_allowed"])

    # 2. 语法解析
    try:
        statements = sqlglot.parse(stripped, read=dialect)
    except Exception as exc:
        return _fail(stripped, [f"parse_error:{exc}"])

    # 3. 多语句拦截
    statements = [s for s in statements if s is not None]
    if len(statements) != 1:
        return _fail(stripped, ["multiple_statements"])

    expression = statements[0]

    # 4. 只读限制：仅允许 SELECT、WITH(CTE) 与集合运算 UNION/INTERSECT/EXCEPT
    #    集合运算（exp.SetOperation）的分支仍是 SELECT，其表/列白名单校验在后面照常生效
    if not isinstance(expression, (exp.Select, exp.With, exp.SetOperation)):
        return _fail(stripped, ["only_select_allowed"])

    # 5. 表/列白名单 + SELECT * 校验
    schema = _allowed_schema(table_infos)
    violations: list[str] = []

    if schema:
        violations.extend(_validate_tables(expression, schema))
        violations.extend(_check_stars(expression, reject_select_star))
        violations.extend(_validate_columns(expression, schema))
    else:
        # 无 schema 上下文时只检查 SELECT *（避免无 context 时一刀切）
        violations.extend(_check_stars(expression, reject_select_star))

    if violations:
        return _fail(stripped, sorted(set(violations)))

    # 6. LIMIT 注入/钳制
    expression, rewritten, warnings = _ensure_limit(
        expression, default_limit, max_limit
    )

    return SQLSafetyResult(
        is_safe=True,
        normalized_sql=expression.sql(dialect=dialect),
        violations=[],
        warnings=warnings,
        rewritten=rewritten,
        safety_summary="single_select_with_allowed_schema",
    )
