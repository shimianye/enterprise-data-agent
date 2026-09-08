"""Report real-eval metrics split by baseline-60 / advanced-20 / total-80.

Reads a sql_dump (JSONL produced by run_eval.py --save-sql) and the
ADVANCED_IDS set (kept in sync with split_cases.py), then prints the
three-way breakdown for the headline metrics.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ADVANCED_IDS = {
    "Q007", "Q010", "Q033", "Q045", "Q051", "Q056", "Q061", "Q067",
    "Q068", "Q073", "Q075", "Q079", "Q034", "Q038", "Q052", "Q062",
    "Q066", "Q071", "Q077", "Q078",
}


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    passed = sum(1 for r in rows if r.get("status") == "passed")
    structure_ok = sum(1 for r in rows if r.get("structure_ok"))
    checkable = [r for r in rows if r.get("result_correct_checkable")]
    correct = sum(1 for r in checkable if r.get("result_correct"))
    row_ok = sum(1 for r in rows if r.get("row_count_ok"))
    return {
        "n": n,
        "exec_ok": passed,
        "exec_rate": passed / n if n else 0.0,
        "structure_ok": structure_ok,
        "row_ok": row_ok,
        "correct": correct,
        "checkable": len(checkable),
        "correct_rate": correct / len(checkable) if checkable else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", type=Path, default=Path(__file__).with_name("sql_dump-v9-80q.jsonl"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in args.dump.read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = {r["id"] for r in rows}
    missing = ADVANCED_IDS - ids
    if missing:
        raise SystemExit(f"advanced ids missing: {sorted(missing)}")

    advanced = [r for r in rows if r["id"] in ADVANCED_IDS]
    baseline = [r for r in rows if r["id"] not in ADVANCED_IDS]

    def pct(x: float) -> str:
        return f"{x * 100:.1f}%"

    for label, group in (("基础集 baseline-60", baseline), ("进阶集 advanced-20", advanced), ("总集 total-80", rows)):
        s = summarize(group)
        print(f"[{label}]")
        print(f"  题数 {s['n']} | SQL 可执行 {s['exec_ok']}/{s['n']} ({pct(s['exec_rate'])}) | "
              f"结构正确 {s['structure_ok']}/{s['n']} | 行数正确 {s['row_ok']}/{s['n']}")
        print(f"  结果正确 {s['correct']}/{s['checkable']} ({pct(s['correct_rate'])})")

    # failing ids per split (result wrong or non-checkable)
    for label, group in (("基础集", baseline), ("进阶集", advanced)):
        wrong = [r["id"] for r in group if r.get("result_correct_checkable") and not r.get("result_correct")]
        ncc = [r["id"] for r in group if not r.get("result_correct_checkable")]
        print(f"[{label}] 结果错误 {len(wrong)}: {wrong}")
        print(f"[{label}] 不可对拍 {len(ncc)}: {ncc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
