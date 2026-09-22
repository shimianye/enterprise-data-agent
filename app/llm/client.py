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
    def repair_sql(self, question: str, context: str, previous_sql: str, error: str) -> str: ...

class MockLLMClient:
    def __init__(self, cases_path: str):
        import json
        with open(cases_path, encoding="utf-8") as handle:
            self.cases = {row["question"]: row["golden_sql"] for row in map(json.loads, handle)}
    def generate_sql(self, question: str, context: str) -> str:
        if question not in self.cases:
            raise ValueError("mock model has no golden SQL for this question")
        return self.cases[question]
    def repair_sql(self, question: str, context: str, previous_sql: str, error: str) -> str:
        return self.generate_sql(question, context)

class OpenAICompatibleClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None, timeout: float = 60):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = (base_url or os.getenv("LLM_BASE_URL", "https://api.deepseek.com")).rstrip("/")
        self.model = model or os.getenv("LLM_MODEL", "deepseek-chat")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("LLM_API_KEY is required for the real provider")

    def _request_sql(self, system: str, prompt: str) -> str:
        response = httpx.post(self.base_url + "/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"}, json={"model": self.model, "temperature": 0, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}, timeout=self.timeout)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return re.sub(r"^```(?:sql)?\s*|\s*```$", "", content, flags=re.I).strip()

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
            "16. Result aliases are part of the contract: use the canonical aliases sales, profit, margin, ratio, cnt, ym, growth, mom_growth, yoy_growth, refund_ticket_ratio, high_satisfaction_ratio, available_qty, discount_total, and tier_sales exactly when the question asks that metric. Do not invent aliases such as sales_amount, gross_profit, total_profit, month, or resolution_rate.\n"
            "17. Grain rules: a grouped/store/category/product profit query MUST JOIN order_items and SUM(order_items.subtotal_profit); only a total order-level profit query may SUM(orders.profit_amount). A monthly profit margin also uses order_items.subtotal_profit / order_items.line_paid_amount.\n"
            "18. A customer AOV distribution first computes AVG(paid_amount) per customer in a subquery, then buckets that value; do not bucket individual orders. Repurchase tiers likewise count customers from a grouped customer subquery.\n"
            "19. For month-over-month or year-over-year questions, return the requested difference/rate column only. Use two explicitly filtered CTEs or scalar subqueries when the question asks for a comparison; do not return separate month columns.\n"
            "20. For inventory value or category inventory, join inventory_snapshots to products for product cost/category. Never join order_items as a substitute for products. For promotion names/types, join orders to promotions.\n"
            "21. Use * 1.0 for every ratio or percentage to avoid SQLite integer division. Do not append LIMIT 1000 when the requested shape already defines the result or when it changes a scalar result.\n"
            "Examples:\n"
            "Q: 2026 年 8 月的总销售额\nSQL: SELECT SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0\n"
            "Q: 金卡及以上等级客户占比\nSQL: SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers\n"
            "Q: 最近一次快照中库存低于安全线的 SKU 数量\nSQL: SELECT COUNT(*) AS cnt FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND quantity_available < reorder_level\n"
            "Q: 2026 年 8 月各门店的缺货率\nSQL: SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*) AS stockout_rate FROM inventory_snapshots WHERE snapshot_date >= '2026-08-01' AND snapshot_date < '2026-09-01' GROUP BY store_id\n"
            "Q: 2026 年 8 月的退款率（退款金额占销售额比例）\nSQL: SELECT (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_rate\n"
            "Q: 2026 年 8 月的退款处理平均时长（天数）\nSQL: SELECT AVG(julianday(completed_at) - julianday(requested_at)) AS avg_days FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' AND completed_at IS NOT NULL AND requested_at IS NOT NULL\n"
            "Q: 2026 年 8 月各门店利润\nSQL: SELECT o.store_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY profit DESC\n"
            "Q: 2026 年 8 月各门店销售额环比 7 月\nSQL: SELECT o.store_id, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM orders o WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY mom_growth DESC\n"
            "Q: 2026 年 8 月客单价分段客户数\nSQL: SELECT CASE WHEN avg_aov < 100 THEN '0_100' WHEN avg_aov < 500 THEN '100_500' WHEN avg_aov < 2000 THEN '500_2000' ELSE '2000_plus' END AS bucket, COUNT(*) AS cnt FROM (SELECT customer_id, AVG(paid_amount) AS avg_aov FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY bucket\n"
        )
        prompt = f"{context}\n\nQuestion: {question}"
        return self._request_sql(system, prompt)

    def repair_sql(self, question: str, context: str, previous_sql: str, error: str) -> str:
        system = (
            "You repair one SQLite read-only query. Return exactly one SELECT or WITH statement. "
            "No markdown or explanation. The repaired query must use only the supplied schema and "
            "must address the machine-readable validation or execution error."
        )
        prompt = (
            f"{context}\n\nQuestion: {question}\nPrevious SQL: {previous_sql}\n"
            f"Failure: {error}\nReturn the repaired SQL only."
        )
        return self._request_sql(system, prompt)
