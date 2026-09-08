"""Deterministic intent, chart selection, and chart-data normalization."""
from __future__ import annotations

from numbers import Number
from typing import Any

TIME_COLUMNS = {"ym", "month", "week", "yweek", "date", "snapshot_date"}
BUCKET_COLUMNS = {"bucket", "amount_range", "segment", "repurchase_tier"}

LABELS = {
    "sales": "销售额", "sales_amount": "销售额", "total_sales": "销售额",
    "total_qty": "销量", "quantity": "销量", "order_count": "订单量",
    "customer_count": "客户数", "cnt": "数量", "aov": "客单价",
    "profit": "利润", "total_profit": "利润", "refund_amount": "退款金额",
    "avg_hours": "平均时长", "avg_resolution_hours": "平均时长", "sku_count": "SKU 数",
}

DIMENSION_LABELS = {"store_id":"门店", "city":"城市", "customer_level":"等级", "channel":"渠道", "brand":"品牌", "category":"类目", "ticket_status":"工单状态", "ticket_type":"工单类型", "refund_reason":"退款原因", "ym":"月份", "yweek":"周", "week":"周"}

def column_label(name: str) -> str:
    return DIMENSION_LABELS.get(name.lower(), LABELS.get(name.lower(), name))

UNITS = {
    "sales": "元", "sales_amount": "元", "total_sales": "元", "aov": "元",
    "profit": "元", "total_profit": "元", "refund_amount": "元",
    "total_qty": "件", "quantity": "件", "sku_count": "件",
    "order_count": "单", "customer_count": "人", "cnt": "个",
    "avg_hours": "小时", "avg_resolution_hours": "小时",
}


def _is_number(value: Any) -> bool:
    return isinstance(value, Number) and not isinstance(value, bool)


def _is_bucket(column: str) -> bool:
    lower = column.lower()
    return lower in BUCKET_COLUMNS or lower.endswith("_range") or "bucket" in lower or "tier" in lower


def infer_intent(question: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "table"
    columns = list(rows[0])
    lower = [c.lower() for c in columns]
    if len(rows) == 1 and len(columns) == 1:
        return "metric_query"
    if len(rows) == 1 and len(columns) == 2 and any(word in question for word in ("最高", "最低", "最多", "最少", "TOP", "Top", "top")):
        return "ranking"
    if len(rows) > 1 and any(c in TIME_COLUMNS or c.endswith("_date") for c in lower):
        return "trend"
    if any(_is_bucket(c) for c in lower) or any(word in question for word in ("分布", "分桶", "区间")):
        # A multi-dimensional distribution is a table, even when one column
        # happens to look like a bucket/tier.
        if len(columns) >= 3:
            return "table"
        return "distribution"
    if len(columns) == 2 and len(rows) <= 6:
        return "comparison"
    if len(columns) == 2 and len(rows) > 6:
        return "ranking"
    return "table"


def chart_type_for(intent: str, rows: list[dict[str, Any]]) -> str:
    if intent in {"metric_query"} or (intent == "ranking" and len(rows) == 1):
        return "kpi"
    return {"trend": "line", "distribution": "bar", "comparison": "pie", "ranking": "bar"}.get(intent, "table")


def build_chart_data(chart_type: str, rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if chart_type == "table" or not rows:
        return None
    columns = list(rows[0])
    numeric = [c for c in columns if any(_is_number(row.get(c)) for row in rows)]
    if chart_type == "kpi":
        metric = numeric[-1] if numeric else columns[-1]
        return {"categories": [], "series": [{"name": column_label(metric), "data": [rows[0].get(metric)]}], "unit": UNITS.get(metric, "")}
    dimension = next((c for c in columns if c not in numeric), columns[0])
    metrics = [c for c in numeric if c != dimension]
    if not metrics and len(columns) > 1:
        metrics = [columns[-1]]
    return {
        "categories": [row.get(dimension) for row in rows],
        "series": [{"name": column_label(metric), "data": [row.get(metric) for row in rows]} for metric in metrics],
        "unit": UNITS.get(metrics[0], "") if len(metrics) == 1 else "",
        "dimension": dimension, "dimension_label": column_label(dimension),
    }


def build_presentation(question: str, rows: list[dict[str, Any]]) -> tuple[str, str, dict[str, Any] | None]:
    intent = infer_intent(question, rows)
    chart_type = chart_type_for(intent, rows)
    return intent, chart_type, build_chart_data(chart_type, rows)
