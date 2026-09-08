==============================================================
Text2SQL 评测报告
==============================================================

总题数: 20
SQL 可执行率: 19/20 = 95.0%
结果形状正确率: 18/20 = 90.0%
行数校验通过率: 19/20 = 95.0%
结果正确率: 8/19 = 42.1%

--------------------------------------------------------------
ID    状态    形状   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    2448   sales/easy
Q002  ✓     ✓    ✓    2871   sales/medium
Q003  ✓     ✓    ✓    2746   sales/medium
Q004  ✓     ✓    ✓    2621   sales/medium
Q005  ✓     ✓    ✗    2641   profit/easy
       ↳ 疑似表选错（golden 未用）：['order_items']
Q006  ✓     ✓    ✓    2705   profit/medium
Q007  ✗     ✗    -    0      profit/hard
       ↳ 错误: sql_invalid: ['unknown_column:month', 'unknown_column:sales_amount']
Q008  ✓     ✓    ✓    2446   customer/easy
Q009  ✓     ✓    ✗    2630   customer/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q010  ✓     ✓    ✗    2815   customer/hard
       ↳ 时间字段不一致：golden=['paid_at'] 生成=['created_at']
       ↳ 疑似表选错（golden 未用）：['customer_order_counts']
Q011  ✓     ✓    ✗    2535   inventory/easy
       ↳ 疑似表选错（golden 未用）：['products']
Q012  ✓     ✓    ✗    2304   inventory/medium
       ↳ 疑似表选错（golden 未用）：['products']
Q013  ✓     ✓    ✗    2815   inventory/medium
       ↳ 疑似表选错（golden 未用）：['stores']
Q014  ✓     ✓    ✗    2685   promotion/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q015  ✓     ✓    ✗    2901   promotion/medium
Q016  ✓     ✓    ✓    2311   refund/easy
Q017  ✓     ✓    ✗    2968   refund/medium
       ↳ 时间字段不一致：golden=['completed_at', 'paid_at'] 生成=['paid_at']
Q018  ✓     ✓    ✗    2621   refund/medium
       ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']
       ↳ 聚合函数不一致：golden=['COUNT'] 生成=['COUNT', 'SUM']
Q019  ✓     ✓    ✓    2907   after_sales/medium
Q020  ✓     ✗    ✗    2811   after_sales/medium

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q005】2026 年 8 月的总利润
  golden   : SELECT SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0
  生成     : SELECT COALESCE(SUM(oi.subtotal_profit), 0) AS total_profit FROM order_items AS oi INNER JOIN orders AS o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 LIMIT 1000
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q009】金卡及以上等级客户占比
  golden   : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers
  生成     : SELECT COUNT(DISTINCT CASE WHEN customer_level IN ('金卡', '铂金卡', '钻石卡') THEN customer_id END) * 1.0 / COUNT(DISTINCT customer_id) AS gold_plus_customer_ratio FROM customers LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q010】2026 年 8 月下单次数超过 1 次的客户数
  golden   : SELECT COUNT(*) AS cnt FROM (SELECT customer_id FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id HAVING COUNT(DISTINCT order_id) > 1) AS t
  生成     : WITH customer_order_counts AS (SELECT o.customer_id, COUNT(DISTINCT o.order_id) AS order_count FROM orders AS o WHERE o.paid_amount > 0 AND o.created_at >= '2026-08-01' AND o.created_at < '2026-09-01' GROUP BY o.customer_id HAVING COUNT(DISTINCT o.order_id) > 1) SELECT COUNT(*) AS customer_count FROM customer_order_counts LIMIT 1000
  ↳ 时间字段不一致：golden=['paid_at'] 生成=['created_at']
  ↳ 疑似表选错（golden 未用）：['customer_order_counts']

【Q011】最近一次快照中库存低于安全线的 SKU 数量
  golden   : SELECT COUNT(*) AS cnt FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND quantity_available < reorder_level
  生成     : SELECT COUNT(DISTINCT p.sku_code) AS sku_count FROM inventory_snapshots AS s JOIN products AS p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND s.quantity_available < s.reorder_level LIMIT 1000
  ↳ 疑似表选错（golden 未用）：['products']

【Q012】最近一次快照中库存量最多的 10 个商品
  golden   : SELECT product_id, quantity_on_hand FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) ORDER BY quantity_on_hand DESC LIMIT 10
  生成     : SELECT p.product_id, p.product_name, p.sku_code, p.brand, p.category, s.quantity_available AS inventory_quantity FROM inventory_snapshots AS s JOIN products AS p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) ORDER BY s.quantity_available DESC LIMIT 10
  ↳ 疑似表选错（golden 未用）：['products']

【Q013】2026 年 8 月各门店的缺货率（可用库存为 0 的记录占比）
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*) AS stockout_rate FROM inventory_snapshots WHERE snapshot_date BETWEEN '2026-08-01' AND '2026-08-31' GROUP BY store_id
  生成     : SELECT s.store_id, s.store_name, ROUND(100.0 * SUM(CASE WHEN i.quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS stockout_rate FROM stores AS s LEFT JOIN inventory_snapshots AS i ON s.store_id = i.store_id AND i.snapshot_date >= '2026-08-01' AND i.snapshot_date < '2026-09-01' WHERE s.is_active = 1 GROUP BY s.store_id, s.store_name ORDER BY s.store_id LIMIT 1000
  ↳ 疑似表选错（golden 未用）：['stores']

【Q014】2026 年 8 月使用促销的订单占比
  golden   : SELECT SUM(CASE WHEN promotion_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0
  生成     : SELECT COUNT(DISTINCT CASE WHEN NOT o.promotion_id IS NULL THEN o.order_id END) * 1.0 / COUNT(DISTINCT o.order_id) AS promotion_order_ratio FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q015】2026 年 8 月带来销售额最高的促销活动
  golden   : SELECT p.promotion_name, SUM(o.paid_amount) AS promo_sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY promo_sales DESC LIMIT 1
  生成     : SELECT p.promotion_name, SUM(o.paid_amount) AS sales_amount FROM orders AS o LEFT JOIN promotions AS p ON o.promotion_id = p.promotion_id WHERE o.paid_amount > 0 AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' GROUP BY p.promotion_name ORDER BY sales_amount DESC LIMIT 1

【Q017】2026 年 8 月的退款率（退款金额占销售额比例）
  golden   : SELECT (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_rate
  生成     : SELECT COALESCE(SUM(r.refund_amount), 0) / NULLIF(SUM(o.paid_amount), 0) AS refund_rate FROM orders AS o LEFT JOIN refunds AS r ON o.order_id = r.order_id AND r.refund_status = 'completed' WHERE o.paid_amount > 0 AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' LIMIT 1000
  ↳ 时间字段不一致：golden=['completed_at', 'paid_at'] 生成=['paid_at']

【Q018】2026 年 8 月最常见的退款原因
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE requested_at >= '2026-08-01' AND requested_at < '2026-09-01' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  生成     : SELECT r.refund_reason, COUNT(*) AS refund_count, SUM(r.refund_amount) AS total_refund_amount FROM refunds AS r WHERE r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' GROUP BY r.refund_reason ORDER BY refund_count DESC LIMIT 1
  ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']
  ↳ 聚合函数不一致：golden=['COUNT'] 生成=['COUNT', 'SUM']

【Q020】2026 年 8 月售后工单的解决率（已解决或已关闭占比）
  golden   : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01'
  生成     : SELECT COUNT(*) AS total_tickets, SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) AS resolved_tickets, ROUND(100.0 * SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) / COUNT(*), 2) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000

==============================================================
