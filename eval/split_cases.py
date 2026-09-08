"""Create the documented 60-question baseline and 20-question advanced suites."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ADVANCED_IDS = {
    "Q007", "Q010", "Q033", "Q045", "Q051", "Q056", "Q061", "Q067",
    "Q068", "Q073", "Q075", "Q079", "Q034", "Q038", "Q052", "Q062",
    "Q066", "Q071", "Q077", "Q078",
}

def split(source: Path) -> tuple[list[dict], list[dict]]:
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = {row["id"] for row in rows}
    missing = ADVANCED_IDS - ids
    if missing:
        raise ValueError(f"advanced ids missing from cases: {sorted(missing)}")
    if len(rows) != 80:
        raise ValueError(f"expected 80 cases, got {len(rows)}")
    advanced = [row for row in rows if row["id"] in ADVANCED_IDS]
    baseline = [row for row in rows if row["id"] not in ADVANCED_IDS]
    return baseline, advanced

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).with_name("cases.jsonl"))
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    baseline, advanced = split(args.source)
    for name, rows in (("cases-baseline-60.jsonl", baseline), ("cases-advanced-20.jsonl", advanced)):
        path = args.out_dir / name
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        print(f"{path}: {len(rows)} cases")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
