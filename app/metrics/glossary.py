"""Business metric glossary with lightweight question matching."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class Metric:
    key: str
    name: str
    expression: str
    table: str
    description: str
    filters: tuple[str, ...] = ()

class MetricsGlossary:
    def __init__(self, metrics: dict[str, Metric]): self.metrics = metrics
    @classmethod
    def load(cls, path: str | Path) -> "MetricsGlossary":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls({key: Metric(key, value["name"], value["expression"], value["table"], value.get("description", ""), tuple(value.get("filters", []))) for key, value in raw.get("metrics", {}).items()})
    def match(self, question: str) -> list[Metric]:
        q = question.lower(); aliases = {"sales_amount": ("销售额", "销售收入", "实付金额", "gmv"), "order_count": ("订单量", "订单数", "多少订单"), "average_order_value": ("客单价", "平均订单金额"), "gross_profit": ("毛利", "利润", "盈利"), "refund_amount": ("退款金额", "退了多少钱", "退款"), "after_sales_resolution_hours": ("解决时长", "处理时长", "售后时长")}
        return [m for key, m in self.metrics.items() if any(a.lower() in q for a in aliases.get(key, (m.name,)))]
    def prompt_context(self, metrics: list[Metric] | None = None) -> str:
        return "\n".join(f"- {m.name} ({m.key}): {m.expression}; {m.description}" + (f"; 默认过滤: {', '.join(m.filters)}" if m.filters else "") for m in (metrics or list(self.metrics.values())))
