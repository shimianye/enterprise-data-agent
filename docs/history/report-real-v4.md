==============================================================
Text2SQL 评测报告
==============================================================

总题数: 20
SQL 可执行率: 20/20 = 100.0%
结果结构正确率: 20/20 = 100.0%
结果列名规范率: 6/20 = 30.0%
行数校验通过率: 20/20 = 100.0%
结果正确率: 19/20 = 95.0%

--------------------------------------------------------------
ID    状态    结构   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    3083   sales/easy
       ↳ 列名不符（风格/字段）：实际=['sales_amount'] 预期=['sales']
Q002  ✓     ✓    ✓    2801   sales/medium
Q003  ✓     ✓    ✓    2717   sales/medium
       ↳ 列名不符（风格/字段）：实际=['brand', 'total_quantity'] 预期=['brand', 'total_qty']
Q004  ✓     ✓    ✓    2466   sales/medium
       ↳ 列名不符（风格/字段）：实际=['month', 'sales_amount'] 预期=['ym', 'sales']
Q005  ✓     ✓    ✓    2928   profit/easy
       ↳ 列名不符（风格/字段）：实际=['total_profit'] 预期=['profit']
Q006  ✓     ✓    ✓    2453   profit/medium
       ↳ 列名不符（风格/字段）：实际=['category', 'profit_rate'] 预期=['category', 'margin']
Q007  ✓     ✓    ✓    3056   profit/hard
       ↳ 列名不符（风格/字段）：实际=['category', 'growth_rate'] 预期=['category', 'growth']
Q008  ✓     ✓    ✓    2618   customer/easy
       ↳ 列名不符（风格/字段）：实际=['total_customers'] 预期=['cnt']
Q009  ✓     ✓    ✓    2030   customer/medium
Q010  ✓     ✓    ✓    2393   customer/hard
       ↳ 列名不符（风格/字段）：实际=['customer_count'] 预期=['cnt']
Q011  ✓     ✓    ✓    2622   inventory/easy
Q012  ✓     ✓    ✓    2720   inventory/medium
       ↳ 列名不符（风格/字段）：实际=['product_id', 'inventory_quantity'] 预期=['product_id', 'quantity_on_hand']
Q013  ✓     ✓    ✓    2492   inventory/medium
Q014  ✓     ✓    ✗    2746   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_order_ratio'] 预期=['ratio']
Q015  ✓     ✓    ✓    2456   promotion/medium
       ↳ 列名不符（风格/字段）：实际=['promotion_name', 'sales_amount'] 预期=['promotion_name', 'promo_sales']
Q016  ✓     ✓    ✓    2507   refund/easy
       ↳ 列名不符（风格/字段）：实际=['refund_amount'] 预期=['total']
Q017  ✓     ✓    ✓    2364   refund/medium
Q018  ✓     ✓    ✓    2326   refund/medium
Q019  ✓     ✓    ✓    2709   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['avg_first_response_minutes'] 预期=['avg_minutes']
Q020  ✓     ✓    ✓    2164   after_sales/medium
       ↳ 列名不符（风格/字段）：实际=['resolution_rate'] 预期=['ratio']

==============================================================
结果错误明细（golden vs 生成）
==============================================================

【Q014】2026 年 8 月使用促销的订单占比
  golden   : SELECT SUM(CASE WHEN promotion_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0
  生成     : SELECT SUM(CASE WHEN NOT o.promotion_id IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS promotion_order_ratio FROM orders AS o WHERE o.paid_at >= '2026-08-01' AND o.paid_at < '2026-09-01' AND o.paid_amount > 0 LIMIT 1000
  ↳ 列名不符：实际=['promotion_order_ratio'] 预期=['ratio']

==============================================================
