# 交接状态 Handoff

> 最后更新：2026-09-07 11:09

## 项目当前状态

- 项目目录：`D:\develop\enterprise-data-agent`
- v0 草稿（data/init.sql、data/generate_data.py）**待移动到 `data/_drafts/`**，仅作参考，不进入正式链路
- 数据层设计方案已由用户拍板（下方"已定稿设计"）

## 已定稿设计（2026-09-07 11:09 用户拍板）

### 数据规模
- 10 张核心表
- 5 万订单 / 10 万订单明细
- 1 万客户 / 20 门店
- 12 个月数据（含 24 个库存快照点）
- 覆盖分析场景：销售、利润、客户、库存、促销、退款、履约

### 表结构（10 张）

| # | 表名 | 说明 |
|---|---|---|
| 1 | stores | 门店 |
| 2 | customers | 客户 |
| 3 | products | 商品 |
| 4 | orders | 订单 |
| 5 | order_items | 订单明细 |
| 6 | payments | 支付 |
| 7 | refunds | 退款 |
| 8 | inventory_snapshots | 库存快照 |
| 9 | promotions | 促销活动 |
| 10 | after_sales | 售后工单 |

### 决策 1：库存快照
- 全局商品：约 1500 SKU
- 每店经营：约 300~500 SKU（**非全笛卡尔积**）
- 快照频率：每月 1 日、15 日，12 个月共 24 个快照点
- 预计数据量：20 × 400 × 24 ≈ 19.2 万行
- **断货 SKU 快照 quantity_on_hand=0 仍保留记录**（缺货率分析前提）

### 决策 2：利润字段（明细为事实源，订单存汇总）
- `order_items` 增加：`unit_cost`、`discount_amount`、`subtotal_amount`、`subtotal_cost`、`line_paid_amount`、`subtotal_profit`
  - ⚠️ 明细实付字段命名 **`line_paid_amount`**，避免与 `orders.paid_amount` 混淆
- `orders` 汇总：`cost_amount`、`profit_amount`
- 口径：
  - 明细利润 = 明细实付金额 - 明细成本
  - 订单利润 = SUM(明细利润) + 运费收入（**运费成本暂忽略，全额计入利润**）
- 生成后必须校验：订单汇总值 = 明细汇总值

### 决策 3：促销（一单一促）
- `orders.promotion_id` 外键
- 订单优惠按明细原价占比分摊到 `order_items.discount_amount`
  - 公式：`明细折扣 = 整单折扣 × (明细原价 / 整单原价)`
- 第一版不做满减券/会员折扣/平台券叠加

### 决策 4：售后 SLA
- 字段：`first_response_at`、`resolved_at`、`closed_at`、`response_time_minutes`、`resolution_time_hours`、`satisfaction_score`
- 可空规则：
  - 未首响 → 首响时长为空
  - 未解决 → 解决时长为空
  - 仅已关闭工单才有满意度评分
- 时间戳是事实源，时长是预计算结果；生成后校验两者一致

### 决策 5：业务规则（含退款修正）
- 订单状态机严格：`created → paid → shipped → delivered → completed`，任一节点可 cancelled
- 时间链单调性：后续时间不得早于前置时间
- **已支付未发货的取消订单可退款**
- **已发货订单不能直接取消**（只能走售后/退款）
- **已签收/完成订单 1~30 天内可申请售后退款**
- 退款总额 ≤ 实付金额
- 同一订单成功退款累计 ≤ 支付金额
- 库存变化与销量方向一致，允许补货回升
- 双 11/618/春节/周末/门店地区影响订单概率
- 固定 seed 可重复生成
- 事务 + 幂等重建，失败不留半套数据

### 决策 6：表概念区分
- `refunds` = 资金流（钱退没退）
- `after_sales` = 服务工单（人处理没处理）
- 退款率来自 `refunds`，工单指标来自 `after_sales`，评测题不得混用

## 草稿文件处理

- 移动到 `data/_drafts/v0-init.sql`、`data/_drafts/v0-generate_data.py`
- 正式 `data/init.sql`、`data/generate_data.py` 由用户重新实现

## 评测指标（用户补充，6 个分层指标）

1. SQL 可执行率
2. 结果正确率
3. 结果形状正确率
4. 安全拦截准确率
5. 业务口径正确率
6. 端到端回答成功率

详见 `eval/README.md`。

## 下一步

1. ~~用户回复 5 个待决项~~ ✅ 已定稿
2. 用户整理草稿目录（移动 v0 到 _drafts）
3. 用户重写 `data/init.sql`（10 张表，采纳字段命名修正）
4. 用户重写 `data/generate_data.py`（按业务规则）
5. WorkBuddy 写首批 20 题评测（已交付 eval/cases_draft.jsonl）
6. **主链路开发启动**（13:46）：
   - 用户：SQLite 数据连接、Schema Catalog、Glossary、Text2SQL、Agent 编排
   - WorkBuddy：评测集、文档、只读审查
7. WorkBuddy 写 `docs/data_dictionary.md`（等 Schema 定稿）
8. WorkBuddy 写 `eval/cases.jsonl` 最终版（待 Schema 字段名对齐）
9. 主链路每个模块完成后，WorkBuddy 出 `review-<模块>.md`
