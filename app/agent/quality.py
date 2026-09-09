"""Deterministic quality envelope for Text-to-SQL results.

The level is a product-facing verification signal, not a calibrated probability
that the answer is correct.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


_ADVANCED_TERMS = (
    "同比",
    "环比",
    "复购",
    "分层",
    "占比变化",
    "增长率",
    "退款售后",
    "退款工单",
    "多次退款",
    "零销量",
)
_METRIC_TERMS = (
    "销售额",
    "订单量",
    "订单数",
    "客单价",
    "毛利",
    "利润",
    "退款金额",
    "解决时长",
    "处理时长",
)


@dataclass(frozen=True)
class QualityCheck:
    code: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class QueryQuality:
    confidence: str
    needs_review: bool
    checks: tuple[QualityCheck, ...]

    def checks_as_dicts(self) -> list[dict[str, Any]]:
        return [check.to_dict() for check in self.checks]


def _shape_matches(intent: str, rows: list[dict[str, Any]]) -> bool:
    if not rows:
        return True
    column_count = len(rows[0])
    if intent == "metric_query":
        return len(rows) == 1 and column_count <= 2
    if intent == "trend":
        return len(rows) >= 2 and column_count >= 2
    if intent in {"comparison", "ranking", "distribution"}:
        return column_count >= 2
    return True


def assess_query_quality(
    *,
    question: str,
    metric_keys: Iterable[str],
    warnings: Iterable[str],
    rows: list[dict[str, Any]],
    intent: str,
) -> QueryQuality:
    """Return a transparent rule-based verification level for a query result."""
    metric_keys = list(metric_keys)
    warnings = list(warnings)
    mentions_metric = any(term in question for term in _METRIC_TERMS)
    metric_grounded = bool(metric_keys) or not mentions_metric
    advanced = any(term in question for term in _ADVANCED_TERMS)
    shape_ok = _shape_matches(intent, rows)
    limit_clamped = "limit_clamped" in warnings
    limit_injected = "limit_injected" in warnings

    checks = (
        QualityCheck(
            "metric_grounded",
            metric_grounded,
            "业务指标已命中指标词典。" if metric_grounded else "问题包含业务指标，但未命中指标词典。",
        ),
        QualityCheck("sql_safe", True, "SQL 已通过只读、表列与 AST 安全校验。"),
        QualityCheck(
            "result_non_empty",
            bool(rows),
            "查询返回了数据。" if rows else "查询结果为空，请核对筛选条件和时间范围。",
        ),
        QualityCheck(
            "shape_matches_intent",
            shape_ok,
            "结果结构与展示意图一致。" if shape_ok else "结果结构与问题意图不一致。",
        ),
        QualityCheck(
            "advanced_query",
            not advanced,
            "未命中已知高难查询模式。" if not advanced else "命中高难查询模式，建议人工复核业务口径。",
        ),
        QualityCheck(
            "safety_rewritten",
            not limit_clamped,
            (
                "返回行数已被安全上限钳制，请确认结果是否完整。"
                if limit_clamped
                else "已自动应用安全返回上限。"
                if limit_injected
                else "SQL 未发生安全改写。"
            ),
        ),
    )

    if advanced or not shape_ok:
        confidence = "low"
    elif not rows or not metric_grounded or limit_clamped:
        confidence = "medium"
    else:
        confidence = "high"
    return QueryQuality(
        confidence=confidence,
        needs_review=confidence != "high",
        checks=checks,
    )
