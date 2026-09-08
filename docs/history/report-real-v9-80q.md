==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 79/80 = 98.8%
结果结构正确率: 76/80 = 95.0%
结果列名规范率: 17/80 = 21.2%
行数校验通过率: 77/80 = 96.2%
结果正确率: 48/75 = 64.0%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    990    sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q002  ✓     ✓    ✓    1014   sales/medium
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q003  ✓     ✓    ✓    1689   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'sales_volume'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    1080   sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    581    profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    1187   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✓    ✓    1547   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'growth_rate'] 预期=['category', 'growth']
Q008  ✓     ✓    ✓    1213   customer/easy
       ↳ 列名不符（风格/字段）：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✗    879    customer/medium
Q010  ✓     ✓    ✓    1371   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    1148   inventory/easy
Q012  ✓     ✓    ✓    760    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'inventory_quantity'] 预期=['product_id', 'quantity_on_hand']
Q013  ✓     ✓    ✓    1092   inventory/medium
Q014  ✓     ✓    ✓    1230   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✓    ✗    1008   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
       ↳ 表/JOIN 缺失：['promotions']
Q016  ✓     ✓    ✓    1019   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    1148   refund/medium
Q018  ✓     ✓    ✗    917    refund/medium
       ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']
Q019  ✓     ✓    ✓    935    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✓    775    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']
Q021  ✓     ✓    ✓    737    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q022  ✓     ✓    ✓    860    sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    1863   sales/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'sales_amount'] 预期=['product_id', 'sales']
Q024  ✓     ✓    ✓    1215   sales/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'sales_amount'] 预期=['category', 'sales']
Q025  ✓     ✓    ✗    1132   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
       ↳ 表/JOIN 缺失：['stores']
       ↳ 疑似表选错（golden 未用）：['customers']
Q026  ✓     ✓    ✓    1155   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'gross_profit'] 预期=['category', 'profit']
Q027  ✓     ✓    ✓    1890   profit/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'gross_profit'] 预期=['product_id', 'profit']
Q028  ✓     ✓    ✓    1172   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q029  ✓     ✓    ✓    1152   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit'] 预期=['ym', 'profit']
Q030  ✓     ✓    ✓    711    customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'customer_count'] 预期=['customer_level', 'cnt']
Q031  ✓     ✓    ✓    872    customer/easy
       ↳ 列名不符（风格/字段）：实际=['city', 'customer_count'] 预期=['city', 'cnt']
Q032  ✓     ✓    ✓    1594   customer/easy
       ↳ 列名不符（风格/字段）：实际=['new_customer_count'] 预期=['cnt']
Q033  ✓     ✓    ✗    1416   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_rate'] 预期=['ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q034  ✓     ✓    ✗    3562   inventory/medium
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items', 'stores']
Q035  ✓     ✗    ✗    881    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']
Q036  ✓     ✓    ✓    1090   inventory/easy
Q037  ✓     ✓    -    678    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'order_count'] 预期=['promotion_name', 'cnt']
Q038  ✓     ✓    ✓    704    refund/medium
Q039  ✓     ✓    ✓    1265   refund/medium
Q040  ✓     ✓    ✓    512    after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ticket_count'] 预期=['ticket_type', 'cnt']
Q041  ✓     ✓    ✗    1011   sales/easy
       ↳ 列名不符（风格/字段）：实际=['store_id', 'avg_daily_sales'] 预期=['store_id', 'daily_avg_sales']
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']
Q042  ✓     ✓    ✗    1072   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q043  ✓     ✓    ✗    1296   sales/medium
       ↳ 列名不符（风格/字段）：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']
Q044  ✓     ✓    ✗    1467   sales/medium
       ↳ 列名不符（风格/字段）：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
Q045  ✓     ✓    ✓    907    sales/hard
       ↳ 列名不符（风格/字段）：实际=['yoy_growth_rate'] 预期=['yoy_growth']
Q046  ✓     ✓    ✗    1539   sales/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'sales_mom_change'] 预期=['store_id', 'mom_growth']
       ↳ 疑似表选错（golden 未用）：['stores']
Q047  ✓     ✓    ✓    838    sales/easy
       ↳ 列名不符（风格/字段）：实际=['max_order_amount'] 预期=['max_order']
Q048  ✓     ✓    ✓    916    profit/easy
       ↳ 列名不符（风格/字段）：实际=['gross_profit'] 预期=['profit']
Q049  ✓     ✓    ✓    885    profit/medium
Q050  ✓     ✓    ✗    1086   profit/medium
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q051  ✓     ✗    ✗    946    profit/hard
       ↳ 列名不符（风格/字段）：实际=['year', 'total_profit'] 预期=['yoy_profit_growth']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q052  ✓     ✓    ✗    1018   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q053  ✓     ✓    ✓    1002   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'city', 'customer_count'] 预期=['customer_level', 'city', 'cnt']
Q054  ✓     ✓    ✓    806    customer/medium
       ↳ 列名不符（风格/字段）：实际=['paid_customer_count'] 预期=['cnt']
Q055  ✓     ✓    ✗    1487   customer/medium
       ↳ 列名不符（风格/字段）：实际=['segment', 'customer_count'] 预期=['bucket', 'cnt']
       ↳ 聚合函数不一致：golden=['AVG', 'COUNT'] 生成=['COUNT']
Q056  ✓     ✓    ✗    1417   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
Q057  ✗     ✗    -    0      customer/medium
       ↳ 错误: sql_invalid: ['unknown_column:customers.customer_value']
Q058  ✓     ✓    ✓    705    inventory/easy
       ↳ 列名不符（风格/字段）：实际=['total_inventory'] 预期=['total_on_hand']
Q059  ✓     ✓    ✓    875    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'stockout_sku_count'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    705    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✓    865    inventory/hard
       ↳ 列名不符（风格/字段）：实际=['zero_sales_sku_count'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✗    3402   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q063  ✓     ✓    ✗    915    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    803    promotion/easy
       ↳ 列名不符（风格/字段）：实际=['order_count'] 预期=['cnt']
Q065  ✓     ✓    -    1151   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_type', 'sales']
Q066  ✓     ✓    -    722    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
Q067  ✓     ✓    ✗    1025   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']
Q068  ✓     ✗    -    1049   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount', 'gross_profit', 'roi'] 预期=['promotion_type', 'roi']
Q069  ✓     ✓    ✗    1257   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_order_count'] 预期=['cnt']
       ↳ 时间字段不一致：golden=['completed_at'] 生成=['paid_at']
       ↳ 疑似表选错（golden 未用）：['orders']
Q070  ✓     ✓    ✗    1248   refund/medium
       ↳ 列名不符（风格/字段）：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
Q071  ✓     ✓    ✗    1317   refund/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']
Q072  ✓     ✓    ✓    1098   refund/medium
Q073  ✓     ✓    ✗    1137   refund/hard
       ↳ 列名不符（风格/字段）：实际=['after_sales_ticket_rate'] 预期=['ticket_refund_ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q074  ✓     ✓    ✓    933    refund/medium
       ↳ 列名不符（风格/字段）：实际=['week', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✓     ✓    ✓    995    refund/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q076  ✓     ✓    ✓    868    after_sales/easy
Q077  ✓     ✓    ✓    910    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
Q078  ✓     ✓    ✗    649    after_sales/medium
Q079  ✓     ✓    ✗    975    after_sales/hard
       ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['created_at']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
       ↳ 表/JOIN 缺失：['refunds']
       ↳ 事实表混用：退款应读 refunds，不是 after_sales
Q080  ✓     ✓    ✗    1531   after_sales/easy

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q009】金卡及以上等级客户占比
  golden   : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM customers
  生成     : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers LIMIT 1000

【Q015】2026 年 8 月带来销售额最高的促销活动
  golden   : SELECT p.promotion_name, SUM(o.paid_amount) AS promo_sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY promo_sales DESC LIMIT 1
  生成     : SELECT promotion_id, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY promotion_id ORDER BY sales_amount DESC LIMIT 1
  ↳ 列名不符：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
  ↳ 表/JOIN 缺失：['promotions']

【Q018】2026 年 8 月最常见的退款原因
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE requested_at >= '2026-08-01' AND requested_at < '2026-09-01' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  生成     : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']

【Q025】2026 年 8 月长沙各渠道销售额
  golden   : SELECT o.channel, SUM(o.paid_amount) AS sales FROM orders o JOIN stores s ON o.store_id = s.store_id WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel ORDER BY sales DESC
  生成     : SELECT o.channel, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND c.city = '长沙' GROUP BY o.channel LIMIT 1000
  ↳ 列名不符：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
  ↳ 表/JOIN 缺失：['stores']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q033】2026 年 8 月客户复购率
  golden   : SELECT SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id)
  生成     : SELECT COUNT(DISTINCT customer_id) * 1.0 / (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS repurchase_rate FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 AND customer_id IN (SELECT customer_id FROM orders WHERE paid_at < '2026-08-01' AND paid_amount > 0) LIMIT 1000
  ↳ 列名不符：实际=['repurchase_rate'] 预期=['ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q034】最近一次快照各门店库存总金额
  golden   : SELECT inv.store_id, SUM(inv.quantity_on_hand * p.cost_price) AS inventory_value FROM inventory_snapshots inv JOIN products p ON inv.product_id = p.product_id WHERE inv.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY inv.store_id ORDER BY inventory_value DESC
  生成     : SELECT s.store_id, SUM(i.quantity_on_hand * p.unit_cost) AS inventory_value FROM inventory_snapshots AS i JOIN stores AS s ON i.store_id = s.store_id JOIN order_items AS p ON i.product_id = p.product_id WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY s.store_id LIMIT 1000
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
  生成     : SELECT s.store_id, (SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END)) / NULLIF(SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END), 0) AS sales_mom_change FROM orders AS o JOIN stores AS s ON o.store_id = s.store_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY s.store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'sales_mom_change'] 预期=['store_id', 'mom_growth']
  ↳ 疑似表选错（golden 未用）：['stores']

【Q050】2026 年 8 月各门店利润
  golden   : SELECT o.store_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY profit DESC
  生成     : SELECT store_id, SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q051】2026 H1 vs 2025 H1 利润对比
  golden   : SELECT (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-07-01' AND o.paid_amount > 0) - (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2025-07-01' AND o.paid_amount > 0) AS yoy_profit_growth
  生成     : SELECT STRFTIME('%Y', paid_at) AS year, SUM(profit_amount) AS total_profit FROM orders WHERE paid_at >= '2025-01-01' AND paid_at < '2025-07-01' OR paid_at >= '2026-01-01' AND paid_at < '2026-07-01' GROUP BY STRFTIME('%Y', paid_at) ORDER BY year LIMIT 1000
  ↳ 列名不符：实际=['year', 'total_profit'] 预期=['yoy_profit_growth']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q052】近 3 个月各月利润率
  golden   : SELECT strftime('%Y-%m', o.paid_at) AS ym, SUM(oi.subtotal_profit) * 1.0 / SUM(oi.line_paid_amount) AS margin FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-06-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY ym ORDER BY ym
  生成     : SELECT STRFTIME('%Y-%m', o.paid_at) AS month, SUM(o.profit_amount) / SUM(o.paid_amount) AS profit_rate FROM orders AS o WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-04-01' AND o.paid_amount > 0 GROUP BY STRFTIME('%Y-%m', o.paid_at) LIMIT 1000
  ↳ 列名不符：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q055】2026 年 8 月客单价分段客户数
  golden   : SELECT CASE WHEN avg_aov < 100 THEN '0_100' WHEN avg_aov < 500 THEN '100_500' WHEN avg_aov < 2000 THEN '500_2000' ELSE '2000_plus' END AS bucket, COUNT(*) AS cnt FROM (SELECT customer_id, AVG(paid_amount) AS avg_aov FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY bucket
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0-100' WHEN paid_amount < 200 THEN '100-200' WHEN paid_amount < 300 THEN '200-300' ELSE '300+' END AS segment, COUNT(DISTINCT customer_id) AS customer_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY segment LIMIT 1000
  ↳ 列名不符：实际=['segment', 'customer_count'] 预期=['bucket', 'cnt']
  ↳ 聚合函数不一致：golden=['AVG', 'COUNT'] 生成=['COUNT']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : SELECT CASE WHEN repurchase_count BETWEEN 1 AND 3 THEN '1-3' WHEN repurchase_count BETWEEN 4 AND 6 THEN '4-6' ELSE '7+' END AS repurchase_bucket, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) - 1 AS repurchase_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) AS t WHERE repurchase_count >= 1 GROUP BY repurchase_bucket LIMIT 1000
  ↳ 列名不符：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']

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

【Q067】2026 年 8 月促销订单 vs 非促销订单销售额对比
  golden   : SELECT CASE WHEN promotion_id IS NOT NULL THEN 'promo' ELSE 'non_promo' END AS order_type, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type
  生成     : SELECT CASE WHEN NOT promotion_id IS NULL THEN '促销' ELSE '非促销' END AS order_type, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type LIMIT 1000
  ↳ 列名不符：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']

【Q069】2026 年 8 月退款订单数
  golden   : SELECT COUNT(DISTINCT order_id) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed'
  生成     : SELECT COUNT(DISTINCT orders.order_id) AS refund_order_count FROM orders WHERE orders.order_id IN (SELECT order_id FROM refunds WHERE refund_status = 'completed') AND orders.paid_at >= '2026-08-01' AND orders.paid_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['refund_order_count'] 预期=['cnt']
  ↳ 时间字段不一致：golden=['completed_at'] 生成=['paid_at']
  ↳ 疑似表选错（golden 未用）：['orders']

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
  生成     : SELECT ticket_type, SUM(CASE WHEN ticket_status = 'resolved' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type LIMIT 1000

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
