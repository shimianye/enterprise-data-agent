"""安全拦截评测（校验器层）。

指标 4「安全拦截准确率」的两层含义：
  - 校验器层（本脚本）：给定一条恶意/越权 SQL，`check_sql_safety` 是否拒绝。
    这是防御的底线，不依赖真实 LLM，可离线跑。
  - 端到端层（待真实 LLM 接入）：给定恶意/越权「问题」，模型是否生成出
    被拒绝的 SQL（或系统在意图层就拒答）。需真实 provider，Phase 2 再测。

本脚本只做校验器层，直接对 security_cases.jsonl 的 attack_sql 跑校验，
输出拦截率与违规码命中率。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sqlglot
from sqlglot import exp

from app.security.validator import check_sql_safety


def load_table_infos(init_sql_path: Path) -> list[dict]:
    """从 init.sql 解析出 10 张表的列清单，构造 validator 所需的 table_infos。"""
    sql = init_sql_path.read_text(encoding="utf-8")
    tables: list[dict] = []
    for stmt in sqlglot.parse(sql, read="sqlite"):
        if stmt is None or not isinstance(stmt, exp.Create):
            continue
        if isinstance(stmt.this, exp.Index):
            continue  # CREATE INDEX，不是建表
        schema = stmt.this if isinstance(stmt.this, exp.Schema) else stmt.find(exp.Schema)
        if schema is None:
            continue
        table_node = schema.this
        if not isinstance(table_node, exp.Table):
            continue
        columns = [
            {"name": col.name}
            for col in schema.expressions
            if isinstance(col, exp.ColumnDef)
        ]
        tables.append({"name": table_node.name, "columns": columns})
    return tables


def load_cases(cases_path: Path) -> list[dict]:
    return [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    root = ROOT
    table_infos = load_table_infos(root / "data" / "init.sql")
    cases = load_cases(root / "eval" / "security_cases.jsonl")

    blocked = 0
    violation_matched = 0
    failures: list[dict] = []

    print(f"白名单表：{sorted(t['name'] for t in table_infos)}")
    print(f"安全用例：{len(cases)} 条\n")

    for case in cases:
        result = check_sql_safety(case["attack_sql"], table_infos=table_infos)
        is_blocked = not result.is_safe
        matched = case["expected_violation"] in result.violations
        if is_blocked:
            blocked += 1
        if matched:
            violation_matched += 1
        # ASCII-only markers keep the evaluator usable in Windows GBK terminals.
        status = "BLOCK" if is_blocked else "MISS"
        if not is_blocked or not matched:
            failures.append({
                "id": case["id"],
                "is_blocked": is_blocked,
                "expected_violation": case["expected_violation"],
                "actual_violations": result.violations,
            })
            print(f"[{case['id']}] {status} | 期望违规={case['expected_violation']} | 实际={result.violations}")
        else:
            print(f"[{case['id']}] {status} | 违规码={result.violations}")

    total = len(cases)
    block_rate = blocked / total if total else 0.0
    match_rate = violation_matched / total if total else 0.0
    print("\n" + "=" * 60)
    print(f"安全拦截准确率（校验器层）：{blocked}/{total} = {block_rate:.1%}")
    print(f"违规码命中率：{violation_matched}/{total} = {match_rate:.1%}")
    print("=" * 60)

    report = {
        "total": total,
        "blocked": blocked,
        "violation_matched": violation_matched,
        "block_rate": round(block_rate, 4),
        "violation_match_rate": round(match_rate, 4),
        "failures": failures,
    }
    report_path = root / "eval" / "security_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"报告已写入 {report_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
