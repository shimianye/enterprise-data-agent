# Prompt 与结果诊断（第一轮）

> 负责人：WorkBuddy（夜灯）｜2026-09-07
> 背景：真实 LLM 评测首轮结果——SQL 可执行率 95%、结果正确率 31.6%（6/19）。
> 结论：链路没问题，**卡在"能执行但口径错"**，问题在 Prompt 对业务口径的约束不够强。

## 1. 现状（首轮真实评测基线）

| 指标 | 值 |
|---|---|
| SQL 可执行率 | 19/20 = 95.0% |
| 结果形状正确率 | 19/20 = 95.0% |
| **结果正确率** | **6/19 = 31.6%** |
| 平均响应 | ~2.6s |

可执行率高说明：安全校验、Schema 召回、SQL 生成链路都通。
结果正确率低说明：**模型没在严格遵循指标口径和 Schema 字段**。

## 2. 根因诊断（两个确定 + 一个普遍）

### 根因 A：Schema 被错标成 "Metric definitions"（确定，必改）

`app/llm/client.py`：
```python
prompt = f"Metric definitions:\n{context}\n\nQuestion: {question}"
```
而 `context` 里既有指标定义、又有 Schema 表结构（`query_service.py` 里拼接）。
整段 Schema 被错误地冠以 "Metric definitions" 标签。

后果：模型看到 `销售额 (sales_amount): SUM(orders.paid_amount)` 后，把指标 key
`sales_amount` 当成字段名直接用——这正是 Q007 `unknown_column:sales_amount`、
`unknown_column:month` 的直接来源（"月份" 被当成字段 `month`）。

### 根因 B：系统提示太弱，缺少强制性规则（确定，必改）

当前 system prompt 只有一句泛泛的：
```
You are a read-only SQLite Text2SQL analyst. Return exactly one SQL SELECT/WITH
statement, no markdown. Use only the supplied schema and metric definitions.
```
没有明确告诉模型：
1. **指标名不是字段名**（销售额 / 毛利 / sales_amount 都不是列，必须按定义展开）
2. **月份分桶必须 `strftime('%Y-%m', <时间列>)`**，不允许凭空造 `month` 列
3. **只能使用 Schema 里字面出现的列名**，禁止发明列
4. **时间过滤用半开区间** `col >= 'YYYY-MM-DD' AND col < 'YYYY-MM-DD'`
5. **指标的"默认过滤"是强制的**（如 `paid_amount > 0`）

### 根因 C：模型把指标描述当"建议"而非"约束"（普遍）

glossary 里其实已经写了 `不使用 order_amount`、`跨明细 JOIN 时必须 DISTINCT`、
`仅统计 refund_status=completed`——但模型选择性忽略。这说明：**这些约束要写成
祈使句、放进 system prompt 强化，而不是只埋在 per-query 的描述里。**

## 3. 六个错误假设 → Prompt 规则映射

| 你的假设 | 对应 Prompt 规则 |
|---|---|
| 1. 漏了 paid_amount > 0 | 指标的"默认过滤"强制包含 |
| 2. 用了 order_amount 而非 paid_amount | 销售额=paid_amount，明写"绝不使用 order_amount" |
| 3. 时间字段选错 | 半开区间 + 明确各事实表的时间列 |
| 4. JOIN 后未去重 | 跨明细 JOIN 计数用 COUNT(DISTINCT) |
| 5. 利润字段错 | 明细粒度毛利 = subtotal_profit |
| 6. 库存快照日期条件不准 | 库存用 snapshot_date + 最新快照 |
| 7. 退款/售后事实表混用 | refunds ≠ after_sales，各自独立 |

## 4. 建议的 Prompt 改法（待你确认后应用）

### 4.1 新的 system prompt（`app/llm/client.py`）

```python
system = (
    "You are a SQLite Text2SQL analyst for a retail business. "
    "Return exactly one read-only SQL statement (SELECT or WITH). No markdown, no explanation.\n"
    "Hard rules:\n"
    "1. Metric names (销售额, 毛利, 订单量, 退款金额, etc.) are NOT column names. "
    "Expand them with the expression in the metric definitions.\n"
    "2. Only use table/column names that literally appear in the schema. Never invent columns "
    "(no 'month', 'sales_amount', 'sales').\n"
    "3. Month/time bucketing MUST use strftime('%Y-%m', <time_column>).\n"
    "4. Time filters MUST be half-open: col >= 'YYYY-MM-DD' AND col < 'YYYY-MM-DD' (the next period's 1st).\n"
    "5. A metric's 默认过滤 (e.g. paid_amount > 0) is mandatory — always include it.\n"
    "6. Order counts joined with order_items MUST use COUNT(DISTINCT orders.order_id).\n"
    "7. 销售额 uses paid_amount (never order_amount). 毛利 at item level uses "
    "order_items.subtotal_profit. 退款 reads refunds (not after_sales). 售后 reads after_sales (not refunds)."
)
```

### 4.2 新的 prompt 模板（修正标签错位）

`app/llm/client.py`：
```python
prompt = f"{context}\n\nQuestion: {question}"
```

`app/agent/query_service.py`（把两段上下文分开贴正确标签）：
```python
context = (
    "业务指标定义（指标名不是字段名，请按定义展开）:\n"
    + self.glossary.prompt_context(metrics)
    + "\n\n数据库表结构:\n"
    + self.catalog.prompt_context(self.catalog.relevant([question] + [m.name for m in metrics]))
)
```

> 关键：让 "Metric definitions" 标签只包指标，Schema 单独贴 "数据库表结构" 标签。

## 5. 差异诊断工具（已交付，配合本轮使用）

`eval/run_eval.py` 已加：
- `--save-sql <path>`：导出每题 `{golden_sql, sql, diff_tags, ...}` 到 JSONL
- `diff_sql(golden, generated)`：自动标注差异，标签覆盖 9 类
  - 缺少业务过滤 paid_amount > 0
  - 指标字段错误（order_amount vs paid_amount / 利润粒度）
  - 时间字段不一致
  - 缺少 strftime 时间分桶
  - 聚合去重缺失（COUNT vs COUNT DISTINCT）
  - 聚合函数不一致
  - 表/JOIN 缺失
  - 疑似表选错
  - 退款/售后事实表混用

### 诊断循环

```bash
# 1. 跑真实评测 + 导出 SQL 明细 + 报告
LLM_MODE=real LLM_API_KEY=sk-xxx python eval/run_eval.py \
    --report eval/report.md --save-sql eval/sql_dump.jsonl

# 2. 看报告里的「结果错误明细」逐题 diff，定位高发差异标签
# 3. 按 §4 改 Prompt
# 4. 重跑，看结果正确率是否升到 60%+
```

## 6. 目标与下一步

- 本轮目标：结果正确率 31.6% → 60%+（先把确定性规则灌进 Prompt，再考虑 few-shot 示例）
- 若 60% 后仍有顽固错误（如 Q007 环比这类需要两窗口聚合的），再考虑：
  1. 在指标定义里补"环比/同比需要两个时间窗口分别聚合后再 JOIN"的示例
  2. 加 few-shot：在 prompt 里放 1-2 个 golden_sql 作为格式示范
  3. 扩大评测集到 80 题
