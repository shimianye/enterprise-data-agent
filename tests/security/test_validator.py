"""
SQL 安全校验模块单元测试
========================

覆盖：注释词法分析、多语句拦截、只读限制、表/列白名单、CTE 作用域、
投影别名、歧义列、SELECT *、LIMIT 注入/钳制、SQLite 方言、错误信息。

运行：
    pip install -r tests/requirements.txt
    pytest tests/security/ -v
"""

from __future__ import annotations

import pytest

from app.security.validator import (
    SQLSafetyResult,
    SQLValidationError,
    _has_comment_markers_outside_literals,
    check_sql_safety,
)


# ============================================================
# Fixture：10 张经营分析表的简化 schema
# ============================================================
@pytest.fixture
def schema() -> list[dict]:
    """本项目 10 张核心表的最小可用 schema（仅含测试涉及的字段）。"""
    return [
        {
            "name": "orders",
            "columns": [
                {"name": "order_id"},
                {"name": "customer_id"},
                {"name": "store_id"},
                {"name": "order_status"},
                {"name": "paid_amount"},
                {"name": "paid_at"},
                {"name": "promotion_id"},
            ],
        },
        {
            "name": "order_items",
            "columns": [
                {"name": "item_id"},
                {"name": "order_id"},
                {"name": "product_id"},
                {"name": "brand"},
                {"name": "category"},
                {"name": "quantity"},
                {"name": "unit_price"},
                {"name": "line_paid_amount"},
                {"name": "subtotal_profit"},
            ],
        },
        {
            "name": "products",
            "columns": [
                {"name": "product_id"},
                {"name": "product_name"},
                {"name": "brand"},
                {"name": "category"},
                {"name": "cost_price"},
                {"name": "sale_price"},
            ],
        },
        {
            "name": "customers",
            "columns": [
                {"name": "customer_id"},
                {"name": "customer_name"},
                {"name": "customer_level"},
                {"name": "registered_at"},
            ],
        },
        {
            "name": "stores",
            "columns": [
                {"name": "store_id"},
                {"name": "store_name"},
                {"name": "city"},
                {"name": "region"},
            ],
        },
        {
            "name": "refunds",
            "columns": [
                {"name": "refund_id"},
                {"name": "order_id"},
                {"name": "refund_amount"},
                {"name": "refund_status"},
                {"name": "completed_at"},
            ],
        },
        {
            "name": "after_sales",
            "columns": [
                {"name": "ticket_id"},
                {"name": "order_id"},
                {"name": "ticket_status"},
                {"name": "response_time_minutes"},
                {"name": "satisfaction_score"},
            ],
        },
        {
            "name": "inventory_snapshots",
            "columns": [
                {"name": "store_id"},
                {"name": "product_id"},
                {"name": "snapshot_date"},
                {"name": "quantity_available"},
                {"name": "reorder_level"},
            ],
        },
        {
            "name": "promotions",
            "columns": [
                {"name": "promotion_id"},
                {"name": "name"},
                {"name": "type"},
            ],
        },
        {
            "name": "payments",
            "columns": [
                {"name": "payment_id"},
                {"name": "order_id"},
                {"name": "payment_method"},
                {"name": "payment_amount"},
            ],
        },
    ]


# ============================================================
# 1. 注释词法分析（独立函数）
# ============================================================
class TestCommentDetection:
    def test_single_line_comment_detected(self):
        assert _has_comment_markers_outside_literals("SELECT 1 -- comment") is True

    def test_block_comment_detected(self):
        assert _has_comment_markers_outside_literals("SELECT /* hide */ 1") is True

    def test_hash_comment_detected(self):
        assert _has_comment_markers_outside_literals("SELECT 1 # comment") is True

    def test_comment_inside_single_quotes_ignored(self):
        # 关键！'--' 在字符串内不算注释
        assert _has_comment_markers_outside_literals("SELECT 'a -- b' AS x") is False

    def test_comment_inside_double_quotes_ignored(self):
        assert _has_comment_markers_outside_literals('SELECT "a -- b" AS x') is False

    def test_comment_inside_backticks_ignored(self):
        assert _has_comment_markers_outside_literals("SELECT `a -- b` AS x") is False

    def test_escaped_single_quote_in_string(self):
        # SQL 标准转义：'' 在单引号字符串内表示一个字面 '
        assert (
            _has_comment_markers_outside_literals("SELECT 'it''s ok' AS x") is False
        )

    def test_no_comment(self):
        assert (
            _has_comment_markers_outside_literals("SELECT paid_amount FROM orders")
            is False
        )


# ============================================================
# 2. 多语句拦截
# ============================================================
class TestMultipleStatements:
    def test_two_selects_blocked(self, schema):
        sql = "SELECT 1; SELECT 2"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert "multiple_statements" in result.violations

    def test_select_with_trailing_semicolon_ok(self, schema):
        # 单条 SQL 末尾的分号合法
        sql = "SELECT paid_amount FROM orders;"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe

    def test_select_then_drop_blocked(self, schema):
        sql = "SELECT paid_amount FROM orders; DROP TABLE orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe


# ============================================================
# 3. 只读 SQL 限制
# ============================================================
class TestReadOnly:
    @pytest.mark.parametrize(
        "sql",
        [
            "DELETE FROM orders",
            "UPDATE orders SET paid_amount = 0",
            "INSERT INTO orders (order_id) VALUES (1)",
            "DROP TABLE orders",
            "TRUNCATE TABLE orders",
            "ALTER TABLE orders ADD COLUMN x INT",
            "CREATE TABLE x (id INT)",
            "REPLACE INTO orders VALUES (1)",
        ],
    )
    def test_writes_blocked(self, schema, sql):
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert "only_select_allowed" in result.violations


# ============================================================
# 4. 表/列白名单
# ============================================================
class TestSchemaValidation:
    def test_unknown_table_blocked(self, schema):
        sql = "SELECT * FROM users"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert any("unknown_table:users" in v for v in result.violations)

    def test_unknown_column_blocked(self, schema):
        sql = "SELECT nonexistent FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        # 未限定列报错时只带列名（因为表名不可知）
        assert any(
            v == "unknown_column:nonexistent" for v in result.violations
        )

    def test_known_columns_pass(self, schema):
        sql = "SELECT order_id, paid_amount FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_empty_schema_only_checks_star(self, schema):
        # 无 schema 上下文时，不校验表/列，但仍检查 SELECT *
        sql = "SELECT * FROM anything"
        result = check_sql_safety(sql, table_infos=[])
        assert not result.is_safe
        assert "select_star_not_allowed" in result.violations

    def test_multiple_unknown_tables(self, schema):
        sql = "SELECT * FROM a, b"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        # 至少包含 a 和 b 两个 unknown_table
        assert sum(1 for v in result.violations if v.startswith("unknown_table")) >= 2


# ============================================================
# 5. CTE / 子查询作用域
# ============================================================
class TestCTEScope:
    def test_cte_column_references_pass(self, schema):
        sql = """
        WITH aug AS (
            SELECT category, SUM(line_paid_amount) AS s
            FROM order_items
            GROUP BY category
        )
        SELECT category, s FROM aug WHERE s > 1000
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_subquery_alias_references_pass(self, schema):
        sql = """
        SELECT o.order_id, sub.t
        FROM orders o
        JOIN (SELECT order_id, COUNT(*) AS t FROM order_items GROUP BY order_id) sub
        ON o.order_id = sub.order_id
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_multiple_ctes(self, schema):
        sql = """
        WITH aug AS (
            SELECT category, SUM(line_paid_amount) AS s
            FROM order_items
            GROUP BY category
        ),
        jul AS (
            SELECT category, SUM(line_paid_amount) AS s
            FROM order_items
            GROUP BY category
        )
        SELECT aug.category, (aug.s - jul.s) / jul.s AS growth
        FROM aug JOIN jul ON aug.category = jul.category
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"


# ============================================================
# 6. 投影别名
# ============================================================
class TestProjectionAliases:
    def test_order_by_references_select_alias(self, schema):
        # GROUP BY 后用聚合别名排序，常见用法
        sql = """
        SELECT order_status, SUM(paid_amount) AS total
        FROM orders
        GROUP BY order_status
        ORDER BY total
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_order_by_alias_desc(self, schema):
        sql = """
        SELECT brand, SUM(quantity) AS qty
        FROM order_items
        GROUP BY brand
        ORDER BY qty DESC
        LIMIT 5
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe

    def test_order_by_nonexistent_column_blocked(self, schema):
        sql = "SELECT SUM(paid_amount) AS total FROM orders ORDER BY nonexistent"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe

    def test_group_by_references_select_alias(self, schema):
        # SQLite 允许 GROUP BY 引用 SELECT 别名（如 strftime 别名）
        sql = """
        SELECT strftime('%Y-%m', paid_at) AS ym, SUM(paid_amount) AS sales
        FROM orders
        WHERE paid_at >= '2026-01-01' AND paid_at < '2026-07-01'
        GROUP BY ym ORDER BY ym
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"


# ============================================================
# 7. 歧义列检测
# ============================================================
class TestAmbiguousColumn:
    def test_ambiguous_order_id_between_orders_and_items(self, schema):
        # orders 和 order_items 都有 order_id，未限定 → 歧义
        sql = """
        SELECT order_id
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert any("ambiguous_column:order_id" in v for v in result.violations)

    def test_qualified_columns_pass(self, schema):
        sql = """
        SELECT orders.order_id, order_items.product_id
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe

    def test_unique_column_no_ambiguity(self, schema):
        # orders.cancelled_at 这种 orders 独有的字段（即使 schema 中不列）
        # 我们用 schema 中列出的字段测试：order_id 在 orders/order_items 都存在
        # 但 store_id 只在 orders 中存在，product_id 只在 order_items 中存在
        sql = """
        SELECT o.store_id, oi.product_id
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe


# ============================================================
# 8. SELECT * 拦截
# ============================================================
class TestSelectStar:
    def test_select_star_blocked_by_default(self, schema):
        sql = "SELECT * FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert "select_star_not_allowed" in result.violations

    def test_select_star_allowed_when_disabled(self, schema):
        sql = "SELECT * FROM orders"
        result = check_sql_safety(sql, table_infos=schema, reject_select_star=False)
        assert result.is_safe

    def test_count_star_allowed(self, schema):
        # COUNT(*) 是聚合，不算裸露的 SELECT *
        sql = "SELECT COUNT(*) AS cnt FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe

    def test_sum_with_star_column_blocked(self, schema):
        # 混合 * 与其他字段时，整体仍属于 select * 行为
        sql = "SELECT *, paid_amount FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe


# ============================================================
# 9. LIMIT 注入与钳制
# ============================================================
class TestLimit:
    def test_missing_limit_injected(self, schema):
        sql = "SELECT order_id FROM orders"
        result = check_sql_safety(
            sql, table_infos=schema, default_limit=500, max_limit=1000
        )
        assert result.is_safe
        assert "limit_injected" in result.warnings
        assert "LIMIT 500" in result.normalized_sql.upper()

    def test_limit_clamped_when_too_large(self, schema):
        sql = "SELECT order_id FROM orders LIMIT 99999"
        result = check_sql_safety(
            sql, table_infos=schema, default_limit=500, max_limit=1000
        )
        assert result.is_safe
        assert "limit_clamped" in result.warnings
        assert "LIMIT 1000" in result.normalized_sql.upper()

    def test_normal_limit_unchanged(self, schema):
        sql = "SELECT order_id FROM orders LIMIT 100"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe
        assert result.warnings == []
        assert "LIMIT 100" in result.normalized_sql.upper()

    def test_limit_at_max_unchanged(self, schema):
        # 恰好等于 max_limit 不算超限
        sql = "SELECT order_id FROM orders LIMIT 1000"
        result = check_sql_safety(
            sql, table_infos=schema, default_limit=500, max_limit=1000
        )
        assert result.is_safe
        assert result.warnings == []


# ============================================================
# 10. SQL 方言与边界
# ============================================================
class TestDialect:
    def test_default_dialect_is_sqlite(self, schema):
        sql = "SELECT order_id FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe
        # SQLite 方言下 FROM 表名无引号
        assert "FROM orders" in result.normalized_sql

    def test_explicit_mysql_dialect(self, schema):
        sql = "SELECT order_id FROM orders"
        result = check_sql_safety(sql, table_infos=schema, dialect="mysql")
        assert result.is_safe

    def test_parse_error_returned(self, schema):
        # 故意语法错误
        result = check_sql_safety("SELECT FROM WHERE", table_infos=schema)
        assert not result.is_safe
        assert any(v.startswith("parse_error") for v in result.violations)


# ============================================================
# 11. 错误信息可读性
# ============================================================
class TestErrorMessages:
    def test_sql_validation_error_contains_violations(self):
        err = SQLValidationError(["unknown_table:users", "select_star_not_allowed"])
        msg = str(err)
        assert "unknown_table:users" in msg
        assert "select_star_not_allowed" in msg

    def test_result_str_includes_summary(self, schema):
        result = check_sql_safety("SELECT 1", table_infos=schema)
        s = str(result)
        assert "SQLSafetyResult" in s


# ============================================================
# 12. 真实业务 SQL 集成测试（来自 eval/cases_draft.jsonl 的 golden_sql）
# ============================================================
class TestRealBusinessQueries:
    """抽样评测集中的 golden_sql，验证校验器不会误伤真实业务查询。"""

    def test_q001_total_sales(self, schema):
        sql = """
        SELECT SUM(paid_amount) FROM orders
        WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01'
          AND order_status <> 'cancelled'
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_q002_store_city_sales(self, schema):
        sql = """
        SELECT SUM(o.paid_amount)
        FROM orders o
        JOIN stores s ON o.store_id = s.store_id
        WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01'
          AND o.order_status <> 'cancelled'
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_q007_cte_mom_growth(self, schema):
        sql = """
        WITH aug AS (
            SELECT category, SUM(line_paid_amount) AS s
            FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
            WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01'
              AND o.order_status <> 'cancelled'
            GROUP BY category
        ), jul AS (
            SELECT category, SUM(line_paid_amount) AS s
            FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
            WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01'
              AND o.order_status <> 'cancelled'
            GROUP BY category
        )
        SELECT aug.category, (aug.s - jul.s) / jul.s AS growth
        FROM aug JOIN jul ON aug.category = jul.category
        WHERE jul.s > 0
        ORDER BY growth DESC LIMIT 1
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_q017_scalar_subquery_refund_rate(self, schema):
        sql = """
        SELECT
            (SELECT SUM(refund_amount) FROM refunds
             WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01'
               AND refund_status = 'completed')
            /
            (SELECT SUM(paid_amount) FROM orders
             WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01'
               AND order_status <> 'cancelled')
        """
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"


# ============================================================
# 13. 集合运算（UNION / INTERSECT / EXCEPT）只读识别
# ============================================================
class TestSetOperations:
    """集合运算也是只读查询，应放行；但分支内的表/列白名单校验必须照常生效。"""

    def test_union_select_allowed(self, schema):
        sql = "SELECT paid_amount FROM orders UNION SELECT refund_amount FROM refunds"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_union_gets_default_limit(self, schema):
        sql = "SELECT paid_amount FROM orders UNION SELECT refund_amount FROM refunds"
        result = check_sql_safety(sql, table_infos=schema)
        assert "limit_injected" in result.warnings

    def test_union_with_unknown_table_blocked(self, schema):
        sql = "SELECT paid_amount FROM orders UNION SELECT id FROM users"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert "unknown_table:users" in result.violations

    def test_union_with_select_star_blocked(self, schema):
        sql = "SELECT * FROM orders UNION SELECT refund_amount FROM refunds"
        result = check_sql_safety(sql, table_infos=schema)
        assert not result.is_safe
        assert "select_star_not_allowed" in result.violations

    def test_intersect_allowed(self, schema):
        sql = "SELECT paid_amount FROM orders INTERSECT SELECT paid_amount FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_except_allowed(self, schema):
        sql = "SELECT paid_amount FROM orders EXCEPT SELECT paid_amount FROM orders"
        result = check_sql_safety(sql, table_infos=schema)
        assert result.is_safe, f"violations: {result.violations}"

    def test_union_limit_clamped(self, schema):
        sql = "SELECT paid_amount FROM orders UNION SELECT refund_amount FROM refunds LIMIT 99999"
        result = check_sql_safety(sql, table_infos=schema, max_limit=5000)
        assert result.is_safe
        assert "limit_clamped" in result.warnings

