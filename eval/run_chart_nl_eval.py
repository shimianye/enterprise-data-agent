"""Chart / NL-explanation evaluation (Phase 3).

Loads eval/cases-chart-nl.jsonl, replays each source case's golden_sql to get
real rows, then checks the deterministic presentation + explanation output.
"""
from __future__ import annotations
import argparse, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent.explanation import explain
from app.agent.presentation import build_presentation


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh.read().splitlines() if line.strip()]


def check_case(case: dict, rows: list[dict]) -> tuple[bool, list[str], str, str, str]:
    """Return (passed, failures, intent, chart_type, explanation)."""
    intent, chart_type, chart_data = build_presentation(case["question"], rows)
    text = explain(case["question"], intent, chart_data, rows)
    failures = []

    if intent != case["expected_intent"]:
        failures.append(f"intent: 期望={case['expected_intent']} 实际={intent}")
    if chart_type != case["expected_chart_type"]:
        failures.append(f"chart_type: 期望={case['expected_chart_type']} 实际={chart_type}")

    want_cats = case.get("expect_categories_count")
    want_series = case.get("expect_series_count")
    if want_cats is not None:
        got = len(chart_data["categories"]) if chart_data else None
        if got != want_cats:
            failures.append(f"categories: 期望={want_cats} 实际={got}")
    if want_series is not None:
        got = len(chart_data["series"]) if chart_data else None
        if got != want_series:
            failures.append(f"series: 期望={want_series} 实际={got}")

    for kw in case.get("expect_explanation_contains", []):
        if kw not in text:
            failures.append(f"explanation 缺关键词: {kw!r}")

    flat = text.replace(",", "")
    for digits in case.get("expect_explanation_contains_digits", []):
        if digits.replace(",", "") not in flat:
            failures.append(f"explanation 缺数字: {digits!r}")

    return (not failures), failures, intent, chart_type, text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(ROOT / "eval" / "cases-chart-nl.jsonl"))
    ap.add_argument("--source", default=str(ROOT / "eval" / "cases.jsonl"))
    ap.add_argument("--db", default=str(ROOT / "data" / "enterprise.db"))
    ap.add_argument("--report", default=str(ROOT / "eval" / "report-chart-nl.md"))
    args = ap.parse_args()

    cases = load_jsonl(Path(args.cases))
    source = {row["id"]: row for row in load_jsonl(Path(args.source))}
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    results = []
    for case in cases:
        src = source[case["source_case_id"]]
        cur = conn.execute(src["golden_sql"])
        rows = [dict(r) for r in cur.fetchall()]
        passed, failures, intent, chart_type, text = check_case(case, rows)
        results.append({"id": case["id"], "passed": passed, "failures": failures,
                        "intent": intent, "chart_type": chart_type, "explanation": text})
    conn.close()

    total = len(results)
    ok = sum(r["passed"] for r in results)
    lines = ["# 图表 / NL 解释评测报告", "",
             f"总题数: {total}", f"通过: {ok}/{total} = {ok / total if total else 0:.1%}", "",
             "| ID | 意图 | 图表 | 结果 |", "|---|---|---|---|"]
    for case, res in zip(cases, results):
        mark = "PASS" if res["passed"] else "FAIL"
        lines.append(f"| {case['id']} | {res['intent']} | {res['chart_type']} | {mark} |")
    lines += ["", "## 全部解释文本", "",
              "| ID | 题目 | 生成解释 |", "|---|---|---|"]
    for case, res in zip(cases, results):
        lines.append(f"| {case['id']} | {case['question']} | {res['explanation']} |")
    lines += ["", "## 失败明细", ""]
    for case, res in zip(cases, results):
        if res["passed"]:
            continue
        lines.append(f"### {case['id']} {case['question']}")
        lines.append(f"- 期望 intent={case['expected_intent']} chart={case['expected_chart_type']}")
        lines.append(f"- 实际 intent={res['intent']} chart={res['chart_type']}")
        lines.append(f"- 生成解释: {res['explanation']}")
        for f in res["failures"]:
            lines.append(f"- {f}")
        lines.append("")

    out = "\n".join(lines) + "\n"
    # ASCII-only summary keeps this usable in Windows GBK terminals.
    print(f"[SUMMARY] total={total} passed={ok} failed={total - ok}")
    for case, res in zip(cases, results):
        if not res["passed"]:
            print(f"[FAIL] {case['id']}: " + " | ".join(res["failures"]))
    Path(args.report).write_text(out, encoding="utf-8")
    print(f"report written: {args.report}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
