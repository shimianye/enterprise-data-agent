==============================================================
Text2SQL 评测报告
==============================================================

总题数: 20
SQL 可执行率: 20/20 = 100.0%
结果形状正确率: 6/20 = 30.0%
结果列正确率: 6/20 = 30.0%
行数校验通过率: 20/20 = 100.0%
结果正确率: 15/20 = 75.0%

--------------------------------------------------------------
ID    状态    形状   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    2783   sales/easy
Q002  ✓     ✓    ✓    2537   sales/medium
Q003  ✓     ✗    ✓    2612   sales/medium
       ↳ 列不符：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✗    ✓    2264   sales/medium
       ↳ 列不符：实际=['month', 'sales'] 预期=['ym', 'sales']
Q005  ✓     ✗    ✓    2144   profit/easy
       ↳ 列不符：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✗    ✓    2190   profit/medium
       ↳ 列不符：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✗    ✓    2801   profit/hard
       ↳ 列不符：实际=['category', 'growth_rate'] 预期=['category', 'growth']
Q008  ✓     ✗    ✓    2346   customer/easy
       ↳ 列不符：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✓    2318   customer/medium
Q010  ✓     ✗    ✗    2358   customer/hard
       ↳ 列不符：实际=['customer_count'] 预期=['cnt']
       ↳ 时间字段不一致：golden=['paid_at'] 生成=['created_at']
Q011  ✓     ✓    ✓    2077   inventory/easy
Q012  ✓     ✗    ✗    2207   inventory/medium
       ↳ 列不符：实际=['product_name', 'inventory'] 预期=['product_id', 'quantity_on_hand']
       ↳ 疑似表选错（golden 未用）：['products']
Q013  ✓     ✗    ✗    2575   inventory/medium
       ↳ 列不符：实际=['store_id', 'store_name', 'stockout_rate'] 预期=['store_id', 'stockout_rate']
       ↳ 疑似表选错（golden 未用）：['stores']
Q014  ✓     ✗    ✗    2265   promotion/medium
       ↳ 列不符：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✗    ✓    2334   promotion/medium
       ↳ 列不符：实际=['promotion_name', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
Q016  ✓     ✗    ✓    2112   refund/easy
       ↳ 列不符：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    2489   refund/medium
Q018  ✓     ✓    ✓    2155   refund/medium
Q019  ✓     ✗    ✓    2609   after_sales/medium
       ↳ 列不符：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✗    ✗    2103   after_sales/medium
       ↳ 列不符：实际=['resolution_rate'] 预期=['ratio']

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q010】2026 年 8 月下单次数超过 1 次的客户数
  golden   : SELECT COUNT(*) AS cnt FROM (SELECT customer_id FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id HAVING COUNT(DISTINCT order_id) > 1) AS t
  生成     : SELECT COUNT(*) AS customer_count FROM (SELECT customer_id FROM orders WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY customer_id HAVING COUNT(DISTINCT order_id) > 1) AS t LIMIT 1000
  ↳ 列不符：实际=['customer_count'] 预期=['cnt']
  ↳ 时间字段不一致：golden=['paid_at'] 生成=['created_at']

【Q012】最近一次快照中库存量最多的 10 个商品
  golden   : SELECT product_id, quantity_on_hand FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) ORDER BY quantity_on_hand DESC LIMIT 10
  生成     : SELECT p.product_name, s.quantity_available AS inventory FROM inventory_snapshots AS s JOIN products AS p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) ORDER BY s.quantity_available DESC LIMIT 10
  ↳ 列不符：实际=['product_name', 'inventory'] 预期=['product_id', 'quantity_on_hand']
  ↳ 疑似表选错（golden 未用）：['products']

【Q013】2026 年 8 月各门店的缺货率（可用库存为 0 的记录占比）
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*) AS stockout_rate FROM inventory_snapshots WHERE snapshot_date BETWEEN '2026-08-01' AND '2026-08-31' GROUP BY store_id
  生成     : SELECT s.store_id, s.store_name, SUM(CASE WHEN i.quantity_available = 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS stockout_rate FROM inventory_snapshots AS i JOIN stores AS s ON i.store_id = s.store_id WHERE i.snapshot_date >= '2026-08-01' AND i.snapshot_date < '2026-09-01' GROUP BY s.store_id, s.store_name LIMIT 1000
  ↳ 列不符：实际=['store_id', 'store_name', 'stockout_rate'] 预期=['store_id', 'stockout_rate']
  ↳ 疑似表选错（golden 未用）：['stores']

【Q014】2026 年 8 月使用促销的订单占比
  golden   : SELECT SUM(CASE WHEN promotion_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0
  生成     : SELECT SUM(CASE WHEN NOT promotion_id IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS promotion_order_ratio FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 LIMIT 1000
  ↳ 列不符：实际=['promotion_order_ratio'] 预期=['ratio']

【Q020】2026 年 8 月售后工单的解决率（已解决或已关闭占比）
  golden   : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01'
  生成     : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000
  ↳ 列不符：实际=['resolution_rate'] 预期=['ratio']

==============================================================
