==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 80/80 = 100.0%
结果结构正确率: 80/80 = 100.0%
结果列名规范率: 56/80 = 70.0%
行数校验通过率: 79/80 = 98.8%
结果正确率: 69/80 = 86.2%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    2592   sales/easy
Q002  ✓     ✓    ✓    2389   sales/medium
Q003  ✓     ✓    ✓    2285   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'cnt'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    2439   sales/medium
Q005  ✓     ✓    ✓    2013   profit/easy
Q006  ✓     ✓    ✓    2107   profit/medium
Q007  ✓     ✓    ✗    2544   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'mom_growth'] 预期=['category', 'growth']
       ↳ 表/JOIN 缺失：['aug', 'jul']
Q008  ✓     ✓    ✓    1999   customer/easy
Q009  ✓     ✓    ✓    1850   customer/medium
Q010  ✓     ✓    ✓    2385   customer/hard
Q011  ✓     ✓    ✓    1948   inventory/easy
Q012  ✓     ✓    ✓    1822   inventory/medium
Q013  ✓     ✓    ✗    2212   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'ratio'] 预期=['store_id', 'stockout_rate']
Q014  ✓     ✓    ✓    2213   promotion/medium
Q015  ✓     ✓    ✓    2272   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_name', 'sales'] 预期=['promotion_name', 'promo_sales']
Q016  ✓     ✓    ✓    1743   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    2361   refund/medium
       ↳ 列名不符（风格/字段）：实际=['ratio'] 预期=['refund_rate']
Q018  ✓     ✓    ✓    1843   refund/medium
Q019  ✓     ✓    ✓    2230   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✓    1998   after_sales/medium
Q021  ✓     ✓    ✓    1976   sales/medium
Q022  ✓     ✓    ✓    2668   sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    3455   sales/medium
Q024  ✓     ✓    ✓    2062   sales/medium
Q025  ✓     ✓    ✓    2042   sales/medium
Q026  ✓     ✓    ✓    2009   profit/medium
Q027  ✓     ✓    ✓    3470   profit/medium
Q028  ✓     ✓    ✓    2175   profit/medium
Q029  ✓     ✓    ✗    2481   profit/medium
       ↳ 疑似表选错（golden 未用）：['order_items']
Q030  ✓     ✓    ✓    1882   customer/easy
Q031  ✓     ✓    ✓    2054   customer/easy
Q032  ✓     ✓    ✓    2045   customer/easy
Q033  ✓     ✓    ✓    2624   customer/hard
Q034  ✓     ✓    ✗    7083   inventory/medium
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q035  ✓     ✓    ✓    1762   inventory/medium
Q036  ✓     ✓    ✓    2053   inventory/easy
Q037  ✓     ✓    ✗    2465   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'cnt'] 预期=['promotion_name', 'cnt']
       ↳ 表/JOIN 缺失：['promotions']
Q038  ✓     ✓    ✓    2249   refund/medium
Q039  ✓     ✓    ✓    2301   refund/medium
       ↳ 列名不符（风格/字段）：实际=['ratio'] 预期=['refund_rate']
Q040  ✓     ✓    ✓    2143   after_sales/easy
Q041  ✓     ✓    ✓    2291   sales/easy
       ↳ 列名不符（风格/字段）：实际=['store_id', 'sales'] 预期=['store_id', 'daily_avg_sales']
Q042  ✓     ✓    ✓    2213   sales/medium
Q043  ✓     ✓    ✗    2179   sales/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']
Q044  ✓     ✓    ✗    2484   sales/medium
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['MIN', 'SUM']
       ↳ 表/JOIN 缺失：['customers']
       ↳ 疑似表选错（golden 未用）：['customer_first_order']
Q045  ✓     ✓    ✓    2477   sales/hard
Q046  ✓     ✓    ✓    2520   sales/medium
Q047  ✓     ✓    ✓    2030   sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales'] 预期=['max_order']
Q048  ✓     ✓    ✓    2044   profit/easy
Q049  ✓     ✓    ✓    2319   profit/medium
Q050  ✓     ✓    ✓    1992   profit/medium
Q051  ✓     ✓    ✓    2052   profit/hard
       ↳ 列名不符（风格/字段）：实际=['growth'] 预期=['yoy_profit_growth']
Q052  ✓     ✓    ✓    2163   profit/medium
Q053  ✓     ✓    ✓    2005   customer/easy
Q054  ✓     ✓    ✓    2475   customer/medium
Q055  ✓     ✓    ✓    2492   customer/medium
Q056  ✓     ✓    ✗    2606   customer/hard
       ↳ 列名不符（风格/字段）：实际=['bucket', 'cnt'] 预期=['repurchase_tier', 'customer_count']
Q057  ✓     ✓    ✗    2380   customer/medium
       ↳ 列名不符（风格/字段）：实际=['tier', 'sales'] 预期=['tier', 'tier_sales']
       ↳ 疑似表选错（golden 未用）：['customers']
Q058  ✓     ✓    ✓    2249   inventory/easy
Q059  ✓     ✓    ✓    1948   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'cnt'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    2097   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✓    2890   inventory/hard
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✓    2099   inventory/medium
Q063  ✓     ✓    ✓    2179   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'ratio'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    1906   promotion/easy
Q065  ✓     ✓    ✓    2230   promotion/medium
Q066  ✓     ✓    ✓    2245   promotion/medium
Q067  ✓     ✓    ✓    2256   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['promotion_flag', 'sales'] 预期=['order_type', 'sales']
Q068  ✓     ✓    ✓    2347   promotion/hard
Q069  ✓     ✓    ✓    1946   refund/easy
Q070  ✓     ✓    ✗    1938   refund/medium
       ↳ 列名不符（风格/字段）：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
Q071  ✓     ✓    ✓    2378   refund/medium
Q072  ✓     ✓    ✓    2283   refund/medium
Q073  ✓     ✓    ✓    2488   refund/hard
       ↳ 列名不符（风格/字段）：实际=['refund_ticket_ratio'] 预期=['ticket_refund_ratio']
Q074  ✓     ✓    ✓    2153   refund/medium
       ↳ 列名不符（风格/字段）：实际=['ym', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✓     ✓    ✓    2347   refund/hard
Q076  ✓     ✓    ✓    2194   after_sales/easy
Q077  ✓     ✓    ✓    1964   after_sales/medium
Q078  ✓     ✓    ✓    2025   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ratio'] 预期=['ticket_type', 'resolution_rate']
Q079  ✓     ✓    ✓    2468   after_sales/hard
Q080  ✓     ✓    ✗    1793   after_sales/easy

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q007】2026 年 8 月相比 7 月，销售额环比增长最快的类目
  golden   : WITH aug AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY category), jul AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY category) SELECT aug.category, (aug.s - jul.s) / jul.s AS growth FROM aug JOIN jul ON aug.category = jul.category WHERE jul.s > 0 ORDER BY growth DESC LIMIT 1
  生成     : SELECT oi.category, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY mom_growth DESC LIMIT 1
  ↳ 列名不符：实际=['category', 'mom_growth'] 预期=['category', 'growth']
  ↳ 表/JOIN 缺失：['aug', 'jul']

【Q013】2026 年 8 月各门店的缺货率（可用库存为 0 的记录占比）
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) / COUNT(*) AS stockout_rate FROM inventory_snapshots WHERE snapshot_date BETWEEN '2026-08-01' AND '2026-08-31' GROUP BY store_id
  生成     : SELECT store_id, SUM(CASE WHEN quantity_available = 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM inventory_snapshots WHERE snapshot_date >= '2026-08-01' AND snapshot_date < '2026-09-01' GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'ratio'] 预期=['store_id', 'stockout_rate']

【Q029】2026 年上半年各月利润趋势
  golden   : SELECT strftime('%Y-%m', paid_at) AS ym, SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-01-01' AND paid_at < '2026-07-01' AND paid_amount > 0 GROUP BY ym ORDER BY ym
  生成     : SELECT STRFTIME('%Y-%m', o.paid_at) AS ym, SUM(oi.subtotal_profit) AS profit FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-07-01' AND o.paid_amount > 0 GROUP BY ym ORDER BY ym LIMIT 1000
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q034】最近一次快照各门店库存总金额
  golden   : SELECT inv.store_id, SUM(inv.quantity_on_hand * p.cost_price) AS inventory_value FROM inventory_snapshots inv JOIN products p ON inv.product_id = p.product_id WHERE inv.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY inv.store_id ORDER BY inventory_value DESC
  生成     : SELECT i.store_id, SUM(i.quantity_on_hand * oi.unit_cost) AS inventory_value FROM inventory_snapshots AS i JOIN order_items AS oi ON i.product_id = oi.product_id WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY i.store_id LIMIT 1000
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q037】2026 年 8 月各促销活动订单数
  golden   : SELECT p.promotion_name, COUNT(DISTINCT o.order_id) AS cnt FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY cnt DESC
  生成     : SELECT o.promotion_id, COUNT(DISTINCT o.order_id) AS cnt FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND NOT o.promotion_id IS NULL GROUP BY o.promotion_id ORDER BY cnt DESC LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'cnt'] 预期=['promotion_name', 'cnt']
  ↳ 表/JOIN 缺失：['promotions']

【Q043】2026 年 8 月订单金额分布
  golden   : SELECT CASE WHEN paid_amount < 100 THEN 'under_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE 'over_2000' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket ORDER BY MIN(paid_amount)
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE '2000_plus' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']

【Q044】近一年新客与老客销售额对比
  golden   : SELECT CASE WHEN c.registered_at >= '2024-08-01' THEN 'new' ELSE 'existing' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-08-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY customer_type
  生成     : WITH customer_first_order AS (SELECT customer_id, MIN(paid_at) AS first_paid_at FROM orders WHERE paid_amount > 0 GROUP BY customer_id) SELECT CASE WHEN cfo.first_paid_at >= '2025-01-01' THEN 'new' ELSE 'old' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders AS o JOIN customer_first_order AS cfo ON o.customer_id = cfo.customer_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2026-01-01' AND o.paid_amount > 0 GROUP BY customer_type LIMIT 1000
  ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
  ↳ 聚合函数不一致：golden=['SUM'] 生成=['MIN', 'SUM']
  ↳ 表/JOIN 缺失：['customers']
  ↳ 疑似表选错（golden 未用）：['customer_first_order']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : SELECT CASE WHEN t.cnt <= 3 THEN '1-3' WHEN t.cnt <= 6 THEN '4-6' ELSE '7+' END AS bucket, COUNT(*) AS cnt FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) AS t GROUP BY bucket LIMIT 1000
  ↳ 列名不符：实际=['bucket', 'cnt'] 预期=['repurchase_tier', 'customer_count']

【Q057】2026 年 8 月高、中、低价值客户的销售额贡献
  golden   : SELECT CASE WHEN total_spend >= 5000 THEN 'high' WHEN total_spend >= 1000 THEN 'mid' ELSE 'low' END AS tier, SUM(total_spend) AS tier_sales FROM (SELECT customer_id, SUM(paid_amount) AS total_spend FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY tier ORDER BY tier_sales DESC
  生成     : SELECT CASE WHEN c.customer_level IN ('金卡', '铂金') THEN 'high' WHEN c.customer_level = '银卡' THEN 'mid' ELSE 'low' END AS tier, SUM(o.paid_amount) AS sales FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY tier ORDER BY sales DESC LIMIT 1000
  ↳ 列名不符：实际=['tier', 'sales'] 预期=['tier', 'tier_sales']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q070】2026 年 8 月各退款原因占比
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC
  生成     : SELECT refund_reason, COUNT(*) * 1.0 / (SELECT COUNT(*) FROM refunds WHERE refund_status = 'completed' AND completed_at >= '2026-08-01' AND completed_at < '2026-09-01') AS ratio FROM refunds WHERE refund_status = 'completed' AND completed_at >= '2026-08-01' AND completed_at < '2026-09-01' GROUP BY refund_reason LIMIT 1000
  ↳ 列名不符：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']

【Q080】2026 年 8 月高满意度工单占比
  golden   : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND satisfaction_score IS NOT NULL
  生成     : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000

==============================================================
