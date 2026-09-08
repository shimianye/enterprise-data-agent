# 主链路第二轮复查（加固后）

> 审查人：WorkBuddy（夜灯）
> 审查时间：2026-09-07 17:56
> 复查对象：第一轮审查 3 个非阻塞问题 + 5 处声明的修复

## 一、5 处修复的真实状态

| # | 声明修复 | 实际状态 | 说明 |
|---|---|---|---|
| 1 | Schema 召回分词 | ⚠️ 不彻底 | 正则 `[\w\u4e00-\u9fff]+` 非真正中文分词，见 §2 |
| 2 | 关键表保留 | ❌ 失效 | 用英文表名匹配中文分词，语义错位，见 §3 |
| 3 | Glossary 过滤进上下文 | ❌ 未接入 | `glossary.prompt_context()` 无人调用，见 §4 |
| 4 | 数据库异常 → db_error | ✅ 生效 | `RuntimeError` → api 映射 `db_error` |
| 5 | health 探测一次 + llm | ✅ 生效 | `db_ok` 缓存 + 返回 `llm` 字段 |

## 二、召回分词不彻底（问题 A 未根治）

`schema.py:67`：
```python
terms = [part.lower() for term in terms
         for part in re.findall(r"[\w\u4e00-\u9fff]+", term) if len(part) > 1]
```
正则把**连续中文整体当一个 token**，不做分词。「长沙门店 2026 年 8 月的销售额」会被切成：
- `["长沙门店", "2026", "月的销售额"]`（单字「年」「8」被 `len>1` 过滤）

于是「长沙」「销售额」这些真正有召回价值的词，被「长沙门店」「月的销售额」吞掉，仍然匹配不上 stores/orders 的表描述。**建议改用 jieba 分词**（`jieba.lcut(question)`）。

## 三、关键表保留逻辑失效（问题 A 的另一半）

`schema.py:76-79`：
```python
for required in ("orders", "order_items", "stores", "products"):
    table = self.tables.get(required)
    if table and table not in selected and any(required in term for term in terms):
        selected.append(table)
```
`required` 是**英文表名**（`"stores"`），`terms` 是**中文分词结果**（`["长沙门店", ...]`）。`"stores" in "长沙门店"` 恒为 `False`，所以这层保留逻辑**永远不触发**。

「关键表不轻易被排除」的目标没有实现——`stores` 依然会被字母序排序挤到第 10 位之外。

## 四、Glossary Prompt 未接入（最严重）

`glossary.py:26-27` 的 `prompt_context()` 增加了 filters 输出：
```python
def prompt_context(self, metrics=None):
    return "\n".join(f"- {m.name} ..." + (f"; 默认过滤: {', '.join(m.filters)}" if m.filters else "") ...)
```
但 grep 全 `app/` 目录，**该方法零调用**。`query_service.py:30` 组装的 context 只有：
```python
context = self.catalog.prompt_context(self.catalog.relevant([question] + [m.name for m in metrics]))
```
没有 `self.glossary.prompt_context(metrics)`。

**后果**：真实 LLM 拿到的上下文只有「表结构」，没有「指标口径」——不知道销售额 = `SUM(paid_amount)` 且要 `paid_amount > 0`，不知道退款要 `refund_status='completed'`。这是真实 LLM 模式下**必然导致口径错误**的缺口。

**修复**：query_service 组装 context 时应合并两部分：
```python
context = (
    self.glossary.prompt_context(metrics) + "\n\n" +
    self.catalog.prompt_context(self.catalog.relevant([question] + [m.name for m in metrics]))
)
```

## 五、结论

- ✅ 已根治：db_error 映射、health 探测
- ⚠️ 部分生效：召回（分词方向对了，但非 jieba，效果有限）
- ❌ 未生效：关键表保留、**Glossary 口径进上下文**

**这两处未生效，恰恰是真实 LLM 接入后的两个致命点**：召回错表 → 生成 SQL 缺表；口径不进 context → 生成 SQL 用错字段。Mock 模式的 20/20 全过无法暴露它们（Mock 直接返回 golden_sql，与召回和 context 无关）。

**接入真实 LLM 前，务必先修 §2/§3/§4。**

---

## 六、修复确认（2026-09-07 18:13）

三个问题已全部修复并实测验证：

| 问题 | 修复 | 实测验证 |
|---|---|---|
| §2 召回分词 | 接入 jieba（ImportError 兜底正则）| `jieba.lcut('长沙门店销售额')` = `['长沙','门店','销售额']` ✅ |
| §3 关键表保留 | 英文表名 → 中文别名映射 | `relevant` 召回含 `stores`、`orders` ✅ |
| §4 Glossary 未接入 | query_service 组合 glossary + catalog 两段 context | context 含 `orders.paid_amount > 0` ✅ |

端到端验证（真实 enterprise.db）：
```
jieba 分词: ['长沙', '门店', '销售额']
匹配指标: ['sales_amount']
召回表: ['inventory_snapshots', 'stores', 'after_sales', 'customers', 'order_items', 'orders']
包含 paid_amount > 0: True
```

测试 57 passed，Mock 评测 20/20 全过。三个致命点已消除，可以接入真实 LLM。
