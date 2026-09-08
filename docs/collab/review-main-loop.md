# 主链路审查报告（第一阶段）

> 审查人：WorkBuddy（夜灯）
> 审查时间：2026-09-07 17:46
> 审查对象：`app/db/sqlite.py`、`app/catalog/schema.py`、`app/metrics/glossary.py`、
> `app/llm/client.py`、`app/agent/query_service.py`、`app/api/app.py`

## 一、5 个审查重点结论

### 1. check_sql_safety 集成 ✅ 正确

`query_service.py` 三处调用全部正确：
```python
safety = check_sql_safety(raw_sql, table_infos=self.catalog.to_table_infos())  # 正确传 schema
if not safety.is_safe:
    raise SQLValidationError(safety.violations)                                 # 不安全即抛
rows = self.catalog.db.execute(safety.normalized_sql)                          # 用 normalized_sql 而非 raw_sql ✓
```
关键点：**执行的是 `normalized_sql`（已注入 LIMIT），不是 LLM 原始输出**。正确。

### 2. Glossary 口径与评测集一致 ✅（附 1 条提醒）

- 6 指标定义与 `metrics.yaml` 一致，`cases.jsonl` 的 `business_metric` 与之对齐
- 销售额 `paid_amount > 0`、退款 `refund_status='completed'` 等口径一致
- ⚠️ **提醒**：`glossary.match()` 的别名硬编码在 `glossary.py` 的 `aliases` 字典里，覆盖有限（如「营收」「营业额」不在 sales_amount 别名里）。评测题的措辞若偏离别名，`metric_keys` 会漏匹配。建议后续把别名收敛到 `metrics.yaml`（增加 `aliases` 字段）。

### 3. SQLite query_only 阻止写操作 ✅ 正确（纵深防御）

```python
con.execute("PRAGMA query_only = ON")   # 连接级只读
```
- `query_only=ON` 让 INSERT/UPDATE/DELETE/CREATE/DROP/ALTER 全部失败
- 与 `check_sql_safety`（白名单 + 只读限制）形成**双层防护**：即使校验器被绕过，DB 层仍兜底
- 这是 OWASP LLM「Excessive Agency」的正确防御姿势

### 4. cases.jsonl 稳定驱动 Mock ✅

`MockLLMClient` 以 `question → golden_sql` 精确映射，评测脚本只要传入的 question 与 cases.jsonl 完全一致即可稳定驱动。注意：question 必须**逐字一致**（含标点），否则抛 `ValueError`。

### 5. run_eval.py 需要补充 ⚠️

Mock 模式的基础设施（`MockLLMClient`）已就绪，但缺一个「读 cases.jsonl → 对每题跑 query → 统计指标」的评测脚本。**已补 `eval/run_eval.py`**（见下）。

## 二、非阻塞问题（3 个）

### 问题 A：`catalog.relevant()` 召回基本失效（真实 LLM 模式会暴露）

`query_service.py` 第 29 行：
```python
context = self.catalog.prompt_context(self.catalog.relevant([question] + [m.name for m in metrics]))
```
`relevant()` 用「整串子串匹配」打分：`term in haystack`。但传入的 `question` 是**完整句子**，表名/字段名/描述里不可能包含整句，所以所有表 score 都 = 0，召回退化为「按表名字母序返回前 6 张」。

字母序前 6 张 = `after_sales, customers, inventory_snapshots, order_items, orders, payments`。
**`stores`（第 10 位）不在其中** → Q002「长沙门店销售额」在真实 LLM 模式下拿不到 stores 的 schema，无法生成 JOIN。

- Mock 模式不暴露（Mock 忽略 context）
- 真实 LLM 模式下是**实际缺陷**
- 建议：`relevant()` 改为分词（jieba）或 embedding 召回，至少把 question 按空白/关键词切分后再匹配

### 问题 B：接口契约脱节

`api/app.py` 的实际响应与 `docs/collab/interface-contract.md` 不一致：

| 字段 | 契约 | 实现 |
|---|---|---|
| session_id | ✅ 有 | ❌ 缺 |
| intent | ✅ 有 | ❌ 缺（用 metric_keys 替代）|
| chart | ✅ 有 | ❌ 缺（第二版）|
| explanation | ✅ 有 | ❌ 缺（第二版）|
| metric_keys / warnings | ❌ 无 | ✅ 有 |

建议：**第一版是精简版可接受**，但应同步更新 `interface-contract.md`，标注「chart/explanation/intent 为第二版」避免文档与实现脱节。

### 问题 C：`db.health()` 重复调用

`app.py` 的 health 接口里 `db.health()` 被调了两次（status 一次、db 一次），每次执行 `SELECT 1`。建议缓存一次。非 bug，小优化。

## 三、总体评价

主链路骨架**干净、可测、接口清晰**，`check_sql_safety` 集成和 `query_only` 双层防护是亮点。无阻塞性问题，可以继续实现真实 LLM 接口。

**优先级建议**：
1. 【高】实现真实 LLM 前，先修 `relevant()` 召回（问题 A）——否则真实模式跑不通
2. 【中】同步 `interface-contract.md`（问题 B）
3. 【低】`db.health()` 缓存（问题 C）
