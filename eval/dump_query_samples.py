"""Dump real QueryResult payloads as frontend mock fixtures (Phase 3 step 4).

Replays the golden_sql of eval/cases-chart-nl.jsonl against the real SQLite DB,
runs the actual presentation + explanation pipeline, and writes the exact JSON
the /api/query endpoint would return.

Usage:
    python eval/dump_query_samples.py                 # -> eval/fixtures/query-samples.json
    python eval/dump_query_samples.py --limit-rows 50 # truncate rows per sample
"""
from __future__ import annotations
import argparse, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent.explanation import explain
from app.agent.presentation import build_presentation
from app.metrics.glossary import MetricsGlossary


def load_jsonl(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        text = text[1:]
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(ROOT / "eval" / "cases-chart-nl.jsonl"))
    ap.add_argument("--source", default=str(ROOT / "eval" / "cases.jsonl"))
    ap.add_argument("--db", default=str(ROOT / "data" / "enterprise.db"))
    ap.add_argument("--out", default=str(ROOT / "eval" / "fixtures" / "query-samples.json"))
    ap.add_argument("--limit-rows", type=int, default=0, help="0 = keep all rows")
    args = ap.parse_args()

    cases = load_jsonl(Path(args.cases))
    source = {row["id"]: row for row in load_jsonl(Path(args.source))}
    try:
        glossary = MetricsGlossary.load(ROOT / "config" / "metrics.yaml")
    except Exception:  # pragma: no cover - fixtures must never block on config
        glossary = None

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    samples = []
    for case in cases:
        src = source[case["source_case_id"]]
        rows = [dict(r) for r in conn.execute(src["golden_sql"]).fetchall()]
        intent, chart_type, chart_data = build_presentation(case["question"], rows)
        metric_keys = [m.key for m in glossary.match(case["question"])] if glossary else []
        kept = rows[: args.limit_rows] if args.limit_rows else rows
        samples.append({
            "id": case["id"],
            "question": case["question"],
            "sql": src["golden_sql"],
            "rows": kept,
            "row_count": len(rows),
            "duration_ms": 0,
            "metric_keys": metric_keys,
            "warnings": [],
            "intent": intent,
            "chart_type": chart_type,
            "chart_data": chart_data,
            "nl_explanation": explain(case["question"], intent, chart_data, rows),
        })
    conn.close()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    shapes = sorted({f"{s['intent']}/{s['chart_type']}" for s in samples})
    print(f"[SAMPLES] {len(samples)} written -> {out}")
    print("[SHAPES] " + ", ".join(shapes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
