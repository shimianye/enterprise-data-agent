"""LLM boundary. Mock mode is deterministic and requires no network or API key."""
from __future__ import annotations
from typing import Protocol
import os
import re
import httpx
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

class LLMClient(Protocol):
    def generate_sql(self, question: str, context: str) -> str: ...

class MockLLMClient:
    def __init__(self, cases_path: str):
        import json
        with open(cases_path, encoding="utf-8") as handle:
            self.cases = {row["question"]: row["golden_sql"] for row in map(json.loads, handle)}
    def generate_sql(self, question: str, context: str) -> str:
        if question not in self.cases:
            raise ValueError("mock model has no golden SQL for this question")
        return self.cases[question]

class OpenAICompatibleClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None, timeout: float = 60):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = (base_url or os.getenv("LLM_BASE_URL", "https://api.deepseek.com")).rstrip("/")
        self.model = model or os.getenv("LLM_MODEL", "deepseek-chat")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("LLM_API_KEY is required for the real provider")

    def generate_sql(self, question: str, context: str) -> str:
        system = (
            "You are a SQLite Text2SQL analyst for a retail business. Return exactly one read-only SQL statement (SELECT or WITH). No markdown, no explanation.\n"
            "Hard rules:\n"
            "1. Metric names (销售额, 毛利, 订单量, 退款金额) are NOT column names; expand them using the definitions.\n"
            "2. Only use table/column names literally present in the schema. Never invent columns such as month, sales_amount, or sales.\n"
            "3. Month bucketing MUST use strftime('%Y-%m', <time_column>).\n"
            "4. Time filters MUST use half-open ranges: col >= 'YYYY-MM-DD' AND col < 'YYYY-MM-DD'.\n"
            "5. Metric default filters are mandatory, including paid_amount > 0 where specified.\n"
            "6. Counts across order_items must use COUNT(DISTINCT orders.order_id).\n"
            "7. Sales uses paid_amount, never order_amount; item profit uses order_items.subtotal_profit; refunds and after_sales are separate facts.\n"
            "8. Output shape MUST obey the question: total/ratio/count/average returns exactly ONE metric column; ranking returns ONLY the requested dimension plus ONE metric column. Never add auxiliary aggregates.\n"
            "9. Golden metrics: total profit uses orders.profit_amount directly; inventory questions default to inventory_snapshots only; refund reason filters requested_at; refund rate uses two independent scalar subqueries and never joins funds facts.\n"
            "10. Time semantics: orders transaction and customer behavior filters use paid_at, not created_at; refunds use completed_at or requested_at according to the question; inventory uses snapshot_date.\n"
            "11. Inventory semantics: inventory quantity means quantity_on_hand; available stock means quantity_available; reorder threshold is reorder_level; stockout uses quantity_available = 0 or below reorder_level.\n"
            "12. For ranking/grouped questions return only the requested dimension and one metric; never join or add display columns such as store_name unless explicitly requested.\n"
            "13. Column-field ownership: every referenced column MUST belong to a table currently in FROM/JOIN. Never reference columns from unrelated tables (e.g. store_id on refunds, customer_id on refunds, reason on refunds—use refund_reason; total_profit does not exist).\n"
            "14. Fact-table ownership: refund amount / refund reason / refund rate reads ONLY refunds (filter refund_status='completed', time on completed_at or requested_at). After-sales tickets (resolution_time, satisfaction, ticket_type) read ONLY after_sales. Never use ticket_type='退款' as a proxy for refund—the funds truth lives in refunds.\n"
            "15. Time anchoring: use the absolute dates from the question literally. NEVER use STRFTIME('now', ...) or any dynamic-date function. Fixed half-open ranges only.\n"
            "Examples:\n"
            "Q: 2026 年 8 月的总销售额\nSQL: SELECT SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0\n"
            "Q: 金卡及以上等级客户占比\nSQL: SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers\n"
            "Q: 最近一次快照中库存低于安全线的 SKU 数量\nSQL: SELECT COUNT(*) AS cnt FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND quantity_available < reorder_level\n"
            "Q: 2026 年 8 月各门店的缺货率\nSQL: SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*) AS stockout_rate FROM inventory_snapshots WHERE snapshot_date >= '2026-08-01' AND snapshot_date < '2026-09-01' GROUP BY store_id\n"
            "Q: 2026 年 8 月的退款率（退款金额占销售额比例）\nSQL: SELECT (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_rate\n"
            "Q: 2026 年 8 月的退款处理平均时长（天数）\nSQL: SELECT AVG(julianday(completed_at) - julianday(requested_at)) AS avg_days FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' AND completed_at IS NOT NULL AND requested_at IS NOT NULL\n"
        )
        prompt = f"{context}\n\nQuestion: {question}"
        response = httpx.post(self.base_url + "/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"}, json={"model": self.model, "temperature": 0, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}, timeout=self.timeout)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r"^```(?:sql)?\s*|\s*```$", "", content, flags=re.I).strip()
        return content
