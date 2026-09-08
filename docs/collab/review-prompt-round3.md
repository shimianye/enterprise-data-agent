# Prompt 与结果诊断（第三轮 + 评测口径拆分）

> 负责人：WorkBuddy（夜灯）｜2026-09-07
> 背景：第三轮真实评测——结果正确率 42.1% → 75%（Few-shot + 形状约束有效），但"结果形状正确率 30%"暴露评测口径问题。

## 1. 第三轮基线

| 指标 | 第二轮 | 第三轮 |
|---|---|---|
| SQL 可执行率 | 95.0% | 100.0% |
| ~~结果形状正确率~~ | 90.0% | **30%（评测过严）** |
| **结果正确率** | 42.1% | **75%** |

75% 是一次实打实的胜利。30% 是"严格列名匹配"暴露的评测口径问题——大多是合法别名差异（`total_quantity` vs `total_qty`、`month` vs `ym`），不是 SQL 真的错。

## 2. 评测口径拆分（已实现）

把"形状"拆成**两个互不污染的指标**：

| 指标 | 含义 | 算法 | 用途 |
|---|---|---|---|
| **结果结构正确率** | 行形状 + 列数 | `check_shape` + `len(actual)==len(expected)` | 真正的结构性约束，**别名无关** |
| **结果列名规范率** | 列名是否与黄金一致 | 严格集合匹配 | 风格/字段指标，能抓到 Q012 类真实字段错 |
| 结果正确率 | 结果值与黄金 SQL 一致 | `results_equal`（浮点+行序无关） | 业务正确性 |

之前"结果形状正确率"把结构和列名混在一起，把合法别名算成错——口径过严。

### 验证（合成用例）

| 场景 | 结构 | 列名 | 解读 |
|---|---|---|---|
| 别名差异（`total_quantity` vs `total_qty`）| ✓ | ✗ | 结构正确，列名风格差异 |
| 多列（`store_id, stockout_rate, store_name`）| ✗ | ✗ | 真实错误，多返回列 |
| 完全匹配 | ✓ | ✓ | 都对 |
| 少列 | ✗ | ✗ | 真实错误，缺列 |

合成测试 `python eval/run_eval.py` + 4 个手工用例，全部按预期判定。

## 3. 三个剩余真实错误 + Prompt 改法

第三轮 result_correct 75%，剩 25%（约 5 题）里 Q010/Q012/Q013 是真实错误，区别于"别名"。

### Q010：下单/复购时间字段用错

- 问题：复购客户数用了 `created_at`，黄金用 `paid_at`
- 根因：`created_at` 含未支付/取消订单，`paid_at` 才是真实成交时间
- 建议加规则（第 9 条）：

```
9. 时间字段语义：
   - orders 事实过滤时间默认用 paid_at（实付时间，即真实成交）
   - created_at 含未支付/取消订单，统计成交/销售/客户行为时不用
   - refunds 过滤用 completed_at（退款完成时间）或 requested_at（申请时间，按语义选）
   - inventory 用 snapshot_date
```

### Q012：库存字段语义错

- 问题：库存量排行用了 `quantity_available`，黄金用 `quantity_on_hand`
- 根因：两者不同——`quantity_on_hand` 是总在库，`quantity_available` = on_hand - reserved（可用）
- 建议加规则（第 10 条）：

```
10. 库存字段语义：
    - 库存量/在库 = inventory_snapshots.quantity_on_hand
    - 可用库存 = quantity_available（on_hand - reserved）
    - 安全线/补货线 = reorder_level
    - 缺货 = quantity_available = 0 或 < reorder_level
```

### Q013：缺货率多返回 `store_name`

- 问题：返回 `store_id, stockout_rate, store_name` 三列，黄金只两列
- 根因：模型"擅自加列"——上一轮已加规则 7（形状约束），仍复发
- 建议加强：把规则 7 写得更硬，或在 Few-shot 第 2 条后补一条"返回 dimension + 单一指标，不要额外展示列"

```
7'. (强化) 排行类问题只返回要求的 dimension + 单一 metric，不要 JOIN 展示额外列（如门店名等）。
     问"门店 X 的 Y 率"→ 返回 (门店标识, Y率)，不要 (门店标识, Y率, 门店名)。
```

## 4. 建议顺序

1. **不要立即继续堆 Prompt**。先把 Q010/Q012/Q013 的真实错误用上面的 3 条小规则 + 1 条强化修掉。
2. 重跑真实评测，预期：result_correct 75% → 85%+，列名规范率 30% → ~50%（Q010/Q012/Q013 修好后会升一档，剩下的就是合法别名了）。
3. 达 85% 后扩 80 题。扩 80 时用"结果结构正确率"作为主指标（不被别名污染），用"列名规范率"挑需要 Prompt 改的真实字段错。

## 5. 运行

```bash
LLM_MODE=real LLM_API_KEY=sk-xxx python eval/run_eval.py \
    --report eval/report.md --save-sql eval/sql_dump.jsonl
```

报告现在会分别给出「结果结构正确率」「结果列名规范率」「结果正确率」三条，按这次拆分的口径判定。
