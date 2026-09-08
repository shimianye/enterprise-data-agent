==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 76/80 = 95.0%
结果结构正确率: 70/80 = 87.5%
结果列名规范率: 15/80 = 18.8%
行数校验通过率: 73/80 = 91.2%
结果正确率: 46/75 = 61.3%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    1638   sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q002  ✓     ✓    ✓    1243   sales/medium
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q003  ✓     ✓    ✓    1386   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    869    sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    1106   profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    1148   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✗    ✗    2371   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'aug_sales', 'jul_sales', 'growth_rate'] 预期=['category', 'growth']
       ↳ 表/JOIN 缺失：['aug', 'jul']
Q008  ✓     ✓    ✓    899    customer/easy
       ↳ 列名不符（风格/字段）：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✗    774    customer/medium
Q010  ✓     ✓    ✓    1154   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    661    inventory/easy
Q012  ✓     ✓    ✗    1076   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'total_quantity'] 预期=['product_id', 'quantity_on_hand']
       ↳ 聚合函数不一致：golden=['MAX'] 生成=['MAX', 'SUM']
Q013  ✓     ✓    ✓    1226   inventory/medium
Q014  ✓     ✓    ✗    1140   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q015  ✓     ✓    ✗    1147   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
       ↳ 表/JOIN 缺失：['promotions']
Q016  ✓     ✓    ✓    892    refund/easy
       ↳ 列名不符（风格/字段）：实际=['total_refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    796    refund/medium
Q018  ✓     ✓    ✓    908    refund/medium
Q019  ✓     ✓    ✓    971    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✗    1233   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']
Q021  ✓     ✓    ✓    821    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q022  ✓     ✓    ✓    1016   sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    871    sales/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'sales_amount'] 预期=['product_id', 'sales']
Q024  ✗     ✗    -    0      sales/medium
       ↳ 错误: sql_invalid: ['unknown_table:p']
Q025  ✓     ✓    ✗    1170   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
       ↳ 表/JOIN 缺失：['stores']
       ↳ 疑似表选错（golden 未用）：['customers']
Q026  ✓     ✓    ✓    1398   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'gross_profit'] 预期=['category', 'profit']
Q027  ✓     ✓    ✓    1303   profit/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'gross_profit'] 预期=['product_id', 'profit']
Q028  ✓     ✓    ✓    1341   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q029  ✓     ✓    ✓    1137   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit'] 预期=['ym', 'profit']
Q030  ✓     ✓    ✓    604    customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'customer_count'] 预期=['customer_level', 'cnt']
Q031  ✓     ✓    ✓    1125   customer/easy
       ↳ 列名不符（风格/字段）：实际=['city', 'customer_count'] 预期=['city', 'cnt']
Q032  ✓     ✓    ✓    644    customer/easy
       ↳ 列名不符（风格/字段）：实际=['new_customer_count'] 预期=['cnt']
Q033  ✓     ✗    ✗    2016   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_rate'] 预期=['ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q034  ✗     ✗    -    0      inventory/medium
       ↳ 错误: sql_invalid: ['unknown_column:products.unit_cost']
Q035  ✓     ✗    ✗    948    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']
Q036  ✓     ✓    ✓    1035   inventory/easy
Q037  ✓     ✓    -    944    promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'order_count'] 预期=['promotion_name', 'cnt']
Q038  ✗     ✗    -    0      refund/medium
       ↳ 错误: sql_invalid: ['unknown_column:refunds.store_id']
Q039  ✓     ✓    ✓    1126   refund/medium
Q040  ✓     ✓    ✓    708    after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ticket_count'] 预期=['ticket_type', 'cnt']
Q041  ✓     ✓    ✗    891    sales/easy
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']
       ↳ 疑似表选错（golden 未用）：['stores']
Q042  ✓     ✓    ✓    876    sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q043  ✓     ✓    ✗    1161   sales/medium
       ↳ 列名不符（风格/字段）：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']
       ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']
Q044  ✓     ✓    ✗    1301   sales/medium
       ↳ 列名不符（风格/字段）：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
Q045  ✓     ✓    ✓    854    sales/hard
       ↳ 列名不符（风格/字段）：实际=['yoy_ratio'] 预期=['yoy_growth']
Q046  ✓     ✗    ✗    1834   sales/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'store_name', 'sales_change'] 预期=['store_id', 'mom_growth']
       ↳ 疑似表选错（golden 未用）：['stores']
Q047  ✓     ✓    ✓    1011   sales/easy
       ↳ 列名不符（风格/字段）：实际=['max_order_amount'] 预期=['max_order']
Q048  ✓     ✓    ✓    882    profit/easy
       ↳ 列名不符（风格/字段）：实际=['gross_profit'] 预期=['profit']
Q049  ✓     ✓    ✓    1120   profit/medium
Q050  ✓     ✓    ✓    865    profit/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'gross_profit'] 预期=['store_id', 'profit']
Q051  ✓     ✗    ✗    1249   profit/hard
       ↳ 列名不符（风格/字段）：实际=['year', 'half', 'total_profit'] 预期=['yoy_profit_growth']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q052  ✓     ✓    ✓    1151   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit_rate'] 预期=['ym', 'margin']
Q053  ✓     ✓    ✓    1390   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'city', 'customer_count'] 预期=['customer_level', 'city', 'cnt']
Q054  ✓     ✓    ✓    1522   customer/medium
       ↳ 列名不符（风格/字段）：实际=['paid_customer_count'] 预期=['cnt']
Q055  ✓     ✓    ✗    1822   customer/medium
       ↳ 列名不符（风格/字段）：实际=['segment', 'customer_count'] 预期=['bucket', 'cnt']
Q056  ✓     ✓    ✗    1557   customer/hard
Q057  ✗     ✗    -    0      customer/medium
       ↳ 错误: sql_invalid: ['unknown_column:customers.customer_value']
Q058  ✓     ✓    ✓    698    inventory/easy
       ↳ 列名不符（风格/字段）：实际=['total_inventory'] 预期=['total_on_hand']
Q059  ✓     ✓    ✓    979    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'stockout_sku_count'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    746    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✗    2819   inventory/hard
       ↳ 列名不符（风格/字段）：实际=['zero_sales_sku_count'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✗    5389   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q063  ✓     ✓    ✓    893    inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    744    promotion/easy
       ↳ 列名不符（风格/字段）：实际=['order_count'] 预期=['cnt']
Q065  ✓     ✓    ✗    1121   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'sales_amount'] 预期=['promotion_type', 'sales']
Q066  ✓     ✓    ✗    1350   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
Q067  ✓     ✓    ✗    1255   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']
Q068  ✓     ✗    ✗    1449   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['promotion_type', 'sales_amount', 'gross_profit', 'roi'] 预期=['promotion_type', 'roi']
Q069  ✓     ✓    ✓    1262   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_order_count'] 预期=['cnt']
Q070  ✓     ✓    ✗    1006   refund/medium
       ↳ 列名不符（风格/字段）：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
Q071  ✓     ✓    ✗    80664  refund/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']
Q072  ✓     ✓    ✓    1076   refund/medium
Q073  ✓     ✓    ✗    1295   refund/hard
       ↳ 列名不符（风格/字段）：实际=['after_sales_rate'] 预期=['ticket_refund_ratio']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q074  ✓     ✓    ✓    802    refund/medium
       ↳ 列名不符（风格/字段）：实际=['week', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✓     ✓    ✓    1173   refund/hard
       ↳ 列名不符（风格/字段）：实际=['customer_cnt'] 预期=['cnt']
Q076  ✓     ✓    ✓    818    after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_status', 'ticket_count'] 预期=['ticket_status', 'cnt']
Q077  ✓     ✓    ✗    851    after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
       ↳ 时间字段不一致：golden=['created_at'] 生成=['created_at', 'first_response_at']
Q078  ✓     ✓    ✗    1042   after_sales/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
Q079  ✓     ✓    ✗    1196   after_sales/hard
       ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['completed_at', 'paid_at']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
       ↳ 表/JOIN 缺失：['after_sales']
       ↳ 疑似表选错（golden 未用）：['orders']
       ↳ 事实表混用：售后应读 after_sales，不是 refunds
Q080  ✓     ✓    ✗    1053   after_sales/easy

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q007】2026 年 8 月相比 7 月，销售额环比增长最快的类目
  golden   : WITH aug AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY category), jul AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY category) SELECT aug.category, (aug.s - jul.s) / jul.s AS growth FROM aug JOIN jul ON aug.category = jul.category WHERE jul.s > 0 ORDER BY growth DESC LIMIT 1
  生成     : SELECT category, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN oi.line_paid_amount ELSE 0 END) AS aug_sales, SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN oi.line_paid_amount ELSE 0 END) AS jul_sales, (SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN oi.line_paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN oi.line_paid_amount ELSE 0 END)) / NULLIF(SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN oi.line_paid_amount ELSE 0 END), 0) AS growth_rate FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id WHERE o.paid_amount > 0 AND ((o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01') OR (o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01')) GROUP BY oi.category ORDER BY growth_rate DESC LIMIT 1
  ↳ 列名不符：实际=['category', 'aug_sales', 'jul_sales', 'growth_rate'] 预期=['category', 'growth']
  ↳ 表/JOIN 缺失：['aug', 'jul']

【Q009】金卡及以上等级客户占比
  golden   : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers
  生成     : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM customers LIMIT 1000

【Q012】最近一次快照中库存量最多的 10 个商品
  golden   : SELECT product_id, quantity_on_hand FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) ORDER BY quantity_on_hand DESC LIMIT 10
  生成     : SELECT product_id, SUM(quantity_on_hand) AS total_quantity FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY product_id ORDER BY total_quantity DESC LIMIT 10
  ↳ 列名不符：实际=['product_id', 'total_quantity'] 预期=['product_id', 'quantity_on_hand']
  ↳ 聚合函数不一致：golden=['MAX'] 生成=['MAX', 'SUM']

【Q014】2026 年 8 月使用促销的订单占比
  golden   : SELECT SUM(CASE WHEN promotion_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0
  生成     : SELECT COUNT(DISTINCT CASE WHEN NOT o.promotion_id IS NULL THEN o.order_id END) * 1.0 / COUNT(DISTINCT o.order_id) AS promotion_order_ratio FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 LIMIT 1000
  ↳ 列名不符：实际=['promotion_order_ratio'] 预期=['ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q015】2026 年 8 月带来销售额最高的促销活动
  golden   : SELECT p.promotion_name, SUM(o.paid_amount) AS promo_sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY promo_sales DESC LIMIT 1
  生成     : SELECT o.promotion_id, SUM(o.paid_amount) AS sales_amount FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.promotion_id ORDER BY sales_amount DESC LIMIT 1
  ↳ 列名不符：实际=['promotion_id', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
  ↳ 表/JOIN 缺失：['promotions']

【Q020】2026 年 8 月售后工单的解决率（已解决或已关闭占比）
  golden   : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01'
  生成     : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['resolution_rate'] 预期=['ratio']

【Q025】2026 年 8 月长沙各渠道销售额
  golden   : SELECT o.channel, SUM(o.paid_amount) AS sales FROM orders o JOIN stores s ON o.store_id = s.store_id WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel ORDER BY sales DESC
  生成     : SELECT o.channel, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE c.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel LIMIT 1000
  ↳ 列名不符：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
  ↳ 表/JOIN 缺失：['stores']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q033】2026 年 8 月客户复购率
  golden   : SELECT SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id)
  生成     : SELECT COUNT(DISTINCT o.customer_id) * 1.0 / (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS repurchase_rate FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.customer_id HAVING COUNT(DISTINCT o.order_id) > 1 LIMIT 1000
  ↳ 列名不符：实际=['repurchase_rate'] 预期=['ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q035】最近一次快照各 SKU 平均可用库存
  golden   : SELECT product_id, AVG(quantity_available) AS avg_available FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY product_id
  生成     : SELECT AVG(quantity_available) AS avg_available_stock FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) LIMIT 1000
  ↳ 列名不符：实际=['avg_available_stock'] 预期=['product_id', 'avg_available']

【Q041】2026 年 8 月各门店日均销售额
  golden   : SELECT store_id, SUM(paid_amount) * 1.0 / 31 AS daily_avg_sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id ORDER BY daily_avg_sales DESC
  生成     : SELECT s.store_id, SUM(o.paid_amount) / COUNT(DISTINCT STRFTIME('%Y-%m-%d', o.paid_at)) AS daily_avg_sales FROM orders AS o JOIN stores AS s ON o.store_id = s.store_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY s.store_id LIMIT 1000
  ↳ 聚合函数不一致：golden=['SUM'] 生成=['COUNT', 'SUM']
  ↳ 疑似表选错（golden 未用）：['stores']

【Q043】2026 年 8 月订单金额分布
  golden   : SELECT CASE WHEN paid_amount < 100 THEN 'under_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE 'over_2000' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket ORDER BY MIN(paid_amount)
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0-100' WHEN paid_amount < 500 THEN '100-500' WHEN paid_amount < 1000 THEN '500-1000' WHEN paid_amount < 5000 THEN '1000-5000' ELSE '5000+' END AS amount_range, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY amount_range ORDER BY amount_range LIMIT 1000
  ↳ 列名不符：实际=['amount_range', 'order_count'] 预期=['bucket', 'cnt']
  ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']

【Q044】近一年新客与老客销售额对比
  golden   : SELECT CASE WHEN c.registered_at >= '2024-08-01' THEN 'new' ELSE 'existing' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-08-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY customer_type
  生成     : SELECT CASE WHEN c.customer_id IN (SELECT customer_id FROM orders WHERE paid_at >= '2025-01-01' AND paid_at < '2026-01-01' AND paid_amount > 0) THEN '新客' ELSE '老客' END AS customer_type, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2026-01-01' AND o.paid_amount > 0 GROUP BY customer_type LIMIT 1000
  ↳ 列名不符：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
  ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']

【Q046】2026 年 8 月各门店销售额环比 7 月
  golden   : SELECT o.store_id, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM orders o WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY mom_growth DESC
  生成     : SELECT s.store_id, s.store_name, (SELECT SUM(o2.paid_amount) FROM orders AS o2 WHERE o2.store_id = s.store_id AND o2.paid_at >= '2026-08-01' AND o2.paid_at < '2026-09-01' AND o2.paid_amount > 0) - (SELECT SUM(o1.paid_amount) FROM orders AS o1 WHERE o1.store_id = s.store_id AND o1.paid_at >= '2026-07-01' AND o1.paid_at < '2026-08-01' AND o1.paid_amount > 0) AS sales_change FROM stores AS s WHERE s.store_id IN (SELECT store_id FROM orders WHERE paid_at >= '2026-07-01' AND paid_at < '2026-09-01' AND paid_amount > 0) ORDER BY sales_change DESC LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'store_name', 'sales_change'] 预期=['store_id', 'mom_growth']
  ↳ 疑似表选错（golden 未用）：['stores']

【Q051】2026 H1 vs 2025 H1 利润对比
  golden   : SELECT (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-07-01' AND o.paid_amount > 0) - (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2025-07-01' AND o.paid_amount > 0) AS yoy_profit_growth
  生成     : SELECT STRFTIME('%Y', paid_at) AS year, CASE WHEN STRFTIME('%m', paid_at) IN ('01', '02', '03', '04', '05', '06') THEN 'H1' END AS half, SUM(profit_amount) AS total_profit FROM orders WHERE paid_at >= '2025-01-01' AND paid_at < '2026-07-01' AND paid_amount > 0 AND STRFTIME('%m', paid_at) IN ('01', '02', '03', '04', '05', '06') GROUP BY year, half ORDER BY year LIMIT 1000
  ↳ 列名不符：实际=['year', 'half', 'total_profit'] 预期=['yoy_profit_growth']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q055】2026 年 8 月客单价分段客户数
  golden   : SELECT CASE WHEN avg_aov < 100 THEN '0_100' WHEN avg_aov < 500 THEN '100_500' WHEN avg_aov < 2000 THEN '500_2000' ELSE '2000_plus' END AS bucket, COUNT(*) AS cnt FROM (SELECT customer_id, AVG(paid_amount) AS avg_aov FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY bucket
  生成     : SELECT CASE WHEN avg_paid < 100 THEN '0-100' WHEN avg_paid < 200 THEN '100-200' WHEN avg_paid < 300 THEN '200-300' ELSE '300+' END AS segment, COUNT(*) AS customer_count FROM (SELECT o.customer_id, AVG(o.paid_amount) AS avg_paid FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.customer_id) AS t GROUP BY segment LIMIT 1000
  ↳ 列名不符：实际=['segment', 'customer_count'] 预期=['bucket', 'cnt']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : SELECT CASE WHEN repurchase_count BETWEEN 1 AND 3 THEN '1-3' WHEN repurchase_count BETWEEN 4 AND 6 THEN '4-6' ELSE '7+' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) - 1 AS repurchase_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) AS t WHERE repurchase_count >= 1 GROUP BY repurchase_tier LIMIT 1000

【Q061】近 90 天零销量 SKU 数
  golden   : SELECT COUNT(*) AS slow_moving_cnt FROM products p WHERE p.is_active = 1 AND NOT EXISTS (SELECT 1 FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE oi.product_id = p.product_id AND o.paid_at >= '2026-05-10' AND o.paid_at < '2026-08-09' AND o.paid_amount > 0)
  生成     : SELECT COUNT(*) AS zero_sales_sku_count FROM products AS p WHERE NOT EXISTS(SELECT 1 FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id WHERE oi.product_id = p.product_id AND o.paid_at >= '2025-06-01' AND o.paid_at < '2025-08-30' AND o.paid_amount > 0) LIMIT 1000
  ↳ 列名不符：实际=['zero_sales_sku_count'] 预期=['slow_moving_cnt']

【Q062】最近一次快照各品类可销库存量
  golden   : SELECT p.category, SUM(s.quantity_available) AS available_qty FROM inventory_snapshots s JOIN products p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category ORDER BY available_qty DESC
  生成     : SELECT p.category, SUM(i.quantity_available) AS available_stock FROM inventory_snapshots AS i JOIN order_items AS p ON i.product_id = p.product_id WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q065】2026 年 8 月各促销类型销售额
  golden   : SELECT p.promotion_type, SUM(o.paid_amount) AS sales FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type ORDER BY sales DESC
  生成     : SELECT p.promotion_id, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN promotions AS p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_id LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'sales_amount'] 预期=['promotion_type', 'sales']

【Q066】2026 年 8 月各促销活动优惠总额
  golden   : SELECT p.promotion_name, SUM(o.discount_amount) AS discount_total FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY discount_total DESC
  生成     : SELECT p.promotion_id, SUM(o.discount_amount) AS total_discount FROM orders AS o JOIN promotions AS p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_id LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']

【Q067】2026 年 8 月促销订单 vs 非促销订单销售额对比
  golden   : SELECT CASE WHEN promotion_id IS NOT NULL THEN 'promo' ELSE 'non_promo' END AS order_type, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type
  生成     : SELECT CASE WHEN NOT o.promotion_id IS NULL THEN '促销' ELSE '非促销' END AS order_type, SUM(o.paid_amount) AS sales_amount FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY CASE WHEN NOT o.promotion_id IS NULL THEN '促销' ELSE '非促销' END LIMIT 1000
  ↳ 列名不符：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']

【Q068】2026 年 8 月各促销类型 ROI
  golden   : SELECT p.promotion_type, (SUM(o.paid_amount) - SUM(o.discount_amount)) * 1.0 / NULLIF(SUM(o.discount_amount), 0) AS roi FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type ORDER BY roi DESC
  生成     : SELECT p.promotion_type, SUM(o.paid_amount) AS sales_amount, SUM(o.profit_amount) AS gross_profit, SUM(o.paid_amount) / NULLIF(SUM(o.paid_amount), 0) AS roi FROM orders AS o JOIN promotions AS p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type LIMIT 1000
  ↳ 列名不符：实际=['promotion_type', 'sales_amount', 'gross_profit', 'roi'] 预期=['promotion_type', 'roi']

【Q070】2026 年 8 月各退款原因占比
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC
  生成     : SELECT refund_reason, COUNT(*) * 1.0 / (SELECT COUNT(*) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') AS ratio FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason LIMIT 1000
  ↳ 列名不符：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']

【Q071】2026 年 8 月各品类退款率
  golden   : SELECT t.category, SUM(CASE WHEN t.refund_amount IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_rate FROM (SELECT oi.category, r.refund_amount FROM order_items oi JOIN orders o ON oi.order_id = o.order_id LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0) t GROUP BY t.category ORDER BY refund_rate DESC
  生成     : SELECT oi.category, (SELECT SUM(r.refund_amount) FROM refunds AS r WHERE r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.order_id IN (SELECT oi2.order_id FROM order_items AS oi2 WHERE oi2.category = oi.category)) / NULLIF(SUM(oi.line_paid_amount), 0) AS refund_rate FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']

【Q073】2026 年 8 月有退款订单的售后工单率
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ticket_refund_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT (SELECT COUNT(DISTINCT a.order_id) FROM after_sales AS a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01' AND a.order_id IN (SELECT DISTINCT r.order_id FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed')) * 1.0 / (SELECT COUNT(DISTINCT r.order_id) FROM refunds AS r WHERE r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' AND r.refund_status = 'completed') AS after_sales_rate LIMIT 1000
  ↳ 列名不符：实际=['after_sales_rate'] 预期=['ticket_refund_ratio']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q077】2026 年 8 月首次响应平均时长
  golden   : SELECT AVG(response_time_minutes) AS avg_response_minutes FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND response_time_minutes IS NOT NULL
  生成     : SELECT AVG(first_response_at - created_at) AS avg_first_response_minutes FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND NOT first_response_at IS NULL AND NOT created_at IS NULL LIMIT 1000
  ↳ 列名不符：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
  ↳ 时间字段不一致：golden=['created_at'] 生成=['created_at', 'first_response_at']

【Q078】2026 年 8 月各工单类型解决率
  golden   : SELECT ticket_type, SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type ORDER BY resolution_rate DESC
  生成     : SELECT ticket_type, COUNT(CASE WHEN ticket_status = 'resolved' THEN 1 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']

【Q079】2026 年 8 月涉及退款的工单占比
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_ticket_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT (SELECT COUNT(DISTINCT order_id) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') * 1.0 / (SELECT COUNT(DISTINCT order_id) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_ticket_ratio LIMIT 1000
  ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['completed_at', 'paid_at']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
  ↳ 表/JOIN 缺失：['after_sales']
  ↳ 疑似表选错（golden 未用）：['orders']
  ↳ 事实表混用：售后应读 after_sales，不是 refunds

【Q080】2026 年 8 月高满意度工单占比
  golden   : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND satisfaction_score IS NOT NULL
  生成     : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND ticket_status = 'resolved' AND NOT satisfaction_score IS NULL LIMIT 1000

==============================================================
