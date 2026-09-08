"""Append eval batch 1 (Q021-Q040, 20 new cases) to eval/cases.jsonl.

Batch 1 distribution:
  sales 5 / profit 4 / customer 4 / inventory 3 / promotion 1 / refund 2 / after_sales 1
Difficulty: easy 6 / medium 12 / hard 2

Time anchor: 2026-08 (consistent with Q001-Q020).
Field names strictly aligned with data/init.sql.
Caliber strictly aligned with config/metrics.yaml + Rule 9 (total profit uses orders.profit_amount).
"""
from __future__ import annotations

import json
from pathlib import Path

CASES_PATH = Path("eval/cases.jsonl")

NEW_CASES = [
    # ---------- sales (5) ----------
    {
        "id": "Q021", "category": "sales", "difficulty": "medium",
        "question": "2026 年 Q3 各渠道销售额",
        "business_metric": "销售额",
        "golden_sql": "SELECT channel, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-07-01' AND paid_at < '2026-10-01' AND paid_amount > 0 GROUP BY channel ORDER BY sales DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["channel", "sales"],
        "metric_keywords": ["paid_amount", "SUM", "channel", "paid_amount > 0"],
        "tags": ["time_filter", "group_by", "channel"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q022", "category": "sales", "difficulty": "easy",
        "question": "2026 年 8 月的客单价",
        "business_metric": "客单价",
        "golden_sql": "SELECT AVG(paid_amount) AS aov FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0",
        "expected_shape": "single_value", "expected_result_check": "row_count == 1",
        "expected_columns": ["aov"],
        "metric_keywords": ["paid_amount", "AVG", "paid_amount > 0"],
        "tags": ["time_filter", "aggregation"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q023", "category": "sales", "difficulty": "medium",
        "question": "2026 年 8 月销售额 TOP10 商品",
        "business_metric": "销售额",
        "golden_sql": "SELECT oi.product_id, SUM(oi.line_paid_amount) AS sales FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.product_id ORDER BY sales DESC LIMIT 10",
        "expected_shape": "list", "expected_result_check": "row_count == 10",
        "expected_columns": ["product_id", "sales"],
        "metric_keywords": ["line_paid_amount", "SUM", "JOIN", "paid_amount > 0"],
        "tags": ["time_filter", "join", "top_n", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q024", "category": "sales", "difficulty": "medium",
        "question": "2026 年 8 月各品类销售额",
        "business_metric": "销售额",
        "golden_sql": "SELECT oi.category, SUM(oi.line_paid_amount) AS sales FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY sales DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["category", "sales"],
        "metric_keywords": ["line_paid_amount", "SUM", "category", "paid_amount > 0"],
        "tags": ["time_filter", "join", "group_by", "category"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q025", "category": "sales", "difficulty": "medium",
        "question": "2026 年 8 月长沙各渠道销售额",
        "business_metric": "销售额",
        "golden_sql": "SELECT o.channel, SUM(o.paid_amount) AS sales FROM orders o JOIN stores s ON o.store_id = s.store_id WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel ORDER BY sales DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["channel", "sales"],
        "metric_keywords": ["paid_amount", "SUM", "JOIN", "channel", "city", "paid_amount > 0"],
        "tags": ["time_filter", "region_filter", "join", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- profit (4) ----------
    {
        "id": "Q026", "category": "profit", "difficulty": "medium",
        "question": "2026 年 8 月各品类利润",
        "business_metric": "毛利",
        "golden_sql": "SELECT oi.category, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY profit DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["category", "profit"],
        "metric_keywords": ["subtotal_profit", "SUM", "category", "paid_amount > 0"],
        "tags": ["time_filter", "join", "group_by", "item_level"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q027", "category": "profit", "difficulty": "medium",
        "question": "2026 年 8 月利润 TOP10 商品",
        "business_metric": "毛利",
        "golden_sql": "SELECT oi.product_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.product_id ORDER BY profit DESC LIMIT 10",
        "expected_shape": "list", "expected_result_check": "row_count == 10",
        "expected_columns": ["product_id", "profit"],
        "metric_keywords": ["subtotal_profit", "SUM", "paid_amount > 0"],
        "tags": ["time_filter", "join", "top_n", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q028", "category": "profit", "difficulty": "medium",
        "question": "2026 年 8 月利润率最低的 5 个类目",
        "business_metric": "利润率",
        "golden_sql": "SELECT oi.category, SUM(oi.subtotal_profit) * 1.0 / SUM(oi.line_paid_amount) AS margin FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY margin ASC LIMIT 5",
        "expected_shape": "list", "expected_result_check": "row_count == 5",
        "expected_columns": ["category", "margin"],
        "metric_keywords": ["subtotal_profit", "line_paid_amount", "ratio", "paid_amount > 0"],
        "tags": ["time_filter", "join", "ratio", "bottom_n"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q029", "category": "profit", "difficulty": "medium",
        "question": "2026 年上半年各月利润趋势",
        "business_metric": "毛利",
        "golden_sql": "SELECT strftime('%Y-%m', paid_at) AS ym, SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-01-01' AND paid_at < '2026-07-01' AND paid_amount > 0 GROUP BY ym ORDER BY ym",
        "expected_shape": "time_series", "expected_result_check": "row_count == 6",
        "expected_columns": ["ym", "profit"],
        "metric_keywords": ["profit_amount", "SUM", "strftime", "paid_amount > 0"],
        "tags": ["time_series", "group_by", "strftime"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- customer (4) ----------
    {
        "id": "Q030", "category": "customer", "difficulty": "easy",
        "question": "各等级客户数",
        "business_metric": "客户数",
        "golden_sql": "SELECT customer_level, COUNT(*) AS cnt FROM customers GROUP BY customer_level ORDER BY cnt DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["customer_level", "cnt"],
        "metric_keywords": ["customer_level", "COUNT"],
        "tags": ["group_by", "count"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q031", "category": "customer", "difficulty": "easy",
        "question": "各城市客户数 TOP10",
        "business_metric": "客户数",
        "golden_sql": "SELECT city, COUNT(*) AS cnt FROM customers GROUP BY city ORDER BY cnt DESC LIMIT 10",
        "expected_shape": "list", "expected_result_check": "row_count == 10",
        "expected_columns": ["city", "cnt"],
        "metric_keywords": ["city", "COUNT"],
        "tags": ["group_by", "top_n", "region"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q032", "category": "customer", "difficulty": "easy",
        "question": "2026 年 8 月新增客户数",
        "business_metric": "客户数",
        "golden_sql": "SELECT COUNT(*) AS cnt FROM customers WHERE registered_at >= '2026-08-01' AND registered_at < '2026-09-01'",
        "expected_shape": "single_value", "expected_result_check": "row_count == 1",
        "expected_columns": ["cnt"],
        "metric_keywords": ["registered_at", "COUNT"],
        "tags": ["time_filter", "count"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q033", "category": "customer", "difficulty": "hard",
        "question": "2026 年 8 月客户复购率",
        "business_metric": "复购率",
        "golden_sql": "SELECT SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id)",
        "expected_shape": "single_value", "expected_result_check": "row_count == 1",
        "expected_columns": ["ratio"],
        "metric_keywords": ["COUNT", "DISTINCT", "ratio", "paid_amount > 0"],
        "tags": ["ratio", "subquery", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- inventory (3) ----------
    {
        "id": "Q034", "category": "inventory", "difficulty": "hard",
        "question": "最近一次快照各门店库存总金额",
        "business_metric": "库存金额",
        "golden_sql": "SELECT inv.store_id, SUM(inv.quantity_on_hand * p.cost_price) AS inventory_value FROM inventory_snapshots inv JOIN products p ON inv.product_id = p.product_id WHERE inv.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY inv.store_id ORDER BY inventory_value DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["store_id", "inventory_value"],
        "metric_keywords": ["quantity_on_hand", "cost_price", "JOIN", "snapshot_date"],
        "tags": ["latest_snapshot", "join", "group_by", "computation"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q035", "category": "inventory", "difficulty": "medium",
        "question": "最近一次快照各 SKU 平均可用库存",
        "business_metric": "可用库存",
        "golden_sql": "SELECT product_id, AVG(quantity_available) AS avg_available FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY product_id",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["product_id", "avg_available"],
        "metric_keywords": ["quantity_available", "AVG", "snapshot_date"],
        "tags": ["latest_snapshot", "aggregation", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q036", "category": "inventory", "difficulty": "easy",
        "question": "最近一次快照零在库 SKU 数",
        "business_metric": "零在库 SKU",
        "golden_sql": "SELECT COUNT(*) AS cnt FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND quantity_on_hand = 0",
        "expected_shape": "single_value", "expected_result_check": "row_count == 1",
        "expected_columns": ["cnt"],
        "metric_keywords": ["quantity_on_hand", "COUNT", "snapshot_date"],
        "tags": ["latest_snapshot", "count", "filter"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- promotion (1) ----------
    {
        "id": "Q037", "category": "promotion", "difficulty": "medium",
        "question": "2026 年 8 月各促销活动订单数",
        "business_metric": "促销订单数",
        "golden_sql": "SELECT p.promotion_name, COUNT(DISTINCT o.order_id) AS cnt FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY cnt DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["promotion_name", "cnt"],
        "metric_keywords": ["promotion_id", "COUNT", "DISTINCT", "JOIN", "paid_amount > 0"],
        "tags": ["time_filter", "join", "group_by"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- refund (2) ----------
    {
        "id": "Q038", "category": "refund", "difficulty": "medium",
        "question": "2026 年 8 月各门店退款金额",
        "business_metric": "退款金额",
        "golden_sql": "SELECT o.store_id, SUM(r.refund_amount) AS refund_amount FROM refunds r JOIN orders o ON r.order_id = o.order_id WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed' GROUP BY o.store_id ORDER BY refund_amount DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["store_id", "refund_amount"],
        "metric_keywords": ["refund_amount", "SUM", "JOIN", "refund_status"],
        "tags": ["time_filter", "join", "group_by", "status_filter"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    {
        "id": "Q039", "category": "refund", "difficulty": "medium",
        "question": "2026 年 7 月的退款率",
        "business_metric": "退款率",
        "golden_sql": "SELECT (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-07-01' AND completed_at < '2026-08-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-07-01' AND paid_at < '2026-08-01' AND paid_amount > 0) AS refund_rate",
        "expected_shape": "single_value", "expected_result_check": "row_count == 1",
        "expected_columns": ["refund_rate"],
        "metric_keywords": ["refund_amount", "paid_amount", "scalar_subquery", "paid_amount > 0"],
        "tags": ["scalar_subquery", "ratio", "time_filter"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
    # ---------- after_sales (1) ----------
    {
        "id": "Q040", "category": "after_sales", "difficulty": "easy",
        "question": "2026 年 8 月各类型售后工单数",
        "business_metric": "工单数",
        "golden_sql": "SELECT ticket_type, COUNT(*) AS cnt FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type ORDER BY cnt DESC",
        "expected_shape": "list", "expected_result_check": "row_count >= 1",
        "expected_columns": ["ticket_type", "cnt"],
        "metric_keywords": ["ticket_type", "COUNT"],
        "tags": ["time_filter", "group_by", "count"],
        "eval_metrics": ["sql_executable", "result_correct", "shape_correct", "metric_correct", "e2e"],
    },
]


def main():
    existing = [json.loads(l) for l in CASES_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    existing_ids = {c["id"] for c in existing}
    new_ids = [c["id"] for c in NEW_CASES]
    overlap = existing_ids & set(new_ids)
    if overlap:
        raise SystemExit(f"ID 冲突，已存在于 cases.jsonl: {sorted(overlap)}")
    with CASES_PATH.open("a", encoding="utf-8") as f:
        for c in NEW_CASES:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    total = len(existing) + len(NEW_CASES)
    print(f"原 {len(existing)} 题 + 新 {len(NEW_CASES)} 题 = {total} 题")
    # 分布
    from collections import Counter
    cat = Counter(c["category"] for c in NEW_CASES)
    diff = Counter(c["difficulty"] for c in NEW_CASES)
    print(f"batch1 场景: {dict(cat)}")
    print(f"batch1 难度: {dict(diff)}")


if __name__ == "__main__":
    main()
