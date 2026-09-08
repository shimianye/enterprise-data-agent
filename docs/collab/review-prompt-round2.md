# Prompt 与结果诊断（第二轮）

> 负责人：WorkBuddy（夜灯）｜2026-09-07
> 背景：第二轮真实评测——结果正确率 31.6% → 42.1%，Prompt 修复有效但仍有"过度分析/擅自扩展答案"。

## 1. 第二轮基线

| 指标 | 第一轮 | 第二轮 |
|---|---|---|
| SQL 可执行率 | 95.0% | 95.0% |
| 结果形状正确率 | 95.0% | 90.0% |
| **结果正确率** | **31.6%** | **42.1%** |

形状正确率略降（90%）是因为本轮模型"多返回列"（如 Q020 返回 3 列），正是本轮要治的"擅自扩展答案"。

## 2. 错误归类（本轮 9 个典型）

| 类型 | 表现 | 对应题 |
|---|---|---|
| 擅自换事实源 | 利润本可直接 orders.profit_amount，改明细聚合 | Q005 |
| 擅自扩展枚举 | 加入 Schema 未约定的客户等级 | Q009 |
| 时间字段选错 | paid_at → created_at | Q010, Q018 |
| 擅自 JOIN 维度 | 加 JOIN、加展示列、改指标含义 | Q011/Q012/Q013 |
| 擅自改聚合 | SUM(CASE)/COUNT(*) → 复杂 COUNT(DISTINCT CASE) | Q014 |
| 合并口径 | 两个独立时间口径错误合并到同一 JOIN | Q017 |
| 擅自改问题 | "最常见退款原因" → 退款金额 + 错时间字段 | Q018 |
| 多返回列 | 要比例，返回总量+已解决+百分比 3 列 | Q020 |

共同根因：**模型把"回答问题"理解成了"分析问题"，擅自增加维度、列、口径**。

## 3. 本轮升级：形状约束 + 黄金指标 + Few-shot

上一轮只加了硬规则，这一轮不再堆规则，而是加**答案形状约束**和**Few-shot 示范**。

### 3.1 答案形状约束（新增规则）

```
7. Output shape MUST obey the question:
   - "总额/比例/数量/平均值" → return exactly ONE metric column.
   - "排行/最高的/最多的" → return ONLY the requested dimension column + ONE metric column.
   - Never add explanation columns, auxiliary columns, or extra aggregates.
```

### 3.2 黄金指标优先（新增规则）

```
8. Golden metrics:
   - 总利润/利润 → use orders.profit_amount directly, do NOT aggregate order_items.
   - 库存问题 → default to inventory_snapshots only, no dimension JOIN.
   - 退款原因 → filter by requested_at.
   - 退款率 → two independent scalar subqueries, never JOIN the funds fact tables.
```

### 3.3 四条 Few-shot（已对齐 Schema，直接粘贴进 system prompt）

```
Examples:

Q: 2026 年 8 月的总销售额
SQL: SELECT SUM(paid_amount) AS sales FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0

Q: 金卡及以上等级客户占比
SQL: SELECT SUM(CASE WHEN customer_level IN ('金卡', '铂金') THEN 1 ELSE 0 END) / COUNT(*) AS ratio FROM customers

Q: 最近一次快照中库存低于安全线的 SKU 数量
SQL: SELECT COUNT(*) AS cnt FROM inventory_snapshots WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory_snapshots) AND quantity_available < reorder_level

Q: 2026 年 8 月的退款率（退款金额占销售额比例）
SQL: SELECT (SELECT SUM(refund_amount) FROM refunds WHERE completed_at >= '2026-08-01' AND completed_at < '2026-09-01' AND refund_status = 'completed') / (SELECT SUM(paid_amount) FROM orders WHERE paid_at >= '2026-08-01' AND paid_at < '2026-09-01' AND paid_amount > 0) AS refund_rate
```

> 四条分别示范：单指标聚合 / 单表比例 / 最新快照子查询 / 两独立子查询比例。
> 第 4 条直接对应 Q017「退款率必须两个独立子查询、不能 JOIN」的教训。

## 4. 结果列约束（已交付）

`cases.jsonl` 已加 `expected_columns`（每题预期返回的列名集合），`run_eval.py` 已加：

- `check_columns()`：结果列名精确匹配，多列/少列/改名都判不一致
- 列不符时 **shape_ok 置 False**（即"多返回列 = 形状不符"）
- 报告新增「结果列正确率」指标 + 逐题 `↳ 列不符：实际=... 预期=...`

Q020 这类"要 1 列返回 3 列"的题，现在会被形状层直接抓出来。

### 诊断循环（不变）

```bash
LLM_MODE=real LLM_API_KEY=sk-xxx python eval/run_eval.py \
    --report eval/report.md --save-sql eval/sql_dump.jsonl
# 看「结果列正确率」+「结果错误明细」逐题 diff
```

## 5. 目标

- 本轮：42.1% → 60%+（形状约束 + Few-shot + 列约束三管齐下）
- 达到 60% 后再扩 80 题；若仍有顽固题（如 Q007 环比两窗口 CTE），补第 5 条 Few-shot（CTE 环比）
