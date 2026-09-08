# Batch2 Review (Q041–Q080)

> 目的：按 Batch1 同样的 7 条标准，把 Batch2 40 题的关键属性摊开供你 review。
> 文件位置：`eval/cases.jsonl`（JSONL，按行追加），`eval/_append_batch2.py` 是一次性追加脚本。
> 评测跑通：`python eval/run_eval.py --mode mock --db data/enterprise.db --cases eval/cases.jsonl --report eval/report-batch2-mock.md --save-sql eval/sql_dump-batch2.jsonl`
> 最终结果：**80/80 全绿**（SQL 可执行率 / 结构 / 列名 / 行数 / 结果正确率全部 100%）

## 0. 总体分布（Batch1 + Batch2 合计 80 题）

| 类别 | 目标 | 当前 | Batch2 新增 | 难度构成（Batch2） |
|---|---|---|---|---|
| sales | 16 | **16** ✓ | 7 (Q041–Q047) | easy 2 / medium 4 / hard 1 |
| profit | 12 | **12** ✓ | 5 (Q048–Q052) | easy 1 / medium 3 / hard 1 |
| customer | 12 | **12** ✓ | 5 (Q053–Q057) | easy 1 / medium 3 / hard 1 |
| inventory | 12 | **12** ✓ | 6 (Q058–Q063) | easy 1 / medium 4 / hard 1 |
| promotion | 8 | **8** ✓ | 5 (Q064–Q068) | easy 1 / medium 2 / hard 2 |
| refund | 12 | **12** ✓ | 7 (Q069–Q075) | easy 1 / medium 4 / hard 2 |
| after_sales | 8 | **8** ✓ | 5 (Q076–Q080) | easy 2 / medium 2 / hard 1 |
| **合计** | **80** | **80** ✓ | **40** | **easy 8 / medium 24 / hard 8** |

- 全 80 题难度汇总：**easy 20 / medium 48 / hard 12**（hard 占比 15%，主要给同比/环比/复购分层/库存周转/滞销/促销对比/退款+售后关联）
- 时间锚定多样性：13 题锁 2026-08；Q045=2026 vs 2025 同比；Q046=8 月 vs 7 月环比；Q051=H1 同比；Q052=近 3 月；Q074=周维度；Q056/Q057/Q067=跨期/分层

## 1. Hard 题清单（12 道，验证"用户定义的 hard 标准"）

| ID | 题目 | 难度特征 |
|---|---|---|
| Q007 | 8 月订单量同比（Batch1） | 同比 + scalar subquery |
| Q010 | 8 月客户分层贡献（Batch1） | 复购分层 + subquery |
| Q033 | 8 月客户复购率（Batch1） | 子查询 + CASE |
| Q045 | 8 月销售额同比去年 8 月 | **同比 + scalar subquery** |
| Q046 | 8 月各门店环比 7 月 | **环比 + CASE WHEN** |
| Q051 | 2026 H1 vs 2025 H1 利润对比 | **同比 + line 级 + 半年** |
| Q056 | 复购分层 1-3/4-6/7+ | **复购分层 + 子查询 + CASE** |
| Q061 | 近 90 天零销量 SKU | **滞销识别 + NOT EXISTS** |
| Q067 | 促销 vs 非促销订单对比 | **促销前后对比** |
| Q068 | 各促销类型 ROI | **ROI + NULLIF 防除零** |
| Q073 | 退款订单的售后工单率 | **退款+售后关联 + EXISTS** |
| Q075 | 多次退款客户数 | **HAVING + subquery** |

覆盖了你点名的 6 类 hard 题型（同比/环比 / 复购分层 / 库存周转或滞销 / 促销前后对比 / 退款率与售后关联 / 多层子查询）。Q052 近 3 月利润率算 medium（仅 strftime + ratio，未跨年）。

## 2. Batch2 逐题 Review 表（40 题）

每行：**题目 · 类/难 · 关键字段 · 时间窗 · shape · cols · 重点核对项**。

### Sales (Q041–Q047)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q041 | 8 月各门店日均销售额 | sales/easy | `orders.paid_amount` SUM / 31 | 2026-08 | list | [store_id, daily_avg_sales] | 月按 31 天固定除，*1.0 防整除 |
| Q042 | 8 月线上 vs 线下销售额对比 | sales/medium | `channel` GROUP BY | 2026-08 | list | [channel, sales] | 实际有 3 个渠道（电商/小程序/门店），row_count==3 |
| Q043 | 8 月订单金额分布 | sales/medium | CASE WHEN 分桶 | 2026-08 | list | [bucket, cnt] | 4 桶（<100 / 100-500 / 500-2000 / ≥2000） |
| Q044 | 近一年新客与老客销售额对比 | sales/medium | JOIN customers + registered_at 分层 | 付费 2025-08~2026-08；注册分界 2024-08 | list | [customer_type, sales] | 数据注册截止 2025-05；用近 12 月对齐窗口；2 行 |
| Q045 | 8 月销售额同比去年 8 月 | sales/hard | scalar subquery 跨年 | 2026-08 vs 2025-08 | single_value | [yoy_growth] | 两个子查询相减 |
| Q046 | 8 月各门店销售额环比 7 月 | sales/medium | 跨月 CASE WHEN | 2026-07+08 | list | [store_id, mom_growth] | 一窗口覆盖两月，CASE WHEN 分流 |
| Q047 | 8 月单笔最大订单金额 | sales/easy | MAX(paid_amount) | 2026-08 | single_value | [max_order] | 单值 |

### Profit (Q048–Q052)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q048 | 8 月毛利总额 | profit/easy | SUM(subtotal_profit) | 2026-08 | single_value | [profit] | JOIN orders 取 paid_at>0 |
| Q049 | 8 月各品牌利润 TOP10 | profit/medium | JOIN order_items.brand | 2026-08 | list | [brand, profit] | brand 来自 order_items；line 级 |
| Q050 | 8 月各门店利润 | profit/medium | JOIN orders.store_id | 2026-08 | list | [store_id, profit] | line 级利润 |
| Q051 | 2026 H1 vs 2025 H1 利润对比 | profit/hard | scalar subquery 跨年 | 2026-01~07 vs 2025-01~07 | single_value | [yoy_profit_growth] | line 级双 scalar |
| Q052 | 近 3 月各月利润率 | profit/medium | strftime + 双 SUM 比例 | 2026-06~09 | time_series | [ym, margin] | 3 个月窗口 |

### Customer (Q053–Q057)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q053 | 各等级客户城市分布 | customer/easy | GROUP BY customer_level, city | — | list | [customer_level, city, cnt] | 二维 GROUP BY |
| Q054 | 8 月付费客户数 | customer/medium | COUNT(DISTINCT customer_id) | 2026-08 | single_value | [cnt] | 去重 |
| Q055 | 8 月客单价分段客户数 | customer/medium | 子查询 AVG + CASE 分箱 | 2026-08 | list | [bucket, cnt] | 4 桶（<100/100-500/500-2000/≥2000） |
| Q056 | 8 月复购分层 1-3/4-6/7+ | customer/hard | 子查询 + CASE BETWEEN | 2026-08 | list | [repurchase_tier, customer_count] | 复购分层 |
| Q057 | 8 月高/中/低价值客户销售额 | customer/medium | 子查询 SUM + CASE 分层 | 2026-08 | list | [tier, tier_sales] | 三层（≥5000/≥1000/<1000） |

### Inventory (Q058–Q063)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q058 | 最近快照全公司在库总量 | inventory/easy | SUM(quantity_on_hand) | 最近快照 | single_value | [total_on_hand] | 全公司 SUM |
| Q059 | 最近快照各门店缺货 SKU | inventory/medium | quantity_available=0 GROUP BY | 最近快照 | list | [store_id, sku_count] | 缺货 = 可销=0 |
| Q060 | 最近快照低于安全线 SKU 数 | inventory/medium | quantity_available<reorder_level | 最近快照 | single_value | [low_stock_cnt] | 预警 |
| Q061 | 近 90 天零销量 SKU | inventory/hard | NOT EXISTS + JOIN | 付费 2026-05-10~2026-08-09 | single_value | [slow_moving_cnt] | **滞销识别** |
| Q062 | 最近快照各品类可销库存量 | inventory/medium | JOIN products.category | 最近快照 | list | [category, available_qty] | 通过 product_id JOIN 取 category |
| Q063 | 最近快照各门店安全线达标率 | inventory/medium | CASE WHEN + ratio | 最近快照 | list | [store_id, pass_rate] | >=reorder_level 占比 |

### Promotion (Q064–Q068)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q064 | 8 月促销订单数 | promotion/easy | promotion_id IS NOT NULL | 2026-08 | single_value | [cnt] | 简单过滤 |
| Q065 | 8 月各促销类型销售额 | promotion/medium | JOIN promotions.promotion_type | 2026-08 | list | [promotion_type, sales] | 按类型聚合 |
| Q066 | 8 月各促销活动优惠总额 | promotion/medium | SUM(o.discount_amount) | 2026-08 | list | [promotion_name, discount_total] | 订单级 discount_amount |
| Q067 | 8 月促销 vs 非促销订单对比 | promotion/hard | CASE WHEN promotion_id IS NULL | 2026-08 | list | [order_type, sales] | 2 行 |
| Q068 | 8 月各促销类型 ROI | promotion/hard | NULLIF 防除零 | 2026-08 | list | [promotion_type, roi] | ROI=(sales-discount)/discount |

### Refund (Q069–Q075)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q069 | 8 月退款订单数 | refund/easy | COUNT(DISTINCT order_id) | 2026-08 | single_value | [cnt] | completed only |
| Q070 | 8 月各退款原因占比 | refund/medium | GROUP BY refund_reason | 2026-08 | list | [refund_reason, cnt] | 退款原因 |
| Q071 | 8 月各品类退款率 | refund/medium | LEFT JOIN refunds + 比率 | 2026-08 | list | [category, refund_rate] | 行级 category LEFT JOIN |
| Q072 | 8 月退款处理平均时长 | refund/medium | julianday() 日期差 | 2026-08 | single_value | [avg_days] | completed 状态 |
| Q073 | 8 月有退款订单的售后工单率 | refund/hard | EXISTS + CASE WHEN | 2026-08 | single_value | [ticket_refund_ratio] | **退款+售后关联** |
| Q074 | 8 月各周退款金额趋势 | refund/medium | strftime '%Y-%W' | 2026-08 | time_series | [yweek, refund_amount] | 周维度 |
| Q075 | 8 月多次退款客户数 | refund/hard | HAVING COUNT(refund_id)>=2 | 2026-08 | single_value | [cnt] | 多退款客户 |

### After-sales (Q076–Q080)

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q076 | 8 月各工单状态数 | after_sales/easy | GROUP BY ticket_status | 2026-08 | list | [ticket_status, cnt] | 状态分布 |
| Q077 | 8 月首次响应平均时长 | after_sales/medium | AVG(response_time_minutes) | 2026-08 | single_value | [avg_response_minutes] | IS NOT NULL 过滤 |
| Q078 | 8 月各工单类型解决率 | after_sales/medium | CASE WHEN IN ('resolved','closed') | 2026-08 | list | [ticket_type, resolution_rate] | 比率 |
| Q079 | 8 月涉及退款的工单占比 | after_sales/hard | EXISTS + refunds | 2026-08 | single_value | [refund_ticket_ratio] | 退款工单关联 |
| Q080 | 8 月高满意度工单占比 | after_sales/easy | CASE WHEN satisfaction_score>=4 | 2026-08 | single_value | [high_satisfaction_ratio] | 4-5 分为高 |

## 3. 自查（按你的 7 条标准）

| # | 标准 | 自查结果 |
|---|---|---|
| 1 | SQLite 实际可执行 | 80/80 mock 全绿 ✓ |
| 2 | 10 张表/字段严格对齐 | 所有表名/字段与 `data/init.sql` 一致；新增用到 `channel`（电商/小程序/门店）、`discount_amount`、`promotion_type`、`refund_reason`、`julianday()`、`response_time_minutes`、`satisfaction_score`、`quantity_reserved`、`reorder_level` 全部存在 ✓ |
| 3 | 指标口径正确 | sales=paid_amount（line=line_paid_amount）；profit=line 级 subtotal_profit；退款=refunds.refund_amount + completed；ROI=(sales-discount)/discount；周转率/滞销=近 90 天 ✓ |
| 4 | 时间窗口统一性 | 半开区间全部使用；时间锚定多样（同比/环比/单月/季度/近 12 月）✓ |
| 5 | expected_columns 准确 | 全部使用英文键；如 `daily_avg_sales`、`slow_moving_cnt`、`refund_ticket_ratio`、`roi` 都已落到 mock 结果 ✓ |
| 6 | 与 Batch1/原 20 题不重复 | Q041–Q080 题面/口径与 Q001–Q040 完全不重叠 ✓ |
| 7 | easy/medium/hard 合理 | hard 严格按你给的 6 类（同环比/复购分层/库存周转/促销对比/退款关联/HAVING 多次退款）✓ |

## 4. 已修正的 2 处（mock 评测暴露）

| ID | 原问题 | 修正 | 修正原因 |
|---|---|---|---|
| Q042 | `row_count == 2` | `row_count == 3` | channel 字段实际有 3 个枚举值（电商平台/小程序/门店），不是 2 |
| Q044 | `2026-08 新客与老客销售额` + `row_count == 2` | 题面改为「近一年新客与老客销售额对比」+ 窗口调整为付费 2025-08~2026-08，注册分界 2024-08 | 数据中 customers 注册截止 2025-05，原 8 月口径 0 新客户 → GROUP BY 只剩 1 行 |

## 5. 改动汇总

| 文件 | 改动 |
|---|---|
| `eval/cases.jsonl` | 40 → 80 题（Q041–Q080 追加） |
| `eval/_append_batch2.py` | 一次性追加脚本（**路径 bug 已修复**：`Path(__file__).resolve().parent / "cases.jsonl"`，不再误写到项目根） |
| `eval/cases.jsonl` | 同步 Q034 难度：hard → medium（按你的拍板） |
| `eval/cases.jsonl` | Q042 row_count==2 → ==3；Q044 题面/口径调整 |
| `eval/report-batch2-mock.md` | 新生成 mock 评测报告（80/80） |
| `eval/sql_dump-batch2.jsonl` | 新生成 mock SQL 明细 |

## 6. 路径 bug 说明（自我提醒）

第一次跑 `_append_batch2.py` 时，因为 `Path(__file__).resolve().parents[1]` 把 `cases.jsonl` 误写到了项目根目录 `D:\develop\enterprise-data-agent\cases.jsonl`（应该是 `eval/` 内）。已修正为 `Path(__file__).resolve().parent / "cases.jsonl"`，并把误写到根目录的 40 行内容合并到正确位置后删除了根目录文件。**目前 `eval/cases.jsonl` 是唯一权威来源**。

## 7. 等你反馈

请重点告诉我：
1. Q042（3 个渠道）/ Q044（"近一年"对齐窗口）这两个修正是否符合预期
2. Hard 题分布是否符合"同比/环比/复购分层/库存周转/滞销/促销对比/退款+售后关联"六类
3. 时间锚定多样性（季度/半年/近 12 月/同比/环比）是否需要更激进或更保守
4. 是否需要补充几道**窗口函数**题（如 RANK/ROW_NUMBER 取各品类月度销售 Top 3）？
6. 整体题面措辞是否符合"经营分析口吻"

确认完就可以进入下一阶段：**README + 架构图**（我出）+ **安全题端到端评测**（需真实 LLM runner）+ **前端图表 + NL 解释**（你的）。