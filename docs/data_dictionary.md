# 数据字典（Data Dictionary）

> 本文件是 Text2SQL 评测集与 SQL 安全校验的**业务口径权威来源**。
> 所有 golden_sql、指标定义、Schema 检索都必须与本文件一致。
> Schema 权威来源：`data/init.sql`；指标权威来源：`config/metrics.yaml`。

## 1. 概述

- **数据库**：SQLite（`data/enterprise.db`），只读访问
- **表数量**：10 张核心业务表
- **时间字段**：均为 `TEXT` 类型，格式 `YYYY-MM-DD HH:MM:SS`（ISO 8601）
  - 日期比较依赖字典序 = 时间序（同格式字符串可直接 `>=` / `<` 比较）
  - 月份聚合用 `strftime('%Y-%m', col)`，**不要用** MySQL 的 `DATE_FORMAT`
- **布尔字段**：用 `INTEGER`（`0`/`1`）表达，无 TINYINT
- **主键**：单列 INTEGER 主键，`inventory_snapshots` 为三列复合主键

## 2. 表间关系

```
stores(1) ────< orders(∞) ────< order_items(∞) >──── products(1)
                  │  │
                  │  └────< payments(∞) ────< refunds(∞)
                  │
customers(1) ────< orders
                  │
promotions(1) ───< orders (promotion_id 可空)
                  │
orders ────< after_sales(∞)   (售后工单，服务流，≠ 退款资金流)
stores(1) ────< inventory_snapshots(∞) >──── products(1)
```

关键关系：
- `orders.customer_id` → `customers.customer_id`
- `orders.store_id` → `stores.store_id`
- `orders.promotion_id` → `promotions.promotion_id`（可空 = 无促销）
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`
- `payments.order_id` → `orders.order_id`
- `refunds.order_id` → `orders.order_id`；`refunds.payment_id` → `payments.payment_id`
- `inventory_snapshots` 复合主键 `(store_id, product_id, snapshot_date)`
- `after_sales.order_id` → `orders.order_id`；`after_sales.customer_id` → `customers.customer_id`

**⚠️ 概念区分**：`refunds`（资金流，钱退没退）与 `after_sales`（服务流，人处理没处理）是**两个独立事实表**。退款率查 `refunds`，工单指标查 `after_sales`，不得混用。

## 3. 各表字段明细

### 3.1 stores — 门店维度表

| 字段 | 类型 | 说明 |
|---|---|---|
| store_id | INTEGER PK | 门店 ID |
| store_name | TEXT | 门店名称 |
| city | TEXT | 城市（如「长沙」）|
| region | TEXT | 大区（华中/华东/华南/华北/西南/西北/东北）|
| store_type | TEXT | 门店类型（直营/加盟/体验店）|
| opened_at | TEXT | 开业时间 |
| is_active | INTEGER | 是否营业（1/0）|

### 3.2 customers — 客户维度表

| 字段 | 类型 | 说明 |
|---|---|---|
| customer_id | INTEGER PK | 客户 ID |
| customer_name | TEXT | 客户姓名 |
| gender | TEXT | 性别（M/F）|
| age | INTEGER | 年龄 |
| city | TEXT | 城市 |
| region | TEXT | 大区 |
| customer_level | TEXT | 客户等级（普通/银卡/金卡/铂金）|
| registered_at | TEXT | 注册时间 |

### 3.3 products — 商品维度表

| 字段 | 类型 | 说明 |
|---|---|---|
| product_id | INTEGER PK | 商品 ID |
| sku_code | TEXT UNIQUE | SKU 编码 |
| product_name | TEXT | 商品名称 |
| brand | TEXT | 品牌（如「Apple」「华为」）|
| category | TEXT | 类目（如「智能手机」「配件」）|
| cost_price | NUMERIC | 内部成本价 |
| sale_price | NUMERIC | 标价销售价 |
| list_price | NUMERIC | 吊牌价 |
| launched_at | TEXT | 上架时间 |
| is_active | INTEGER | 是否在售（1/0）|

### 3.4 promotions — 促销活动维度表

| 字段 | 类型 | 说明 |
|---|---|---|
| promotion_id | INTEGER PK | 促销 ID |
| promotion_name | TEXT | 促销名称（注意：字段名是 promotion_name 而非 name）|
| promotion_type | TEXT | 促销类型（满减/折扣/赠品/优惠券）|
| start_at | TEXT | 开始时间 |
| end_at | TEXT | 结束时间 |
| min_amount | NUMERIC | 满减门槛（默认 0）|
| discount_value | NUMERIC | 优惠值/比例 |
| max_discount | NUMERIC | 最大优惠封顶（可空）|
| is_active | INTEGER | 是否启用（1/0）|

### 3.5 orders — 订单事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| order_id | INTEGER PK | 订单 ID |
| order_no | TEXT UNIQUE | 订单编号（SO+日期+序号）|
| customer_id | INTEGER FK | 客户 ID |
| store_id | INTEGER FK | 门店 ID |
| order_status | TEXT | 订单状态（见 §5）|
| order_amount | NUMERIC | 订单原价金额（未减优惠）|
| discount_amount | NUMERIC | 优惠金额 |
| freight_amount | NUMERIC | 运费 |
| **paid_amount** | NUMERIC | **实付金额（销售额事实源）** |
| cost_amount | NUMERIC | 成本金额（汇总）|
| profit_amount | NUMERIC | 利润金额（汇总）|
| item_count | INTEGER | 商品件数 |
| channel | TEXT | 渠道（app/miniprogram/web/offline）|
| promotion_id | INTEGER FK | 促销 ID（可空 = 无促销）|
| created_at | TEXT | 创建时间 |
| paid_at | TEXT | 支付时间（可空）|
| shipped_at | TEXT | 发货时间（可空）|
| delivered_at | TEXT | 签收时间（可空）|
| completed_at | TEXT | 完成时间（可空）|
| cancelled_at | TEXT | 取消时间（可空）|

**时间链约束**：`created_at ≤ paid_at ≤ shipped_at ≤ delivered_at ≤ completed_at`，后续时间不得早于前置时间。

### 3.6 order_items — 订单明细事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| item_id | INTEGER PK | 明细 ID |
| order_id | INTEGER FK | 订单 ID |
| product_id | INTEGER FK | 商品 ID |
| sku_code | TEXT | SKU 编码 |
| brand | TEXT | 品牌 |
| category | TEXT | 类目 |
| quantity | INTEGER | 数量 |
| unit_price | NUMERIC | 单价 |
| unit_cost | NUMERIC | 单位成本 |
| discount_amount | NUMERIC | 明细优惠（按原价占比分摊整单优惠）|
| subtotal_amount | NUMERIC | 明细原价小计（quantity × unit_price）|
| subtotal_cost | NUMERIC | 明细成本小计（quantity × unit_cost）|
| **line_paid_amount** | NUMERIC | **明细实付（≠ orders.paid_amount，不含运费）** |
| **subtotal_profit** | NUMERIC | **明细利润（毛利事实源 = line_paid_amount - subtotal_cost）** |

**⚠️ 字段名陷阱**：
- `orders.paid_amount` = 整单实付（含运费）
- `order_items.line_paid_amount` = 明细实付（不含运费）
- 两者**同名不同义**，Text2SQL 与评测都不得混淆

### 3.7 payments — 支付资金事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| payment_id | INTEGER PK | 支付 ID |
| order_id | INTEGER FK | 订单 ID |
| payment_method | TEXT | 支付方式（wechat/alipay/card/installment）|
| payment_amount | NUMERIC | 支付金额 |
| payment_status | TEXT | 支付状态（success 表示成功）|
| refund_amount | NUMERIC | 已退款金额（默认 0）|
| paid_at | TEXT | 支付时间（可空）|
| transaction_id | TEXT UNIQUE | 交易流水号 |

### 3.8 refunds — 退款资金事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| refund_id | INTEGER PK | 退款 ID |
| order_id | INTEGER FK | 订单 ID |
| payment_id | INTEGER FK | 支付 ID |
| refund_reason | TEXT | 退款原因（质量问题/不想要了/物流问题/描述不符/其他）|
| refund_type | TEXT | 退款类型（仅退款/退货退款/换货）|
| refund_amount | NUMERIC | 退款金额 |
| refund_status | TEXT | 退款状态（**completed 表示退款成功**）|
| requested_at | TEXT | 申请时间 |
| completed_at | TEXT | 完成时间（可空）|

**口径**：退款金额 = `SUM(refund_amount) WHERE refund_status = 'completed'`。
退款总额 ≤ 实付金额；同一订单成功退款累计 ≤ 支付金额。

### 3.9 inventory_snapshots — 库存快照事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| store_id | INTEGER PK | 门店 ID（复合主键之一）|
| product_id | INTEGER PK | 商品 ID（复合主键之一）|
| snapshot_date | TEXT PK | 快照日期（复合主键之一）|
| quantity_on_hand | INTEGER | 在手库存 |
| quantity_reserved | INTEGER | 预留库存 |
| quantity_available | INTEGER | 可用库存（= on_hand - reserved）|
| reorder_level | INTEGER | 补货阈值（安全线）|

**口径**：缺货 = `quantity_available < reorder_level`；缺货率 = `quantity_available = 0` 的记录占比。
断货 SKU（on_hand=0）**仍保留快照记录**，这是缺货率分析的前提。

### 3.10 after_sales — 售后工单事实表

| 字段 | 类型 | 说明 |
|---|---|---|
| ticket_id | INTEGER PK | 工单 ID |
| order_id | INTEGER FK | 订单 ID |
| customer_id | INTEGER FK | 客户 ID |
| ticket_type | TEXT | 工单类型（退款/换货/维修/投诉/咨询）|
| ticket_status | TEXT | 工单状态（见 §5）|
| priority | TEXT | 优先级（low/medium/high/urgent）|
| assigned_to | TEXT | 处理人（可空）|
| created_at | TEXT | 创建时间 |
| first_response_at | TEXT | 首次响应时间（可空）|
| resolved_at | TEXT | 解决时间（可空）|
| closed_at | TEXT | 关闭时间（可空）|
| response_time_minutes | INTEGER | 首响时长（分钟，可空）|
| resolution_time_hours | NUMERIC | 解决时长（小时，可空）|
| satisfaction_score | INTEGER | 满意度评分（1-5，可空）|

**SLA 可空规则**：
- 未首响工单 → `first_response_at` / `response_time_minutes` 为空
- 未解决工单 → `resolved_at` / `resolution_time_hours` 为空
- 仅已关闭工单才有 `satisfaction_score`
- 时间戳是事实源，时长字段是预计算结果（数据生成后校验两者一致）

## 4. 核心业务口径（权威）

> 与 `config/metrics.yaml` 一一对应。评测的「业务口径正确率」以此为准。

| 指标 | key | 表达式 | 关键口径 |
|---|---|---|---|
| 销售额 | sales_amount | `SUM(orders.paid_amount)` | **用 paid_amount，不用 order_amount**；`paid_amount > 0` |
| 订单量 | order_count | `COUNT(DISTINCT orders.order_id)` | 跨明细 JOIN 时**必须 DISTINCT** |
| 客单价 | average_order_value | `AVG(orders.paid_amount)` | 实付金额均值 |
| 毛利 | gross_profit | `SUM(order_items.subtotal_profit)` | **明细利润以 subtotal_profit 为事实源**；运费成本暂忽略，订单级利润可用 `orders.profit_amount` |
| 退款金额 | refund_amount | `SUM(refunds.refund_amount)` | 仅 `refund_status = 'completed'` |
| 售后解决时长 | after_sales_resolution_hours | `AVG(after_sales.resolution_time_hours)` | 已解决工单的平均解决时长 |

### 关键口径陷阱（Text2SQL 必须规避）

1. **销售额 ≠ order_amount**：`order_amount` 是未减优惠的原价，`paid_amount` 才是实付。
2. **销售额过滤用 `paid_amount > 0`**，不是 `order_status <> 'cancelled'`（后者无法排除「已创建未支付」订单）。
3. **JOIN order_items 时订单量/销售额要 `DISTINCT`**：一条订单对应多条明细，直接 SUM 会重复计算。
4. **退款只统计 `refund_status = 'completed'`**：requested/approved 不算实际退款。
5. **售后 ≠ 退款**：`after_sales` 是工单，`refunds` 是资金，两个事实域。

## 5. 状态枚举值（约定）

> 以下为业务约定值，最终以 `data/generate_data.py` 生成的数据为准。

| 字段 | 枚举值 |
|---|---|
| order_status | created / paid / shipped / delivered / completed / cancelled / refunded |
| refund_status | requested / approved / rejected / completed |
| ticket_status | open / in_progress / resolved / closed / escalated |
| payment_status | success / failed / refunded |
| ticket_type | 退款 / 换货 / 维修 / 投诉 / 咨询 |
| refund_type | 仅退款 / 退货退款 / 换货 |
| promotion_type | 满减 / 折扣 / 赠品 / 优惠券 |
| customer_level | 普通 / 银卡 / 金卡 / 铂金 |
| channel | app / miniprogram / web / offline |
| payment_method | wechat / alipay / card / installment |
| store_type | 直营 / 加盟 / 体验店 |
| region | 华中 / 华东 / 华南 / 华北 / 西南 / 西北 / 东北 |

## 6. 时间字段约定

- 所有时间字段为 `TEXT`，格式 `YYYY-MM-DD HH:MM:SS`
- 评测集时间锚点：`AS_OF_DATE = '2026-09-01'`
- 相对时间（「上个月」「最近 30 天」）在评测题中**尽量写成绝对时间**（「2026 年 8 月」）
- 月份聚合：`strftime('%Y-%m', col)`；日期比较：字符串 `>=` / `<`

## 7. 与评测集的关系

- 评测集：`eval/cases.jsonl`（80 题目标，已交付前 20 题）
- 每题的 `golden_sql` 必须严格遵循本文件口径
- `business_metric` 字段引用本文件 §4 的指标名
- SQL 安全校验：`app/security/validator.py` 的白名单 schema 由 `SchemaCatalog.to_table_infos()` 提供，与本文件字段一致
