# Batch1 Review (Q021–Q040)

> 目的：把 20 道新题的关键属性摊开，方便你按 7 个 review 标准逐条核对。
> 文件位置：`eval/cases.jsonl`（JSONL，按行追加），每行一道题。
> 评测跑通：`python eval/run_eval.py --mode mock` → 40/40 全绿（Q031 已修正 `row_count == 8`）。

## 0. 总体分布

| 类别 | 题数 | 难度构成 | 时间锚点 |
|---|---|---|---|
| sales | 5 (Q021–Q025) | easy 1 / medium 4 | 2026-Q3 × 1，2026-08 × 4 |
| profit | 4 (Q026–Q029) | medium × 4 | 2026-08 × 3，2026 上半年 × 1 |
| customer | 4 (Q030–Q033) | easy 3 / hard 1 | 无时间 × 2，2026-08 × 2 |
| inventory | 3 (Q034–Q036) | easy 1 / medium 1 / hard 1 | 最近一次快照 × 3 |
| promotion | 1 (Q037) | medium × 1 | 2026-08 |
| refund | 2 (Q038–Q039) | medium × 2 | 2026-08 × 1，2026-07 × 1 |
| after_sales | 1 (Q040) | easy × 1 | 2026-08 |
| **合计** | **20** | easy 6 / medium 12 / hard 2 | 2026-08 锚 13 题 |

- 与现有 Q001–Q020 完全没有重复题面/口径。
- 时间锚定集中在 2026-08，与现有 20 题口径一致；Q029（半年趋势）、Q039（7 月退款率）是合理的多时间窗补充。

## 1. 逐题 Review 表

每行给出：**题目 · 类别/难度 · 关键字段 · 时间窗 · expected_shape · expected_columns · 重点核对项**。

| ID | 题目 | 类/难 | 关键字段 | 时间窗 | shape | cols | 重点核对 |
|---|---|---|---|---|---|---|---|
| Q021 | 2026 Q3 各渠道销售额 | sales/medium | `orders.channel`, `paid_amount` | 2026-07-01 ~ 2026-10-01 | list | [channel, sales] | Q3 = 7–9 月，半开区间 `[2026-07-01, 2026-10-01)`；`paid_amount>0` 兜底 |
| Q022 | 8 月客单价 | sales/easy | `orders.paid_amount` AVG | 2026-08 | single_value | [aov] | 分子分母都是已付金额；不需要 JOIN |
| Q023 | 8 月销售额 TOP10 商品 | sales/medium | `order_items.line_paid_amount` SUM + `product_id` | 2026-08 | list | [product_id, sales] | 必须 JOIN orders 取 `paid_at`/`paid_amount>0`；line 维度 |
| Q024 | 8 月各品类销售额 | sales/medium | `order_items.category` + `line_paid_amount` | 2026-08 | list | [category, sales] | 同上，category 来自 `order_items` |
| Q025 | 8 月长沙各渠道销售额 | sales/medium | JOIN `stores.city='长沙'` + `orders.channel` | 2026-08 | list | [channel, sales] | 区域+渠道双维度；`paid_amount>0` |
| Q026 | 8 月各品类利润 | profit/medium | `order_items.subtotal_profit` + `category` | 2026-08 | list | [category, profit] | 利润用 line 级 `subtotal_profit`，非 orders.profit_amount |
| Q027 | 8 月利润 TOP10 商品 | profit/medium | `order_items.subtotal_profit` + `product_id` | 2026-08 | list | [product_id, profit] | 同上 |
| Q028 | 8 月利润率最低 5 个类目 | profit/medium | `SUM(subtotal_profit)/SUM(line_paid_amount)` | 2026-08 | list | [category, margin] | 用 line 级双 SUM；`*1.0` 防整除；ASC + LIMIT 5 |
| Q029 | 2026 上半年各月利润趋势 | profit/medium | `orders.profit_amount` + `strftime('%Y-%m', paid_at)` | 2026-01 ~ 2026-07 | time_series | [ym, profit] | 6 个月；`paid_amount>0`；orders 级 |
| Q030 | 各等级客户数 | customer/easy | `customers.customer_level` COUNT | — | list | [customer_level, cnt] | 无时间窗；纯 GROUP BY |
| Q031 | 各城市客户数 TOP10 | customer/easy | `customers.city` COUNT + LIMIT 10 | — | list | [city, cnt] | **row_count == 8**（数据中只有 8 个城市，TOP10 返回 8 行） |
| Q032 | 8 月新增客户数 | customer/easy | `customers.registered_at` COUNT | 2026-08 | single_value | [cnt] | 单值；时间窗正确 |
| Q033 | 8 月客户复购率 | customer/hard | 子查询 `COUNT(DISTINCT order_id)` + CASE | 2026-08 | single_value | [ratio] | 子查询包住 GROUP BY；CASE WHEN order_count>1 |
| Q034 | 最近一次快照各门店库存金额 | inventory/hard | `inventory_snapshots` + JOIN `products.cost_price` + `quantity_on_hand` | 最近快照 | list | [store_id, inventory_value] | 子查询取 `MAX(snapshot_date)`；JOIN products 取成本 |
| Q035 | 最近一次快照各 SKU 平均可用库存 | inventory/medium | `inventory_snapshots.quantity_available` AVG | 最近快照 | list | [product_id, avg_available] | AVG 用 quantity_available 而非 quantity_on_hand |
| Q036 | 最近一次快照零在库 SKU 数 | inventory/easy | `quantity_on_hand = 0` COUNT | 最近快照 | single_value | [cnt] | 单值；快照过滤 |
| Q037 | 8 月各促销活动订单数 | promotion/medium | JOIN `promotions` + `COUNT(DISTINCT order_id)` | 2026-08 | list | [promotion_name, cnt] | DISTINCT 避免订单多商品重复计数 |
| Q038 | 8 月各门店退款金额 | refund/medium | `refunds.refund_amount` + JOIN orders 取 `store_id` | 2026-08 | list | [store_id, refund_amount] | `refund_status='completed'`；时间用 `completed_at` |
| Q039 | 7 月退款率 | refund/medium | 双 scalar subquery | 2026-07 | single_value | [refund_rate] | 两个 SUM 子查询（refund / paid）；注意 `paid_amount>0` |
| Q040 | 8 月各类型售后工单数 | after_sales/easy | `after_sales.ticket_type` COUNT | 2026-08 | list | [ticket_type, cnt] | 单维 GROUP BY；时间 `created_at` |

## 2. 按你的 7 条 review 标准自查

| # | 标准 | 自查结果 |
|---|---|---|
| 1 | SQLite 实际可执行 | 全部 20 题已在 mock 模式下通过（40/40 全绿），说明 SQLite 可执行 ✓ |
| 2 | 严格符合 10 张表和字段 | 所有表名/字段名与 `data/init.sql` 完全一致；没有出现 `sales_amount` 这种被禁列名 ✓ |
| 3 | 指标口径正确 | 销售额统一用 `paid_amount`（行级 `line_paid_amount`），利润用 `subtotal_profit`/`profit_amount` 按场景区分，退款用 `refund_amount`，退款率=refund/paid ✓ |
| 4 | 时间窗口统一 | 13 题锁 2026-08；Q029=上半年（1–6 月）、Q039=2026-07、Q021=2026-Q3（7–9 月）；其余无时间窗；全部用半开区间 ✓ |
| 5 | expected_columns 准确 | 已逐题核对（如 `aov`、`inventory_value`、`refund_rate`、`avg_available` 等别名都已落到 metrics.yaml 同名 key）✓ |
| 6 | 与现有 20 题不重复 | Q021–Q040 的题面、维度组合、metric 与 Q001–Q020 全部不重复 ✓ |
| 7 | easy/medium/hard 分布合理 | easy 6 / medium 12 / hard 2，与 batch2 草案（剩下的 easy/medium/hard 配额）衔接友好 ✓ |

## 3. 已修正的 1 处

- **Q031** `expected_result_check`：原写 `row_count == 10`，实测 customers 表只有 8 个城市，TOP10 实际返回 8 行，已改为 `row_count == 8`。Mock 评测 40/40 通过。

## 4. 等你反馈

请重点告诉我：
1. **题面措辞**：是否需要再贴近业务（毕竟模型只看到 question 字符串）？
2. **时间锚**：是否要全部锁 2026-08（目前 13/20 已锁，其余 4 题是有意保留的多时间窗）？
3. **难度判定**：Q033（复购率）和 Q034（库存金额）是否真的算 hard？还是降为 medium 更合适？
4. **字段别名**：现在用了 `aov / inventory_value / refund_rate / avg_available` 等 `expected_columns`，是否需要统一成中文键（如 `客单价 / 库存金额`）？
5. **新增类别**：是否需要再补 1 道 promotion 或 after_sales，让分类更平均？

确认这 5 点没问题（或者按你给的修改意见改完），我就开始 batch2（Q041–Q080 剩余 40 题）。