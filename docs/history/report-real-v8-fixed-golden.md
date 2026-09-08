==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 79/80 = 98.8%
结果结构正确率: 77/80 = 96.2%
结果列名规范率: 17/80 = 21.2%
行数校验通过率: 77/80 = 96.2%
结果正确率: 49/76 = 64.5%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    985    sales/easy
Q002  ✓     ✓    ✓    888    sales/medium
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q003  ✓     ✓    ✓    1394   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    960    sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    1019   profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    888    profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✓    ✓    1629   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'growth_rate'] 预期=['category', 'growth']
Q008  ✓     ✓    ✓    523    customer/easy
       ↳ 列名不符（风格/字段）：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✗    772    customer/medium
Q010  ✓     ✓    ✓    1080   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    853    inventory/easy
Q012  ✓     ✓    ✓    745    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'inventory_quantity'] 预期=['product_id', 'quantity_on_hand']
Q013  ✓     ✓    ✓    1038   inventory/medium
Q014  ✓     ✓    ✓    700    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✓    ✗    672    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
       ↳ 表/JOIN 缺失：['promotions']
Q016  ✓     ✓    ✓    1038   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    1010   refund/medium
Q018  ✓     ✓    ✗    968    refund/medium
       ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']
Q019  ✓     ✓    ✓    1091   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✓    714    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']
Q021  ✓     ✓    ✓    963    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q022  ✓     ✓    ✓    873    sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    2067   sales/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'sales_amount'] 预期=['product_id', 'sales']
Q024  ✓     ✓    ✗    846    sales/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'sales_amount'] 预期=['category', 'sales']
Q025  ✓     ✓    ✓    976    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q026  ✓     ✓    ✓    745    profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'gross_profit'] 预期=['category', 'profit']
Q027  ✓     ✓    ✓    1362   profit/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'gross_profit'] 预期=['product_id', 'profit']
Q028  ✓     ✓    ✓    1390   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q029  ✓     ✓    ✓    1192   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit'] 预期=['ym', 'profit']
Q030  ✓     ✓    ✓    770    customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'customer_count'] 预期=['customer_level', 'cnt']
Q031  ✓     ✓    ✓    672    customer/easy
       ↳ 列名不符（风格/字段）：实际=['city', 'customer_count'] 预期=['city', 'cnt']
Q032  ✓     ✓    ✓    748    customer/easy
       ↳ 列名不符（风格/字段）：实际=['new_customers'] 预期=['cnt']
Q033  ✓     ✓    ✗    1830   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_rate'] 预期=['ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q034  ✓     ✓    ✗    3952   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'total_inventory_value'] 预期=['store_id', 'inventory_value']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items', 'stores']
Q035  ✓     ✗    ✗    777    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']
Q036  ✓     ✓    ✓    893    inventory/easy
Q037  ✓     ✓    -    1039   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'order_count'] 预期=['promotion_name', 'cnt']
Q038  ✓     ✓    ✓    757    refund/medium
Q039  ✓     ✓    ✓    1040   refund/medium
Q040  ✓     ✓    ✓    978    after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ticket_count'] 预期=['ticket_type', 'cnt']
Q041  ✓     ✓    ✗    1346   sales/easy
       ↳ 列名不符（风格/字段）：实际=['store_id', 'avg_daily_sales'] 预期=['store_id', 'daily_avg_sales']
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']
Q042  ✓     ✓    ✗    798    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q043  ✓     ✓    ✗    1245   sales/medium
       ↳ 列名不符（风格/字段）：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']
Q044  ✓     ✓    ✗    1193   sales/medium
       ↳ 列名不符（风格/字段）：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
Q045  ✓     ✓    ✓    1087   sales/hard
       ↳ 列名不符（风格/字段）：实际=['sales_yoy_ratio'] 预期=['yoy_growth']
Q046  ✓     ✓    ✗    1445   sales/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'mom_change'] 预期=['store_id', 'mom_growth']
       ↳ 疑似表选错（golden 未用）：['stores']
Q047  ✓     ✓    ✓    778    sales/easy
       ↳ 列名不符（风格/字段）：实际=['max_order_amount'] 预期=['max_order']
Q048  ✓     ✓    ✓    1076   profit/easy
       ↳ 列名不符（风格/字段）：实际=['gross_profit'] 预期=['profit']
Q049  ✓     ✓    ✓    791    profit/medium
Q050  ✓     ✓    ✗    768    profit/medium
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q051  ✓     ✗    ✗    1126   profit/hard
       ↳ 列名不符（风格/字段）：实际=['profit_2026_h1', 'profit_2025_h1'] 预期=['yoy_profit_growth']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q052  ✓     ✓    ✗    927    profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q053  ✓     ✓    ✓    804    customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'city', 'customer_count'] 预期=['customer_level', 'city', 'cnt']
Q054  ✓     ✓    ✓    1626   customer/medium
       ↳ 列名不符（风格/字段）：实际=['paid_customer_count'] 预期=['cnt']
Q055  ✗     ✗    -    0      customer/medium
       ↳ 错误: RuntimeError: database query failed: aggregate functions are not allowed in the GROUP BY clause
Q056  ✓     ✓    ✗    1604   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
Q057  ✓     ✓    ✗    1108   customer/medium
       ↳ 列名不符（风格/字段）：实际=['customer_value_segment', 'sales_amount'] 预期=['tier', 'tier_sales']
       ↳ 疑似表选错（golden 未用）：['customers']
Q058  ✓     ✓    ✓    867    inventory/easy
       ↳ 列名不符（风格/字段）：实际=['total_inventory'] 预期=['total_on_hand']
Q059  ✓     ✓    ✓    948    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'stockout_sku_count'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    600    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✓    960    inventory/hard
       ↳ 列名不符（风格/字段）：实际=['zero_sales_sku_count'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✗    3688   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q063  ✓     ✓    ✗    1053   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    704    promotion/easy
       ↳ 列名不符（风格/字段）：实际=['order_count'] 预期=['cnt']
Q065  ✓     ✓    -    1072   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_type', 'sales']
Q066  ✓     ✓    ✗    1120   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
       ↳ 表/JOIN 缺失：['promotions']
Q067  ✓     ✓    ✗    953    promotion/hard
       ↳ 列名不符（风格/字段）：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']
Q068  ✓     ✓    -    934    promotion/hard
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'roi'] 预期=['promotion_type', 'roi']
Q069  ✓     ✓    ✓    812    refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_order_count'] 预期=['cnt']
Q070  ✓     ✓    ✗    972    refund/medium
       ↳ 列名不符（风格/字段）：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
Q071  ✓     ✓    ✗    1485   refund/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']
Q072  ✓     ✓    ✓    763    refund/medium
Q073  ✓     ✓    ✗    1568   refund/hard
       ↳ 列名不符（风格/字段）：实际=['after_sales_ticket_rate'] 预期=['ticket_refund_ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q074  ✓     ✓    ✓    927    refund/medium
       ↳ 列名不符（风格/字段）：实际=['week', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✓     ✓    ✓    953    refund/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q076  ✓     ✓    ✓    644    after_sales/easy
Q077  ✓     ✓    ✓    697    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
Q078  ✓     ✓    ✗    669    after_sales/medium
Q079  ✓     ✓    ✗    921    after_sales/hard
       ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['created_at']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
       ↳ 表/JOIN 缺失：['refunds']
       ↳ 事实表混用：退款应读 refunds，不是 after_sales
Q080  ✓     ✓    ✗    837    after_sales/easy

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q009】金卡及以上等级客户占比
  golden   : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM customers
  生成     : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers LIMIT 1000

【Q015】2026 年 8 月带来销售额最高的促销活动
  golden   : SELECT p.promotion_name, SUM(o.paid_amount) AS promo_sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY promo_sales DESC LIMIT 1
  生成     : SELECT orders.promotion_id, SUM(orders.paid_amount) AS sales_amount FROM orders WHERE orders.paid_at >= '2026-08-01' AND orders.paid_at < '2026-09-01' AND orders.paid_amount > 0 GROUP BY orders.promotion_id ORDER BY sales_amount DESC LIMIT 1
  ↳ 列名不符：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
  ↳ 表/JOIN 缺失：['promotions']

【Q018】2026 年 8 月最常见的退款原因
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE requested_at >= '2026-08-01' AND requested_at < '2026-09-01' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  生成     : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']

【Q024】2026 年 8 月各品类销售额
  golden   : SELECT oi.category, SUM(oi.line_paid_amount) AS sales FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY sales DESC
  生成     : SELECT oi.category, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN order_items AS oi ON o.order_id = oi.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'sales_amount'] 预期=['category', 'sales']

【Q033】2026 年 8 月客户复购率
  golden   : SELECT SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id)
  生成     : SELECT COUNT(DISTINCT o.customer_id) * 1.0 / (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS repurchase_rate FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND o.customer_id IN (SELECT customer_id FROM orders WHERE paid_at < '2026-08-01' AND paid_amount > 0) LIMIT 1000
  ↳ 列名不符：实际=['repurchase_rate'] 预期=['ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q034】最近一次快照各门店库存总金额
  golden   : SELECT inv.store_id, SUM(inv.quantity_on_hand * p.cost_price) AS inventory_value FROM inventory_snapshots inv JOIN products p ON inv.product_id = p.product_id WHERE inv.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY inv.store_id ORDER BY inventory_value DESC
  生成     : SELECT s.store_id, SUM(i.quantity_on_hand * p.unit_cost) AS total_inventory_value FROM inventory_snapshots AS i JOIN stores AS s ON i.store_id = s.store_id JOIN order_items AS p ON i.product_id = p.product_id WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY s.store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'total_inventory_value'] 预期=['store_id', 'inventory_value']
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items', 'stores']

【Q035】最近一次快照各 SKU 平均可用库存
  golden   : SELECT product_id, AVG(quantity_available) AS avg_available FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY product_id
  生成     : SELECT AVG(quantity_available) AS avg_available_stock FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) LIMIT 1000
  ↳ 列名不符：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']

【Q041】2026 年 8 月各门店日均销售额
  golden   : SELECT store_id, SUM(paid_amount) * 1.0 / 31 AS daily_avg_sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id ORDER BY daily_avg_sales DESC
  生成     : SELECT store_id, SUM(paid_amount) / COUNT(DISTINCT STRFTIME('%Y-%m-%d', paid_at)) AS avg_daily_sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'avg_daily_sales'] 预期=['store_id', 'daily_avg_sales']
  ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']

【Q042】2026 年 8 月线上 vs 线下销售额对比
  golden   : SELECT channel, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY channel
  生成     : SELECT CASE WHEN channel = '线上' THEN '线上' ELSE '线下' END AS channel, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY CASE WHEN channel = '线上' THEN '线上' ELSE '线下' END LIMIT 1000
  ↳ 列名不符：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']

【Q043】2026 年 8 月订单金额分布
  golden   : SELECT CASE WHEN paid_amount < 100 THEN 'under_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE 'over_2000' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket ORDER BY MIN(paid_amount)
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0-100' WHEN paid_amount < 500 THEN '100-500' WHEN paid_amount < 1000 THEN '500-1000' WHEN paid_amount < 5000 THEN '1000-5000' ELSE '5000+' END AS amount_range, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY amount_range ORDER BY MIN(paid_amount) LIMIT 1000
  ↳ 列名不符：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']

【Q044】近一年新客与老客销售额对比
  golden   : SELECT CASE WHEN c.registered_at >= '2024-08-01' THEN 'new' ELSE 'existing' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-08-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY customer_type
  生成     : SELECT CASE WHEN c.customer_level IN ('金卡', '铂金') THEN '老客' ELSE '新客' END AS customer_type, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2026-01-01' AND o.paid_amount > 0 GROUP BY customer_type LIMIT 1000
  ↳ 列名不符：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
  ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']

【Q046】2026 年 8 月各门店销售额环比 7 月
  golden   : SELECT o.store_id, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM orders o WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY mom_growth DESC
  生成     : SELECT s.store_id, (SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END)) / NULLIF(SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END), 0) AS mom_change FROM orders AS o JOIN stores AS s ON o.store_id = s.store_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY s.store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'mom_change'] 预期=['store_id', 'mom_growth']
  ↳ 疑似表选错（golden 未用）：['stores']

【Q050】2026 年 8 月各门店利润
  golden   : SELECT o.store_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY profit DESC
  生成     : SELECT store_id, SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q051】2026 H1 vs 2025 H1 利润对比
  golden   : SELECT (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-07-01' AND o.paid_amount > 0) - (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2025-07-01' AND o.paid_amount > 0) AS yoy_profit_growth
  生成     : SELECT SUM(CASE WHEN paid_at >= '2026-01-01' AND paid_at < '2026-07-01' THEN profit_amount ELSE 0 END) AS profit_2026_h1, SUM(CASE WHEN paid_at >= '2025-01-01' AND paid_at < '2025-07-01' THEN profit_amount ELSE 0 END) AS profit_2025_h1 FROM orders WHERE paid_at >= '2025-01-01' AND paid_at < '2026-07-01' AND paid_amount > 0 LIMIT 1000
  ↳ 列名不符：实际=['profit_2026_h1', 'profit_2025_h1'] 预期=['yoy_profit_growth']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q052】近 3 个月各月利润率
  golden   : SELECT strftime('%Y-%m', o.paid_at) AS ym, SUM(oi.subtotal_profit) * 1.0 / SUM(oi.line_paid_amount) AS margin FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-06-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY ym ORDER BY ym
  生成     : SELECT STRFTIME('%Y-%m', o.paid_at) AS month, SUM(o.profit_amount) / SUM(o.paid_amount) AS profit_rate FROM orders AS o WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-04-01' AND o.paid_amount > 0 GROUP BY STRFTIME('%Y-%m', o.paid_at) LIMIT 1000
  ↳ 列名不符：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : SELECT CASE WHEN repurchase_count BETWEEN 1 AND 3 THEN '1-3' WHEN repurchase_count BETWEEN 4 AND 6 THEN '4-6' ELSE '7+' END AS repurchase_bucket, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) - 1 AS repurchase_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) AS t WHERE repurchase_count >= 1 GROUP BY repurchase_bucket LIMIT 1000
  ↳ 列名不符：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']

【Q057】2026 年 8 月高、中、低价值客户的销售额贡献
  golden   : SELECT CASE WHEN total_spend >= 5000 THEN 'high' WHEN total_spend >= 1000 THEN 'mid' ELSE 'low' END AS tier, SUM(total_spend) AS tier_sales FROM (SELECT customer_id, SUM(paid_amount) AS total_spend FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY tier ORDER BY tier_sales DESC
  生成     : SELECT CASE WHEN c.customer_level IN ('高价值', 'VIP', '金卡', '铂金') THEN '高价值' WHEN c.customer_level IN ('中价值', '银卡') THEN '中价值' ELSE '低价值' END AS customer_value_segment, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY customer_value_segment LIMIT 1000
  ↳ 列名不符：实际=['customer_value_segment', 'sales_amount'] 预期=['tier', 'tier_sales']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q062】最近一次快照各品类可销库存量
  golden   : SELECT p.category, SUM(s.quantity_available) AS available_qty FROM inventory_snapshots s JOIN products p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category ORDER BY available_qty DESC
  生成     : SELECT category, SUM(quantity_available) AS available_stock FROM inventory_snapshots JOIN order_items ON inventory_snapshots.product_id = order_items.product_id WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY category LIMIT 1000
  ↳ 列名不符：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q063】最近一次快照各门店安全线达标率
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pass_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id ORDER BY pass_rate DESC
  生成     : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) / COUNT(*) AS compliance_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']

【Q066】2026 年 8 月各促销活动优惠总额
  golden   : SELECT p.promotion_name, SUM(o.discount_amount) AS discount_total FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY discount_total DESC
  生成     : SELECT o.promotion_id, SUM(o.discount_amount) AS total_discount FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND NOT o.promotion_id IS NULL GROUP BY o.promotion_id LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
  ↳ 表/JOIN 缺失：['promotions']

【Q067】2026 年 8 月促销订单 vs 非促销订单销售额对比
  golden   : SELECT CASE WHEN promotion_id IS NOT NULL THEN 'promo' ELSE 'non_promo' END AS order_type, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type
  生成     : SELECT CASE WHEN NOT promotion_id IS NULL THEN '促销' ELSE '非促销' END AS order_type, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type LIMIT 1000
  ↳ 列名不符：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']

【Q070】2026 年 8 月各退款原因占比
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC
  生成     : SELECT refund_reason, COUNT(*) * 1.0 / (SELECT COUNT(*) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') AS ratio FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason LIMIT 1000
  ↳ 列名不符：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']

【Q071】2026 年 8 月各品类退款率
  golden   : SELECT t.category, SUM(CASE WHEN t.refund_amount IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_rate FROM (SELECT oi.category, r.refund_amount FROM order_items oi JOIN orders o ON oi.order_id = o.order_id LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0) t GROUP BY t.category ORDER BY refund_rate DESC
  生成     : SELECT oi.category, (SELECT SUM(r.refund_amount) FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed') / (SELECT SUM(oi2.line_paid_amount) FROM order_items AS oi2 JOIN orders AS o2 ON oi2.order_id = o2.order_id WHERE o2.paid_at >= '2026-08-01' AND o2.paid_at < '2026-09-01' AND o2.paid_amount > 0) AS refund_rate FROM order_items AS oi GROUP BY oi.category LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']

【Q073】2026 年 8 月有退款订单的售后工单率
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ticket_refund_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT (SELECT COUNT(DISTINCT a.order_id) FROM after_sales AS a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01' AND a.order_id IN (SELECT DISTINCT r.order_id FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed')) * 1.0 / (SELECT COUNT(DISTINCT r.order_id) FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed') AS after_sales_ticket_rate LIMIT 1000
  ↳ 列名不符：实际=['after_sales_ticket_rate'] 预期=['ticket_refund_ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q078】2026 年 8 月各工单类型解决率
  golden   : SELECT ticket_type, SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type ORDER BY resolution_rate DESC
  生成     : SELECT ticket_type, SUM(CASE WHEN ticket_status = 'resolved' THEN 1 ELSE 0 END) / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type LIMIT 1000

【Q079】2026 年 8 月涉及退款的工单占比
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_ticket_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT (SELECT COUNT(DISTINCT order_id) FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND ticket_type = '退款') * 1.0 / (SELECT COUNT(DISTINCT order_id) FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01') AS refund_ticket_ratio LIMIT 1000
  ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['created_at']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
  ↳ 表/JOIN 缺失：['refunds']
  ↳ 事实表混用：退款应读 refunds，不是 after_sales

【Q080】2026 年 8 月高满意度工单占比
  golden   : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND satisfaction_score IS NOT NULL
  生成     : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000

==============================================================
