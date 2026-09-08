==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 75/80 = 93.8%
结果结构正确率: 72/80 = 90.0%
结果列名规范率: 13/80 = 16.2%
行数校验通过率: 73/80 = 91.2%
结果正确率: 47/73 = 64.4%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    1228   sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q002  ✓     ✓    ✓    1169   sales/medium
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q003  ✓     ✓    ✓    1370   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    781    sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    959    profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    1368   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✓    ✓    1748   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'growth_rate'] 预期=['category', 'growth']
Q008  ✓     ✓    ✓    907    customer/easy
       ↳ 列名不符（风格/字段）：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✓    1004   customer/medium
Q010  ✓     ✓    ✓    1598   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    956    inventory/easy
Q012  ✓     ✓    ✓    1196   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'inventory_quantity'] 预期=['product_id', 'quantity_on_hand']
Q013  ✓     ✓    ✓    1113   inventory/medium
Q014  ✓     ✓    ✓    1143   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✓    ✗    987    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
       ↳ 表/JOIN 缺失：['promotions']
Q016  ✓     ✓    ✓    1318   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    1690   refund/medium
Q018  ✓     ✓    ✓    805    refund/medium
Q019  ✓     ✓    ✓    1122   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✓    752    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']
Q021  ✓     ✓    ✓    766    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q022  ✓     ✓    ✓    1163   sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    1952   sales/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'sales_amount'] 预期=['product_id', 'sales']
Q024  ✓     ✓    ✗    1382   sales/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'sales_amount'] 预期=['category', 'sales']
Q025  ✓     ✓    ✗    1274   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
       ↳ 表/JOIN 缺失：['stores']
       ↳ 疑似表选错（golden 未用）：['customers']
Q026  ✓     ✓    ✓    1337   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'gross_profit'] 预期=['category', 'profit']
Q027  ✓     ✓    ✓    1759   profit/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'gross_profit'] 预期=['product_id', 'profit']
Q028  ✓     ✓    ✓    1181   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q029  ✓     ✓    ✓    1373   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'gross_profit'] 预期=['ym', 'profit']
Q030  ✓     ✓    ✓    513    customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'customer_count'] 预期=['customer_level', 'cnt']
Q031  ✓     ✓    ✓    1008   customer/easy
       ↳ 列名不符（风格/字段）：实际=['city', 'customer_count'] 预期=['city', 'cnt']
Q032  ✓     ✓    ✓    851    customer/easy
       ↳ 列名不符（风格/字段）：实际=['new_customer_count'] 预期=['cnt']
Q033  ✓     ✓    ✗    2056   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_rate'] 预期=['ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q034  ✓     ✓    ✗    5423   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'total_inventory_value'] 预期=['store_id', 'inventory_value']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items', 'stores']
Q035  ✓     ✗    ✗    717    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']
Q036  ✓     ✓    ✓    1084   inventory/easy
Q037  ✓     ✓    -    857    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'order_count'] 预期=['promotion_name', 'cnt']
Q038  ✗     ✗    -    0      refund/medium
       ↳ 错误: sql_invalid: ['unknown_column:store_id']
Q039  ✓     ✓    ✓    1056   refund/medium
Q040  ✓     ✓    ✓    1072   after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ticket_count'] 预期=['ticket_type', 'cnt']
Q041  ✓     ✓    ✗    1279   sales/easy
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']
Q042  ✓     ✗    ✗    750    sales/medium
       ↳ 列名不符（风格/字段）：实际=[] 预期=['channel', 'sales']
Q043  ✓     ✓    ✗    1198   sales/medium
       ↳ 列名不符（风格/字段）：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']
Q044  ✓     ✓    ✗    1468   sales/medium
       ↳ 列名不符（风格/字段）：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
Q045  ✓     ✓    ✓    1245   sales/hard
       ↳ 列名不符（风格/字段）：实际=['sales_yoy_ratio'] 预期=['yoy_growth']
Q046  ✓     ✓    ✗    1965   sales/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'sales_mom_change'] 预期=['store_id', 'mom_growth']
Q047  ✓     ✓    ✓    643    sales/easy
       ↳ 列名不符（风格/字段）：实际=['max_order_amount'] 预期=['max_order']
Q048  ✓     ✓    ✓    1213   profit/easy
       ↳ 列名不符（风格/字段）：实际=['gross_profit'] 预期=['profit']
Q049  ✓     ✓    ✓    1229   profit/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'gross_profit'] 预期=['brand', 'profit']
Q050  ✓     ✓    ✗    809    profit/medium
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q051  ✗     ✗    -    0      profit/hard
       ↳ 错误: sql_invalid: ['unknown_column:total_profit']
Q052  ✓     ✓    ✗    1409   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
Q053  ✓     ✓    ✓    1090   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'city', 'customer_count'] 预期=['customer_level', 'city', 'cnt']
Q054  ✓     ✓    ✓    1593   customer/medium
       ↳ 列名不符（风格/字段）：实际=['paid_customer_count'] 预期=['cnt']
Q055  ✗     ✗    -    0      customer/medium
       ↳ 错误: RuntimeError: database query failed: aggregate functions are not allowed in the GROUP BY clause
Q056  ✓     ✓    ✗    1876   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_group', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
       ↳ 聚合去重缺失：应 COUNT(DISTINCT ...)
       ↳ 聚合函数不一致：golden=['COUNT'] 生成=['COUNT', 'MIN']
Q057  ✓     ✓    ✗    1349   customer/medium
       ↳ 列名不符（风格/字段）：实际=['customer_value_segment', 'sales_amount'] 预期=['tier', 'tier_sales']
       ↳ 疑似表选错（golden 未用）：['customers']
Q058  ✓     ✓    ✓    902    inventory/easy
       ↳ 列名不符（风格/字段）：实际=['total_inventory'] 预期=['total_on_hand']
Q059  ✓     ✓    ✓    1037   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'stockout_sku_count'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    825    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✓    1438   inventory/hard
       ↳ 列名不符（风格/字段）：实际=['zero_sales_sku_count'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✗    4378   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q063  ✓     ✓    ✗    1178   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    1174   promotion/easy
       ↳ 列名不符（风格/字段）：实际=['order_count'] 预期=['cnt']
Q065  ✓     ✓    ✗    1302   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_type', 'sales_amount'] 预期=['promotion_type', 'sales']
       ↳ 表/JOIN 缺失：['promotions']
Q066  ✓     ✓    ✗    1191   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
       ↳ 表/JOIN 缺失：['promotions']
Q067  ✓     ✓    ✗    1115   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']
Q068  ✓     ✗    -    1014   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount', 'gross_profit', 'roi'] 预期=['promotion_type', 'roi']
Q069  ✓     ✓    ✓    1522   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_order_count'] 预期=['cnt']
Q070  ✗     ✗    -    0      refund/medium
       ↳ 错误: sql_invalid: ['unknown_column:reason']
Q071  ✓     ✓    ✗    27999  refund/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']
Q072  ✓     ✓    ✗    1210   refund/medium
       ↳ 列名不符（风格/字段）：实际=['avg_refund_processing_hours'] 预期=['avg_days']
       ↳ 时间字段不一致：golden=['completed_at', 'requested_at'] 生成=['created_at']
       ↳ 表/JOIN 缺失：['refunds']
       ↳ 疑似表选错（golden 未用）：['after_sales']
       ↳ 事实表混用：退款应读 refunds，不是 after_sales
Q073  ✓     ✓    ✗    1699   refund/hard
       ↳ 列名不符（风格/字段）：实际=['after_sales_rate'] 预期=['ticket_refund_ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q074  ✓     ✓    ✓    1256   refund/medium
       ↳ 列名不符（风格/字段）：实际=['week', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✗     ✗    -    0      refund/hard
       ↳ 错误: sql_invalid: ['unknown_column:customer_id']
Q076  ✓     ✓    ✓    1017   after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_status', 'ticket_count'] 预期=['ticket_status', 'cnt']
Q077  ✓     ✓    ✓    712    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
Q078  ✓     ✓    ✗    1041   after_sales/medium
Q079  ✓     ✓    ✗    1306   after_sales/hard
       ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['created_at']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
       ↳ 表/JOIN 缺失：['refunds']
       ↳ 事实表混用：退款应读 refunds，不是 after_sales
Q080  ✓     ✓    ✗    1031   after_sales/easy

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q015】2026 年 8 月带来销售额最高的促销活动
  golden   : SELECT p.promotion_name, SUM(o.paid_amount) AS promo_sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY promo_sales DESC LIMIT 1
  生成     : SELECT promotion_id, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY promotion_id ORDER BY sales_amount DESC LIMIT 1
  ↳ 列名不符：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
  ↳ 表/JOIN 缺失：['promotions']

【Q024】2026 年 8 月各品类销售额
  golden   : SELECT oi.category, SUM(oi.line_paid_amount) AS sales FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY sales DESC
  生成     : SELECT oi.category, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN order_items AS oi ON o.order_id = oi.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'sales_amount'] 预期=['category', 'sales']

【Q025】2026 年 8 月长沙各渠道销售额
  golden   : SELECT o.channel, SUM(o.paid_amount) AS sales FROM orders o JOIN stores s ON o.store_id = s.store_id WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel ORDER BY sales DESC
  生成     : SELECT o.channel, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND c.city = '长沙' GROUP BY o.channel LIMIT 1000
  ↳ 列名不符：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
  ↳ 表/JOIN 缺失：['stores']
  ↳ 疑似表选错（golden 未用）：['customers']

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
  生成     : SELECT store_id, SUM(paid_amount) / COUNT(DISTINCT STRFTIME('%Y-%m-%d', paid_at)) AS daily_avg_sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']

【Q042】2026 年 8 月线上 vs 线下销售额对比
  golden   : SELECT channel, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY channel
  生成     : SELECT channel, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 AND channel IN ('线上', '线下') GROUP BY channel LIMIT 1000
  ↳ 列名不符：实际=[] 预期=['channel', 'sales']

【Q043】2026 年 8 月订单金额分布
  golden   : SELECT CASE WHEN paid_amount < 100 THEN 'under_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE 'over_2000' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket ORDER BY MIN(paid_amount)
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0-100' WHEN paid_amount < 500 THEN '100-500' WHEN paid_amount < 1000 THEN '500-1000' WHEN paid_amount < 5000 THEN '1000-5000' ELSE '5000+' END AS amount_range, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY amount_range ORDER BY MIN(paid_amount) LIMIT 1000
  ↳ 列名不符：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']

【Q044】近一年新客与老客销售额对比
  golden   : SELECT CASE WHEN c.registered_at >= '2024-08-01' THEN 'new' ELSE 'existing' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-08-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY customer_type
  生成     : SELECT CASE WHEN c.customer_level IN ('金卡', '铂金') THEN '老客' ELSE '新客' END AS customer_type, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= STRFTIME('%Y-%m-%d', 'now', '-1 year') AND o.paid_at < STRFTIME('%Y-%m-%d', 'now', '+1 day') AND o.paid_amount > 0 GROUP BY customer_type LIMIT 1000
  ↳ 列名不符：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
  ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']

【Q046】2026 年 8 月各门店销售额环比 7 月
  golden   : SELECT o.store_id, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM orders o WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY mom_growth DESC
  生成     : SELECT store_id, (SUM(CASE WHEN paid_at >= '2026-08-01' AND paid_at < '2026-09-01' THEN paid_amount ELSE 0 END) - SUM(CASE WHEN paid_at >= '2026-07-01' AND paid_at < '2026-08-01' THEN paid_amount ELSE 0 END)) / NULLIF(SUM(CASE WHEN paid_at >= '2026-07-01' AND paid_at < '2026-08-01' THEN paid_amount ELSE 0 END), 0) AS sales_mom_change FROM orders WHERE paid_amount > 0 AND ((paid_at >= '2026-07-01' AND paid_at < '2026-08-01') OR (paid_at >= '2026-08-01' AND paid_at < '2026-09-01')) GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'sales_mom_change'] 预期=['store_id', 'mom_growth']

【Q050】2026 年 8 月各门店利润
  golden   : SELECT o.store_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY profit DESC
  生成     : SELECT store_id, SUM(profit_amount) AS profit FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q052】近 3 个月各月利润率
  golden   : SELECT strftime('%Y-%m', o.paid_at) AS ym, SUM(oi.subtotal_profit) * 1.0 / SUM(oi.line_paid_amount) AS margin FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-06-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY ym ORDER BY ym
  生成     : SELECT STRFTIME('%Y-%m', o.paid_at) AS month, SUM(oi.subtotal_profit) / SUM(oi.line_paid_amount) AS profit_rate FROM orders AS o JOIN order_items AS oi ON o.order_id = oi.order_id WHERE o.paid_at >= STRFTIME('%Y-%m-01', 'now', '-2 months') AND o.paid_at < STRFTIME('%Y-%m-01', 'now', '+1 month') AND o.paid_amount > 0 GROUP BY STRFTIME('%Y-%m', o.paid_at) ORDER BY month LIMIT 1000
  ↳ 列名不符：实际=['month', 'profit_rate'] 预期=['ym', 'margin']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : SELECT CASE WHEN repurchase_count BETWEEN 1 AND 3 THEN '1-3次' WHEN repurchase_count BETWEEN 4 AND 6 THEN '4-6次' WHEN repurchase_count >= 7 THEN '7+次' END AS repurchase_group, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(*) - 1 AS repurchase_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) AS t WHERE repurchase_count >= 1 GROUP BY repurchase_group ORDER BY MIN(repurchase_count) LIMIT 1000
  ↳ 列名不符：实际=['repurchase_group', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
  ↳ 聚合去重缺失：应 COUNT(DISTINCT ...)
  ↳ 聚合函数不一致：golden=['COUNT'] 生成=['COUNT', 'MIN']

【Q057】2026 年 8 月高、中、低价值客户的销售额贡献
  golden   : SELECT CASE WHEN total_spend >= 5000 THEN 'high' WHEN total_spend >= 1000 THEN 'mid' ELSE 'low' END AS tier, SUM(total_spend) AS tier_sales FROM (SELECT customer_id, SUM(paid_amount) AS total_spend FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY tier ORDER BY tier_sales DESC
  生成     : SELECT CASE WHEN c.customer_level IN ('金卡', '铂金') THEN '高价值' WHEN c.customer_level = '银卡' THEN '中价值' ELSE '低价值' END AS customer_value_segment, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY customer_value_segment LIMIT 1000
  ↳ 列名不符：实际=['customer_value_segment', 'sales_amount'] 预期=['tier', 'tier_sales']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q062】最近一次快照各品类可销库存量
  golden   : SELECT p.category, SUM(s.quantity_available) AS available_qty FROM inventory_snapshots s JOIN products p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category ORDER BY available_qty DESC
  生成     : SELECT p.category, SUM(i.quantity_available) AS available_stock FROM inventory_snapshots AS i JOIN order_items AS p ON i.product_id = p.product_id WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q063】最近一次快照各门店安全线达标率
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pass_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id ORDER BY pass_rate DESC
  生成     : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) / COUNT(*) AS compliance_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']

【Q065】2026 年 8 月各促销类型销售额
  golden   : SELECT p.promotion_type, SUM(o.paid_amount) AS sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type ORDER BY sales DESC
  生成     : SELECT CASE WHEN promotion_id IS NULL THEN '无促销' ELSE CAST(promotion_id AS TEXT) END AS promotion_type, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY promotion_type LIMIT 1000
  ↳ 列名不符：实际=['promotion_type', 'sales_amount'] 预期=['promotion_type', 'sales']
  ↳ 表/JOIN 缺失：['promotions']

【Q066】2026 年 8 月各促销活动优惠总额
  golden   : SELECT p.promotion_name, SUM(o.discount_amount) AS discount_total FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY discount_total DESC
  生成     : SELECT promotion_id, SUM(discount_amount) AS total_discount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 AND NOT promotion_id IS NULL GROUP BY promotion_id LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
  ↳ 表/JOIN 缺失：['promotions']

【Q067】2026 年 8 月促销订单 vs 非促销订单销售额对比
  golden   : SELECT CASE WHEN promotion_id IS NOT NULL THEN 'promo' ELSE 'non_promo' END AS order_type, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type
  生成     : SELECT CASE WHEN NOT promotion_id IS NULL THEN '促销' ELSE '非促销' END AS order_type, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type LIMIT 1000
  ↳ 列名不符：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']

【Q071】2026 年 8 月各品类退款率
  golden   : SELECT t.category, SUM(CASE WHEN t.refund_amount IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_rate FROM (SELECT oi.category, r.refund_amount FROM order_items oi JOIN orders o ON oi.order_id = o.order_id LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0) t GROUP BY t.category ORDER BY refund_rate DESC
  生成     : SELECT oi.category, (SELECT SUM(r.refund_amount) FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed' AND r.order_id IN (SELECT o.order_id FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0) AND r.order_id IN (SELECT oi2.order_id FROM order_items AS oi2 WHERE oi2.category = oi.category)) / (SELECT SUM(oi3.line_paid_amount) FROM order_items AS oi3 JOIN orders AS o2 ON oi3.order_id = o2.order_id WHERE o2.paid_at >= '2026-08-01' AND o2.paid_at < '2026-09-01' AND o2.paid_amount > 0 AND oi3.category = oi.category) AS refund_rate FROM order_items AS oi WHERE NOT oi.category IS NULL GROUP BY oi.category LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']

【Q072】2026 年 8 月退款处理平均时长
  golden   : SELECT AVG(julianday(completed_at) - julianday(requested_at)) AS avg_days FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' AND completed_at IS NOT NULL AND requested_at IS NOT NULL
  生成     : SELECT AVG(resolution_time_hours) AS avg_refund_processing_hours FROM after_sales WHERE ticket_type = 'refund' AND created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['avg_refund_processing_hours'] 预期=['avg_days']
  ↳ 时间字段不一致：golden=['completed_at', 'requested_at'] 生成=['created_at']
  ↳ 表/JOIN 缺失：['refunds']
  ↳ 疑似表选错（golden 未用）：['after_sales']
  ↳ 事实表混用：退款应读 refunds，不是 after_sales

【Q073】2026 年 8 月有退款订单的售后工单率
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ticket_refund_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT (SELECT COUNT(DISTINCT a.order_id) FROM after_sales AS a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01' AND a.order_id IN (SELECT DISTINCT r.order_id FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed')) * 1.0 / (SELECT COUNT(DISTINCT r.order_id) FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed') AS after_sales_rate LIMIT 1000
  ↳ 列名不符：实际=['after_sales_rate'] 预期=['ticket_refund_ratio']
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
  生成     : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000

==============================================================
