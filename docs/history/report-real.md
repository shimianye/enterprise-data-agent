==============================================================
Text2SQL 评测报告
==============================================================

总题数: 20
SQL 可执行率: 19/20 = 95.0%
结果形状正确率: 19/20 = 95.0%
行数校验通过率: 19/20 = 95.0%
结果正确率: 6/19 = 31.6%

--------------------------------------------------------------
ID    状态    形状   结果   耗时     类别/难度
--------------------------------------------------------------
Q001  ✓     ✓    ✓    3293   sales/easy
Q002  ✓     ✓    ✗    2593   sales/medium
Q003  ✓     ✓    ✗    3004   sales/medium
Q004  ✓     ✓    ✓    2623   sales/medium
Q005  ✓     ✓    ✗    2663   profit/easy
Q006  ✓     ✓    ✗    3490   profit/medium
Q007  ✗     ✗    -    0      profit/hard
       ↳ 错误: sql_invalid: ['unknown_column:month', 'unknown_column:sales_amount']
Q008  ✓     ✓    ✓    2500   customer/easy
Q009  ✓     ✓    ✗    2483   customer/medium
Q010  ✓     ✓    ✗    2569   customer/hard
Q011  ✓     ✓    ✗    2116   inventory/easy
Q012  ✓     ✓    ✗    2613   inventory/medium
Q013  ✓     ✓    ✗    2837   inventory/medium
Q014  ✓     ✓    ✗    2518   promotion/medium
Q015  ✓     ✓    ✓    2417   promotion/medium
Q016  ✓     ✓    ✓    2077   refund/easy
Q017  ✓     ✓    ✗    2553   refund/medium
Q018  ✓     ✓    ✗    2020   refund/medium
Q019  ✓     ✓    ✓    2231   after_sales/medium
Q020  ✓     ✓    ✗    2894   after_sales/medium

==============================================================
