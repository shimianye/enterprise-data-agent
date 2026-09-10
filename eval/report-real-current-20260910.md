# Text2SQL 真实 LLM 评测报告

- 运行日期：2026-09-10
- 模式：`real`
- Provider：OpenAI-compatible DeepSeek API
- 模型：`deepseek-chat`
- Temperature：`0`
- Git commit：`61b3e7c47f9f5a89963515d6630b1baaec71944d`
- 数据库：`data/enterprise.db`
- 评测集：`eval/cases.jsonl`，80 题
- SQL 明细：`eval/sql_dump-real-current-20260910.jsonl`

==============================================================
Text2SQL 评测报告
==============================================================

总题数: 80
SQL 可执行率: 80/80 = 100.0%
结果结构正确率: 78/80 = 97.5%
结果列名规范率: 17/80 = 21.2%
行数校验通过率: 79/80 = 98.8%
结果正确率: 54/80 = 67.5%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    2525   sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q002  ✓     ✓    ✓    2229   sales/medium
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q003  ✓     ✓    ✓    1916   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    2220   sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    1857   profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    2315   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_margin'] 预期=['category', 'margin']
Q007  ✓     ✓    ✗    2200   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'growth_rate'] 预期=['category', 'growth']
       ↳ 表/JOIN 缺失：['aug', 'jul']
Q008  ✓     ✓    ✓    1575   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q009  ✓     ✓    ✗    1630   customer/medium
Q010  ✓     ✓    ✓    2115   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    1654   inventory/easy
Q012  ✓     ✓    ✓    2079   inventory/medium
Q013  ✓     ✓    ✓    2047   inventory/medium
Q014  ✓     ✓    ✓    1806   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✓    ✓    2217   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_name', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
Q016  ✓     ✓    ✓    1909   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    1998   refund/medium
Q018  ✓     ✓    ✗    2000   refund/medium
       ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']
Q019  ✓     ✓    ✓    1866   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_response_time_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✗    1866   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']
Q021  ✓     ✓    ✓    1600   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q022  ✓     ✓    ✓    2003   sales/easy
       ↳ 列名不符（风格/字段）：实际=['average_order_value'] 预期=['aov']
Q023  ✓     ✓    ✓    3194   sales/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'sales_amount'] 预期=['product_id', 'sales']
Q024  ✓     ✓    ✗    2116   sales/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'sales_amount'] 预期=['category', 'sales']
Q025  ✓     ✓    ✗    2136   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
       ↳ 表/JOIN 缺失：['stores']
       ↳ 疑似表选错（golden 未用）：['customers']
Q026  ✓     ✓    ✓    1996   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'gross_profit'] 预期=['category', 'profit']
Q027  ✓     ✓    ✓    2846   profit/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'gross_profit'] 预期=['product_id', 'profit']
Q028  ✓     ✓    ✓    1861   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_margin'] 预期=['category', 'margin']
Q029  ✓     ✓    ✓    1992   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit'] 预期=['ym', 'profit']
Q030  ✓     ✓    ✓    1894   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'customer_count'] 预期=['customer_level', 'cnt']
Q031  ✓     ✓    ✓    1888   customer/easy
       ↳ 列名不符（风格/字段）：实际=['city', 'customer_count'] 预期=['city', 'cnt']
Q032  ✓     ✓    ✓    1828   customer/easy
       ↳ 列名不符（风格/字段）：实际=['new_customers'] 预期=['cnt']
Q033  ✓     ✓    ✓    1988   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_rate'] 预期=['ratio']
Q034  ✓     ✓    ✗    4563   inventory/medium
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q035  ✓     ✓    ✓    1806   inventory/medium
Q036  ✓     ✓    ✓    1736   inventory/easy
Q037  ✓     ✓    ✓    1976   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_name', 'order_count'] 预期=['promotion_name', 'cnt']
Q038  ✓     ✓    ✓    2188   refund/medium
Q039  ✓     ✓    ✓    2086   refund/medium
Q040  ✓     ✓    ✓    1905   after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_type', 'ticket_count'] 预期=['ticket_type', 'cnt']
Q041  ✓     ✓    ✓    1864   sales/easy
       ↳ 列名不符（风格/字段）：实际=['store_id', 'avg_daily_sales'] 预期=['store_id', 'daily_avg_sales']
Q042  ✓     ✓    ✓    1800   sales/medium
       ↳ 列名不符（风格/字段）：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
Q043  ✓     ✓    ✗    2121   sales/medium
       ↳ 列名不符（风格/字段）：实际=['amount_bucket', 'order_count'] 预期=['bucket', 'cnt']
       ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']
Q044  ✓     ✓    ✗    2512   sales/medium
       ↳ 列名不符（风格/字段）：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
       ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
       ↳ 聚合函数不一致：golden=['SUM'] 生成=['MIN', 'SUM']
       ↳ 表/JOIN 缺失：['customers']
       ↳ 疑似表选错（golden 未用）：['customer_first_order']
Q045  ✓     ✓    ✓    1951   sales/hard
       ↳ 列名不符（风格/字段）：实际=['yoy_ratio'] 预期=['yoy_growth']
Q046  ✓     ✗    ✗    2259   sales/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'aug_sales', 'jul_sales'] 预期=['store_id', 'mom_growth']
Q047  ✓     ✓    ✓    1980   sales/easy
       ↳ 列名不符（风格/字段）：实际=['max_order_amount'] 预期=['max_order']
Q048  ✓     ✓    ✓    1793   profit/easy
       ↳ 列名不符（风格/字段）：实际=['gross_profit'] 预期=['profit']
Q049  ✓     ✓    ✓    1917   profit/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'gross_profit'] 预期=['brand', 'profit']
Q050  ✓     ✓    ✗    2137   profit/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'gross_profit'] 预期=['store_id', 'profit']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q051  ✓     ✗    ✗    2373   profit/hard
       ↳ 列名不符（风格/字段）：实际=['year', 'total_profit'] 预期=['yoy_profit_growth']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q052  ✓     ✓    ✗    2166   profit/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'profit_margin'] 预期=['ym', 'margin']
       ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
       ↳ 表/JOIN 缺失：['order_items']
Q053  ✓     ✓    ✓    1885   customer/easy
       ↳ 列名不符（风格/字段）：实际=['customer_level', 'city', 'customer_count'] 预期=['customer_level', 'city', 'cnt']
Q054  ✓     ✓    ✓    2788   customer/medium
       ↳ 列名不符（风格/字段）：实际=['paying_customers'] 预期=['cnt']
Q055  ✓     ✓    ✗    1884   customer/medium
       ↳ 列名不符（风格/字段）：实际=['bucket', 'order_count'] 预期=['bucket', 'cnt']
       ↳ 聚合函数不一致：golden=['AVG', 'COUNT'] 生成=['COUNT']
Q056  ✓     ✓    ✗    2051   customer/hard
       ↳ 列名不符（风格/字段）：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
       ↳ 疑似表选错（golden 未用）：['customer_orders']
Q057  ✓     ✓    ✗    1947   customer/medium
       ↳ 列名不符（风格/字段）：实际=['value_tier', 'sales_amount'] 预期=['tier', 'tier_sales']
       ↳ 疑似表选错（golden 未用）：['customers']
Q058  ✓     ✓    ✓    1886   inventory/easy
Q059  ✓     ✓    ✓    2602   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'stockout_sku_count'] 预期=['store_id', 'sku_count']
Q060  ✓     ✓    ✓    1760   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['cnt'] 预期=['low_stock_cnt']
Q061  ✓     ✓    ✓    3317   inventory/hard
       ↳ 列名不符（风格/字段）：实际=['sku_count'] 预期=['slow_moving_cnt']
Q062  ✓     ✓    ✗    4823   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
       ↳ 表/JOIN 缺失：['products']
       ↳ 疑似表选错（golden 未用）：['order_items']
Q063  ✓     ✓    ✗    2355   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']
Q064  ✓     ✓    ✓    1985   promotion/easy
       ↳ 列名不符（风格/字段）：实际=['order_count'] 预期=['cnt']
Q065  ✓     ✓    ✓    2366   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_type', 'sales_amount'] 预期=['promotion_type', 'sales']
Q066  ✓     ✓    ✗    2166   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
       ↳ 表/JOIN 缺失：['promotions']
Q067  ✓     ✓    ✗    2355   promotion/hard
       ↳ 列名不符（风格/字段）：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']
Q068  ✓     ✓    ✗    2038   promotion/hard
Q069  ✓     ✓    ✓    2144   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_order_count'] 预期=['cnt']
Q070  ✓     ✓    ✗    1891   refund/medium
       ↳ 列名不符（风格/字段）：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
       ↳ 聚合函数不一致：golden=['COUNT'] 生成=['SUM']
Q071  ✓     ✓    ✗    2231   refund/medium
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']
Q072  ✓     ✓    ✓    2127   refund/medium
Q073  ✓     ✓    ✗    2824   refund/hard
       ↳ 列名不符（风格/字段）：实际=['ticket_rate'] 预期=['ticket_refund_ratio']
       ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['completed_at', 'paid_at']
       ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
       ↳ 疑似表选错（golden 未用）：['orders']
Q074  ✓     ✓    ✓    2214   refund/medium
       ↳ 列名不符（风格/字段）：实际=['week', 'refund_amount'] 预期=['yweek', 'refund_amount']
Q075  ✓     ✓    ✓    1942   refund/hard
Q076  ✓     ✓    ✓    1936   after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ticket_status', 'ticket_count'] 预期=['ticket_status', 'cnt']
Q077  ✓     ✓    ✓    2186   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_response_minutes']
Q078  ✓     ✓    ✗    1876   after_sales/medium
Q079  ✓     ✓    ✓    2384   after_sales/hard
       ↳ 列名不符（风格/字段）：实际=['ratio'] 预期=['refund_ticket_ratio']
Q080  ✓     ✓    ✗    1990   after_sales/easy
       ↳ 列名不符（风格/字段）：实际=['ratio'] 预期=['high_satisfaction_ratio']

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q007】2026 年 8 月相比 7 月，销售额环比增长最快的类目
  golden   : WITH aug AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY category), jul AS (SELECT category, SUM(line_paid_amount) AS s FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY category) SELECT aug.category, (aug.s - jul.s) / jul.s AS growth FROM aug JOIN jul ON aug.category = jul.category WHERE jul.s > 0 ORDER BY growth DESC LIMIT 1
  生成     : SELECT order_items.category, (SUM(CASE WHEN orders.paid_at >= '2026-08-01' AND orders.paid_at < '2026-09-01' THEN orders.paid_amount ELSE 0 END) - SUM(CASE WHEN orders.paid_at >= '2026-07-01' AND orders.paid_at < '2026-08-01' THEN orders.paid_amount ELSE 0 END)) / NULLIF(SUM(CASE WHEN orders.paid_at >= '2026-07-01' AND orders.paid_at < '2026-08-01' THEN orders.paid_amount ELSE 0 END), 0) AS growth_rate FROM orders JOIN order_items ON orders.order_id = order_items.order_id WHERE orders.paid_amount > 0 AND orders.paid_at >= '2026-07-01' AND orders.paid_at < '2026-09-01' GROUP BY order_items.category ORDER BY growth_rate DESC LIMIT 1
  ↳ 列名不符：实际=['category', 'growth_rate'] 预期=['category', 'growth']
  ↳ 表/JOIN 缺失：['aug', 'jul']

【Q009】金卡及以上等级客户占比
  golden   : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM customers
  生成     : SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers LIMIT 1000

【Q018】2026 年 8 月最常见的退款原因
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE requested_at >= '2026-08-01' AND requested_at < '2026-09-01' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  生成     : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC LIMIT 1
  ↳ 时间字段不一致：golden=['requested_at'] 生成=['completed_at']

【Q020】2026 年 8 月售后工单的解决率（已解决或已关闭占比）
  golden   : SELECT SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01'
  生成     : SELECT SUM(CASE WHEN ticket_status IN ('已解决', '已关闭') THEN 1 ELSE 0 END) / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['resolution_rate'] 预期=['ratio']

【Q024】2026 年 8 月各品类销售额
  golden   : SELECT oi.category, SUM(oi.line_paid_amount) AS sales FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY oi.category ORDER BY sales DESC
  生成     : SELECT order_items.category, SUM(orders.paid_amount) AS sales_amount FROM orders JOIN order_items ON orders.order_id = order_items.order_id WHERE orders.paid_at >= '2026-08-01' AND orders.paid_at < '2026-09-01' AND orders.paid_amount > 0 GROUP BY order_items.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'sales_amount'] 预期=['category', 'sales']

【Q025】2026 年 8 月长沙各渠道销售额
  golden   : SELECT o.channel, SUM(o.paid_amount) AS sales FROM orders o JOIN stores s ON o.store_id = s.store_id WHERE s.city = '长沙' AND o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.channel ORDER BY sales DESC
  生成     : SELECT orders.channel, SUM(orders.paid_amount) AS sales_amount FROM orders JOIN customers ON orders.customer_id = customers.customer_id WHERE orders.paid_at >= '2026-08-01' AND orders.paid_at < '2026-09-01' AND orders.paid_amount > 0 AND customers.city = '长沙' GROUP BY orders.channel LIMIT 1000
  ↳ 列名不符：实际=['channel', 'sales_amount'] 预期=['channel', 'sales']
  ↳ 表/JOIN 缺失：['stores']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q034】最近一次快照各门店库存总金额
  golden   : SELECT inv.store_id, SUM(inv.quantity_on_hand * p.cost_price) AS inventory_value FROM inventory_snapshots inv JOIN products p ON inv.product_id = p.product_id WHERE inv.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY inv.store_id ORDER BY inventory_value DESC
  生成     : SELECT store_id, SUM(quantity_on_hand * unit_cost) AS inventory_value FROM inventory_snapshots JOIN order_items ON inventory_snapshots.product_id = order_items.product_id WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id LIMIT 1000
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q043】2026 年 8 月订单金额分布
  golden   : SELECT CASE WHEN paid_amount < 100 THEN 'under_100' WHEN paid_amount < 500 THEN '100_500' WHEN paid_amount < 2000 THEN '500_2000' ELSE 'over_2000' END AS bucket, COUNT(*) AS cnt FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket ORDER BY MIN(paid_amount)
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '0-100' WHEN paid_amount < 300 THEN '100-300' WHEN paid_amount < 500 THEN '300-500' WHEN paid_amount < 1000 THEN '500-1000' ELSE '1000+' END AS amount_bucket, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY amount_bucket LIMIT 1000
  ↳ 列名不符：实际=['amount_bucket', 'order_count'] 预期=['bucket', 'cnt']
  ↳ 聚合函数不一致：golden=['COUNT', 'MIN'] 生成=['COUNT']

【Q044】近一年新客与老客销售额对比
  golden   : SELECT CASE WHEN c.registered_at >= '2024-08-01' THEN 'new' ELSE 'existing' END AS customer_type, SUM(o.paid_amount) AS sales FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2025-08-01' AND o.paid_at < '2026-08-01' AND o.paid_amount > 0 GROUP BY customer_type
  生成     : WITH customer_first_order AS (SELECT customer_id, MIN(paid_at) AS first_paid_at FROM orders WHERE paid_amount > 0 GROUP BY customer_id) SELECT CASE WHEN o.paid_at = cfo.first_paid_at THEN '新客' ELSE '老客' END AS customer_type, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customer_first_order AS cfo ON o.customer_id = cfo.customer_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2026-01-01' AND o.paid_amount > 0 GROUP BY customer_type LIMIT 1000
  ↳ 列名不符：实际=['customer_type', 'sales_amount'] 预期=['customer_type', 'sales']
  ↳ 时间字段不一致：golden=['paid_at', 'registered_at'] 生成=['paid_at']
  ↳ 聚合函数不一致：golden=['SUM'] 生成=['MIN', 'SUM']
  ↳ 表/JOIN 缺失：['customers']
  ↳ 疑似表选错（golden 未用）：['customer_first_order']

【Q046】2026 年 8 月各门店销售额环比 7 月
  golden   : SELECT o.store_id, SUM(CASE WHEN o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' THEN o.paid_amount ELSE 0 END) - SUM(CASE WHEN o.paid_at >= '2026-07-01' AND o.paid_at < '2026-08-01' THEN o.paid_amount ELSE 0 END) AS mom_growth FROM orders o WHERE o.paid_at >= '2026-07-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY mom_growth DESC
  生成     : SELECT store_id, SUM(CASE WHEN paid_at >= '2026-08-01' AND paid_at < '2026-09-01' THEN paid_amount ELSE 0 END) AS aug_sales, SUM(CASE WHEN paid_at >= '2026-07-01' AND paid_at < '2026-08-01' THEN paid_amount ELSE 0 END) AS jul_sales FROM orders WHERE paid_amount > 0 AND paid_at >= '2026-07-01' AND paid_at < '2026-09-01' GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'aug_sales', 'jul_sales'] 预期=['store_id', 'mom_growth']

【Q050】2026 年 8 月各门店利润
  golden   : SELECT o.store_id, SUM(oi.subtotal_profit) AS profit FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY o.store_id ORDER BY profit DESC
  生成     : SELECT store_id, SUM(profit_amount) AS gross_profit FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'gross_profit'] 预期=['store_id', 'profit']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q051】2026 H1 vs 2025 H1 利润对比
  golden   : SELECT (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-01-01' AND o.paid_at < '2026-07-01' AND o.paid_amount > 0) - (SELECT SUM(oi.subtotal_profit) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2025-01-01' AND o.paid_at < '2025-07-01' AND o.paid_amount > 0) AS yoy_profit_growth
  生成     : SELECT STRFTIME('%Y', paid_at) AS year, SUM(profit_amount) AS total_profit FROM orders WHERE paid_at >= '2025-01-01' AND paid_at < '2025-07-01' AND paid_amount > 0 GROUP BY STRFTIME('%Y', paid_at) UNION ALL SELECT STRFTIME('%Y', paid_at) AS year, SUM(profit_amount) AS total_profit FROM orders WHERE paid_at >= '2026-01-01' AND paid_at < '2026-07-01' AND paid_amount > 0 GROUP BY STRFTIME('%Y', paid_at) LIMIT 1000
  ↳ 列名不符：实际=['year', 'total_profit'] 预期=['yoy_profit_growth']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q052】近 3 个月各月利润率
  golden   : SELECT strftime('%Y-%m', o.paid_at) AS ym, SUM(oi.subtotal_profit) * 1.0 / SUM(oi.line_paid_amount) AS margin FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.paid_at >= '2026-06-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY ym ORDER BY ym
  生成     : SELECT STRFTIME('%Y-%m', paid_at) AS month, SUM(profit_amount) / SUM(paid_amount) AS profit_margin FROM orders WHERE paid_at >= '2026-06-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY STRFTIME('%Y-%m', paid_at) LIMIT 1000
  ↳ 列名不符：实际=['month', 'profit_margin'] 预期=['ym', 'margin']
  ↳ 利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit
  ↳ 表/JOIN 缺失：['order_items']

【Q055】2026 年 8 月客单价分段客户数
  golden   : SELECT CASE WHEN avg_aov < 100 THEN '0_100' WHEN avg_aov < 500 THEN '100_500' WHEN avg_aov < 2000 THEN '500_2000' ELSE '2000_plus' END AS bucket, COUNT(*) AS cnt FROM (SELECT customer_id, AVG(paid_amount) AS avg_aov FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY bucket
  生成     : SELECT CASE WHEN paid_amount < 100 THEN '<100' WHEN paid_amount < 300 THEN '100-300' WHEN paid_amount < 500 THEN '300-500' ELSE '>=500' END AS bucket, COUNT(DISTINCT orders.order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY bucket LIMIT 1000
  ↳ 列名不符：实际=['bucket', 'order_count'] 预期=['bucket', 'cnt']
  ↳ 聚合函数不一致：golden=['AVG', 'COUNT'] 生成=['COUNT']

【Q056】2026 年 8 月复购次数 1-3、4-6、7+ 次的客户数分布
  golden   : SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1_3' WHEN order_count BETWEEN 4 AND 6 THEN '4_6' WHEN order_count >= 7 THEN '7_plus' END AS repurchase_tier, COUNT(*) AS customer_count FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY repurchase_tier ORDER BY repurchase_tier
  生成     : WITH customer_orders AS (SELECT customer_id, COUNT(DISTINCT order_id) AS order_count FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) SELECT CASE WHEN order_count BETWEEN 1 AND 3 THEN '1-3' WHEN order_count BETWEEN 4 AND 6 THEN '4-6' ELSE '7+' END AS repurchase_bucket, COUNT(*) AS customer_count FROM customer_orders GROUP BY repurchase_bucket LIMIT 1000
  ↳ 列名不符：实际=['repurchase_bucket', 'customer_count'] 预期=['repurchase_tier', 'customer_count']
  ↳ 疑似表选错（golden 未用）：['customer_orders']

【Q057】2026 年 8 月高、中、低价值客户的销售额贡献
  golden   : SELECT CASE WHEN total_spend >= 5000 THEN 'high' WHEN total_spend >= 1000 THEN 'mid' ELSE 'low' END AS tier, SUM(total_spend) AS tier_sales FROM (SELECT customer_id, SUM(paid_amount) AS total_spend FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY customer_id) t GROUP BY tier ORDER BY tier_sales DESC
  生成     : SELECT CASE WHEN c.customer_level IN ('金卡', '铂金') THEN '高价值' WHEN c.customer_level = '银卡' THEN '中价值' ELSE '低价值' END AS value_tier, SUM(o.paid_amount) AS sales_amount FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY value_tier LIMIT 1000
  ↳ 列名不符：实际=['value_tier', 'sales_amount'] 预期=['tier', 'tier_sales']
  ↳ 疑似表选错（golden 未用）：['customers']

【Q062】最近一次快照各品类可销库存量
  golden   : SELECT p.category, SUM(s.quantity_available) AS available_qty FROM inventory_snapshots s JOIN products p ON s.product_id = p.product_id WHERE s.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY p.category ORDER BY available_qty DESC
  生成     : SELECT order_items.category, SUM(inventory_snapshots.quantity_available) AS available_stock FROM inventory_snapshots JOIN order_items ON inventory_snapshots.product_id = order_items.product_id WHERE inventory_snapshots.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY order_items.category LIMIT 1000
  ↳ 列名不符：实际=['category', 'available_stock'] 预期=['category', 'available_qty']
  ↳ 表/JOIN 缺失：['products']
  ↳ 疑似表选错（golden 未用）：['order_items']

【Q063】最近一次快照各门店安全线达标率
  golden   : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pass_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id ORDER BY pass_rate DESC
  生成     : SELECT store_id, SUM(CASE WHEN quantity_available >= reorder_level THEN 1 ELSE 0 END) / COUNT(*) AS compliance_rate FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) GROUP BY store_id LIMIT 1000
  ↳ 列名不符：实际=['store_id', 'compliance_rate'] 预期=['store_id', 'pass_rate']

【Q066】2026 年 8 月各促销活动优惠总额
  golden   : SELECT p.promotion_name, SUM(o.discount_amount) AS discount_total FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_name ORDER BY discount_total DESC
  生成     : SELECT promotion_id, SUM(discount_amount) AS total_discount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 AND NOT promotion_id IS NULL GROUP BY promotion_id LIMIT 1000
  ↳ 列名不符：实际=['promotion_id', 'total_discount'] 预期=['promotion_name', 'discount_total']
  ↳ 表/JOIN 缺失：['promotions']

【Q067】2026 年 8 月促销订单 vs 非促销订单销售额对比
  golden   : SELECT CASE WHEN promotion_id IS NOT NULL THEN 'promo' ELSE 'non_promo' END AS order_type, SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type
  生成     : SELECT CASE WHEN NOT promotion_id IS NULL THEN '促销订单' ELSE '非促销订单' END AS order_type, SUM(paid_amount) AS sales_amount FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0 GROUP BY order_type LIMIT 1000
  ↳ 列名不符：实际=['order_type', 'sales_amount'] 预期=['order_type', 'sales']

【Q068】2026 年 8 月各促销类型 ROI
  golden   : SELECT p.promotion_type, (SUM(o.paid_amount) - SUM(o.discount_amount)) * 1.0 / NULLIF(SUM(o.discount_amount), 0) AS roi FROM orders o JOIN promotions p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type ORDER BY roi DESC
  生成     : SELECT p.promotion_type, SUM(o.paid_amount) / NULLIF(SUM(p.discount_value), 0) AS roi FROM orders AS o JOIN promotions AS p ON o.promotion_id = p.promotion_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 GROUP BY p.promotion_type LIMIT 1000

【Q070】2026 年 8 月各退款原因占比
  golden   : SELECT refund_reason, COUNT(*) AS cnt FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason ORDER BY cnt DESC
  生成     : SELECT refund_reason, SUM(refund_amount) / (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') AS ratio FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed' GROUP BY refund_reason LIMIT 1000
  ↳ 列名不符：实际=['refund_reason', 'ratio'] 预期=['refund_reason', 'cnt']
  ↳ 聚合函数不一致：golden=['COUNT'] 生成=['SUM']

【Q071】2026 年 8 月各品类退款率
  golden   : SELECT t.category, SUM(CASE WHEN t.refund_amount IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS refund_rate FROM (SELECT oi.category, r.refund_amount FROM order_items oi JOIN orders o ON oi.order_id = o.order_id LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0) t GROUP BY t.category ORDER BY refund_rate DESC
  生成     : SELECT order_items.category, (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_rate FROM order_items GROUP BY order_items.category LIMIT 1000
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['SUM']

【Q073】2026 年 8 月有退款订单的售后工单率
  golden   : SELECT SUM(CASE WHEN EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = a.order_id AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS ticket_refund_ratio FROM after_sales a WHERE a.created_at >= '2026-08-01' AND a.created_at < '2026-09-01'
  生成     : SELECT COUNT(DISTINCT a.ticket_id) * 1.0 / COUNT(DISTINCT o.order_id) AS ticket_rate FROM orders AS o JOIN refunds AS r ON r.order_id = o.order_id LEFT JOIN after_sales AS a ON a.order_id = o.order_id WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 AND r.refund_status = 'completed' AND r.completed_at >= '2026-08-01' AND r.completed_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['ticket_rate'] 预期=['ticket_refund_ratio']
  ↳ 时间字段不一致：golden=['completed_at', 'created_at'] 生成=['completed_at', 'paid_at']
  ↳ 聚合函数不一致：golden=['COUNT', 'SUM'] 生成=['COUNT']
  ↳ 疑似表选错（golden 未用）：['orders']

【Q078】2026 年 8 月各工单类型解决率
  golden   : SELECT ticket_type, SUM(CASE WHEN ticket_status IN ('resolved', 'closed') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type ORDER BY resolution_rate DESC
  生成     : SELECT ticket_type, SUM(CASE WHEN ticket_status = 'resolved' THEN 1 ELSE 0 END) / COUNT(*) AS resolution_rate FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' GROUP BY ticket_type LIMIT 1000

【Q080】2026 年 8 月高满意度工单占比
  golden   : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS high_satisfaction_ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' AND satisfaction_score IS NOT NULL
  生成     : SELECT SUM(CASE WHEN satisfaction_score >= 4 THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM after_sales WHERE created_at >= '2026-08-01' AND created_at < '2026-09-01' LIMIT 1000
  ↳ 列名不符：实际=['ratio'] 预期=['high_satisfaction_ratio']

==============================================================
