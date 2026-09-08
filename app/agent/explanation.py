"""Deterministic natural-language explanations."""
from __future__ import annotations
from numbers import Number
from typing import Any
from app.agent.presentation import column_label

def _format(value: Any) -> str:
    if isinstance(value, Number) and not isinstance(value, bool):
        if isinstance(value, float) and not value.is_integer(): return f"{value:,.2f}".rstrip("0").rstrip(".")
        return f"{value:,.0f}"
    return str(value)

def _topic(question: str) -> str:
    for word in ("销售额", "客单价", "SKU 数量", "SKU", "销量", "客户数", "缺货", "订单金额"):
        if word in question: return word
    return "查询结果"

def explain(question: str, intent: str, chart_data: dict[str, Any] | None, rows: list[dict[str, Any]]) -> str:
    if not rows: return "未查询到符合条件的数据。"
    if intent == "table" or chart_data is None:
        dims = [c for c in rows[0] if not any(isinstance(r.get(c), Number) and not isinstance(r.get(c), bool) for r in rows[:20])]
        return f"共 {len(rows)} 条记录，涵盖 {'、'.join(column_label(c) for c in dims) or '相关维度'}。"
    categories, series, unit = chart_data["categories"], chart_data["series"], chart_data.get("unit", "")
    values = series[0]["data"] if series else []
    metric = series[0].get("name", "指标") if series else "指标"
    if intent == "metric_query": return f"{question}：{_topic(question)}为 {_format(values[0])}{unit}。"
    if intent == "ranking":
        best = max(range(len(values)), key=lambda i: values[i]); prefix = chart_data.get("dimension_label", "")
        if not categories and rows:
            dims = [k for k, v in rows[0].items() if not isinstance(v, Number)]
            categories = [rows[0].get(dims[0], "TOP1")] if dims else ["TOP1"]
        verb = "最多" if unit in {"件", "个", "人", "单", "次"} else "最高"
        name = f"{prefix} {categories[best]}" if prefix else str(categories[best])
        return f"{question}：{metric}{verb}的是 {name}（{_format(values[best])}{unit}）。"
    if intent == "trend": return f"{_topic(question)}从 {categories[0]} 的 {_format(values[0])}{unit} 变化到 {categories[-1]} 的 {_format(values[-1])}{unit}。"
    if intent == "comparison":
        total = sum(v for v in values if isinstance(v, Number)); dim = chart_data.get("dimension_label", "分类")
        best = max(range(len(values)), key=lambda i: values[i])
        parts = [f"{categories[i]}{'最高' if i == best else ''}（{_format(values[i])}{unit}，占 {(values[i] / total * 100 if total else 0):.1f}%）" for i in range(len(categories))]
        return f"{len(categories)} 个{dim}中，" + "、".join(parts) + "。"
    if intent == "distribution":
        best = max(range(len(values)), key=lambda i: values[i]); total = sum(v for v in values if isinstance(v, Number)); pct = values[best] / total * 100 if total else 0
        return f"{categories[best]} 区间占比最高（{_format(values[best])}{unit}，占 {pct:.1f}%）；共 {len(categories)} 个区间。"
    return f"共 {len(rows)} 条记录。"
