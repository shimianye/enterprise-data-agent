"""Rule-based checks applied to returned analytical rows."""
from __future__ import annotations

from typing import Any


def validate_result(question: str, rows: list[dict[str, Any]], intent: str) -> tuple[str, list[str]]:
    """Return a product-facing status and actionable warnings.

    These checks are deliberately conservative: they flag suspicious output for
    review rather than silently changing the user's data.
    """
    warnings: list[str] = []
    if not rows:
        return "empty", ["empty_result"]
    keys = {str(k).lower() for k in rows[0]}
    if any("percent" in k or "ratio" in k or "rate" in k or "占比" in k for k in keys):
        values = [v for row in rows for k, v in row.items()
                  if any(token in str(k).lower() for token in ("percent", "ratio", "rate", "占比"))
                  and isinstance(v, (int, float))]
        if any(v < 0 or v > 100 for v in values):
            warnings.append("percentage_out_of_range")
    if any("denominator" in k or "分母" in k for k in keys):
        if any(row.get(k) in (0, None) for row in rows for k in row if "denominator" in str(k).lower() or "分母" in str(k)):
            warnings.append("zero_denominator")
    if intent in {"trend", "comparison", "ranking"} and len(rows[0]) < 2:
        warnings.append("aggregate_detail_mismatch")
    if any(token in question for token in ("同比", "环比", "趋势", "按月", "按天")):
        if not any(any(token in str(k) for token in ("date", "month", "week", "day", "日期", "月份")) for k in keys):
            warnings.append("time_dimension_missing")
    return ("warning" if warnings else "ok"), warnings
