# Review：图表 / NL 解释评测 Round 1（C007–C010 修复方案）

> 评审人：夜灯（WorkBuddy） | 日期：2026-09-08 | 対象：`app/agent/presentation.py`、`app/agent/explanation.py`
> 结论：**4 条失败里有 2 条是真 bug（英文列名泄漏到面向用户的中文文案），不是"细节不一致"**。
> 补丁已在临时脚本中预演，`eval/cases-chart-nl.jsonl` **未放宽任何期望**，预演结果 **10/10**。

---

## 1. 现状

```
[SUMMARY] total=10 passed=6 failed=4
[FAIL] C007: explanation 缺关键词: '金卡'
[FAIL] C008: explanation 缺数字: '3838'
[FAIL] C009: explanation 缺关键词: '门店'
[FAIL] C010: explanation 缺关键词: '城市'
```

10 条的 **intent 与 chart_type 全部正确**（规则 1–7 已生效），失败 100% 集中在 `nl_explanation` 文案层。

## 2. 逐条根因与分级

| ID | 题目 | 当前输出 | 缺什么 | 根因 | 等级 |
|---|---|---|---|---|---|
| C007 | 各等级客户数 | `4 个等级中，普通 最高（5,529个，占 55.3%）。` | 金卡 | comparison 模板只点名 TOP1 | 🟡 模板增强 |
| C008 | 2026 年 8 月订单金额分布 | `over_2000 占比最高（89.8%）；共 4 个区间。` | 3838 | distribution 模板只给百分比，不给绝对值 | 🟡 模板增强 |
| C009 | 最近一次快照各门店缺货 SKU 数 | `SKU最高的是 19（10件）。` | 门店 | 维度列 `store_id` 未映射，裸值 19 出现在中文句里 | 🔴 **真 bug** |
| C010 | 各等级客户城市分布 | `共 32 条记录，涵盖 customer_level、city。` | 城市 | 表格兜底直接拼**原始英文列名** | 🔴 **真 bug** |

### 关于 C007 的一个诚实说明

各等级客户数真实数据：`普通 5529 / 银卡 2472 / 金卡 1496 / 黑卡 503`。
**金卡是第 3 名**，不是第 2 名。所以"点名 TOP2"这条改法**救不了** C007——它会输出"银卡"。
真正站得住的改法是：**comparison 在分类数 ≤5 时全量列举**（饼图本来就是看构成），这样
"普通/银卡/金卡/黑卡"全部出现，任何一条被点名都能命中，且信息量更大、完全确定性。
本轮采用这个改法，**没有为通过评测而修改期望值**。

### C009/C010 为什么算真 bug（不只是文案）

`store_id` / `customer_level` / `city` 是**物理列名**，直接进中文句子，用户看到的是
"最高的是 19""涵盖 customer_level、city"。这不是模板措辞问题，是**展示层缺少列名→中文的映射**。
前端表格若直接拿 `rows` 的 key 当表头，会犯同样的错（见 §6）。

## 3. 补丁 A：`app/agent/presentation.py`

### A1. `LABELS` 补一条（顺带修掉图例/系列名里的 `sku_count`）

```python
LABELS = {
    ...
    "sku_count": "SKU 数",        # 新增：否则 series[0].name 与图例显示 "sku_count"
}
```

### A2. 新增维度名映射 + `column_label()`

```python
DIMENSION_LABELS = {
    "store_id": "门店", "store": "门店", "store_name": "门店",
    "city": "城市", "region": "地区",
    "customer_level": "等级", "level": "等级",
    "brand": "品牌", "category": "品类", "channel": "渠道",
    "sku_id": "SKU", "product_id": "商品", "product_name": "商品",
    "ym": "月份", "month": "月份", "date": "日期", "week": "周", "snapshot_date": "快照日期",
    "bucket": "区间", "amount_range": "金额区间", "segment": "分层", "repurchase_tier": "复购分层",
    "supplier_id": "供应商", "warehouse_id": "仓库", "agent_id": "客服",
}


def column_label(column: str) -> str:
    """物理列名 -> 中文展示名。查不到就原样返回（宁可露列名也不要错译）。"""
    lower = (column or "").lower()
    return DIMENSION_LABELS.get(lower) or LABELS.get(lower) or column
```

### A3. `build_chart_data()` 非 kpi/table 分支补两个字段

```python
    return {
        "categories": [row.get(dimension) for row in rows],
        "series": [...],
        "unit": UNITS.get(metrics[0], "") if len(metrics) == 1 else "",
        "dimension": dimension,                      # 新增：物理列名
        "dimension_label": column_label(dimension),  # 新增：中文维度名（前端可直接当 X 轴名）
    }
```

> `kpi` / `table` 分支保持原样（不输出这两个字段），契约上标注"可选"。

## 4. 补丁 B：`app/agent/explanation.py`（整文件替换）

```python
"""Deterministic natural-language explanations for query results."""
from __future__ import annotations

from numbers import Number
from typing import Any

from app.agent.presentation import column_label

COUNT_UNITS = {"件", "个", "人", "单", "次"}


def _format(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, Number):
        return str(value)
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    return f"{value:,.0f}"


def _topic(question: str) -> str:
    for word in ("销售额", "客单价", "SKU 数量", "SKU", "销量", "客户数", "缺货", "订单金额", "渠道", "等级", "城市"):
        if word in question:
            return word
    return "查询结果"


def _category(value: Any, dim_label: str) -> str:
    """维度值 -> 人类可读标签。store_id=19 -> '门店 19'；中文值（普通/长沙）原样返回。"""
    text = str(value)
    if not dim_label or not text or not text.isascii():
        return text
    return f"{dim_label} {text}"


def explain(question: str, intent: str, chart_data: dict[str, Any] | None, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "未查询到符合条件的数据。"
    if intent == "table" or chart_data is None:
        dimensions = "、".join(column_label(c) for c in list(rows[0])[:-1]) or "相关维度"
        return f"共 {len(rows)} 条记录，涵盖 {dimensions}。"
    categories = chart_data["categories"]
    series = chart_data["series"]
    values = series[0]["data"] if series else []
    unit = chart_data.get("unit", "")
    dim_label = chart_data.get("dimension_label", "")
    metric = series[0]["name"] if series else _topic(question)

    if intent == "metric_query":
        return f"{question}：{metric}为 {_format(values[0])}{unit}。"
    if intent == "ranking" and len(rows) == 1:
        label = next((str(v) for v in rows[0].values() if not isinstance(v, Number)), "TOP1")
        return f"{question}：{label}（{_format(values[0])}{unit}）。"
    if intent == "trend":
        return f"{metric}从 {categories[0]} 的 {_format(values[0])}{unit} 变化到 {categories[-1]} 的 {_format(values[-1])}{unit}。"
    if intent == "comparison":
        order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
        total = sum(v for v in values if isinstance(v, Number))
        shown = order if len(order) <= 5 else order[:3]
        parts = []
        for pos, i in enumerate(shown):
            pct = values[i] / total * 100 if total else 0
            if pos == 0:
                parts.append(f"{categories[i]}最高（{_format(values[i])}{unit}，占 {pct:.1f}%）")
            else:
                parts.append(f"{categories[i]}（{_format(values[i])}{unit}，占 {pct:.1f}%）")
        tail = "。" if len(shown) == len(order) else f"，其余 {len(order) - len(shown)} 个省略。"
        dim = dim_label or ("渠道" if "渠道" in question else "分类")
        return f"{len(categories)} 个{dim}中，" + "、".join(parts) + tail
    if intent == "distribution":
        best = max(range(len(values)), key=lambda i: values[i])
        total = sum(v for v in values if isinstance(v, Number))
        pct = values[best] / total * 100 if total else 0
        return f"{categories[best]} 区间占比最高（{_format(values[best])}{unit}，占 {pct:.1f}%）；共 {len(categories)} 个区间。"
    best = max(range(len(values)), key=lambda i: values[i])
    verb = "最多" if unit in COUNT_UNITS else "最高"
    return f"{metric}{verb}的是 {_category(categories[best], dim_label)}（{_format(values[best])}{unit}）。"
```

**改动点速览**

| 位置 | 改动 | 修哪条 |
|---|---|---|
| 表头 | 引入 `column_label` | — |
| table 分支 | `column_label(c)` 代替原始列名 | **C010** |
| ranking 单行 | 去掉冗余的"最高的是"（问题里已有），只回答案+值 | 可读性 |
| comparison | 分类 ≤5 全量列举（降序，TOP1 标"最高"），>5 只列 TOP3 并注明省略 | **C007** |
| distribution | 同时给**绝对值 + 百分比** | **C008** |
| ranking 多行兜底 | 用 series 名当指标名；按单位选"最多/最高"；`_category()` 补维度名 | **C009** |

> 依赖方向：`explanation` → `presentation`（单向），`presentation` 不 import `explanation`，无循环导入。

## 5. 预演结果（补丁逻辑 + 真实数据，期望值未放宽）

```
PASS C001 [metric_query/kpi] 2026 年 8 月的总销售额：销售额为 34,475,986.52元。
PASS C002 [metric_query/kpi] 2026 年 8 月的客单价：客单价为 8,070.22元。
PASS C003 [metric_query/kpi] 最近一次快照中库存低于安全线的 SKU 数量：数量为 1,458个。
PASS C004 [trend/line]      销售额从 2026-01 的 34,328,506.15元 变化到 2026-06 的 32,342,552.39元。
PASS C005 [ranking/kpi]     2026 年 8 月销量最高的品牌：Cedar（2,123件）。
PASS C006 [comparison/pie]  3 个渠道中，门店最高（23,433,862.88元，占 34.1%）、电商平台（22,733,171.4元，占 33.1%）、小程序（22,480,588.83元，占 32.7%）。
PASS C007 [comparison/pie]  4 个等级中，普通最高（5,529个，占 55.3%）、银卡（2,472个，占 24.7%）、金卡（1,496个，占 15.0%）、黑卡（503个，占 5.0%）。
PASS C008 [distribution/bar] over_2000 区间占比最高（3,838个，占 89.8%）；共 4 个区间。
PASS C009 [ranking/bar]     SKU 数最多的是 门店 19（10件）。
PASS C010 [table/table]     共 32 条记录，涵盖 等级、城市。
[SIM] total=10 passed=10 failed=0
```

> C009 的 `SKU 数` 依赖 A1 的 `LABELS["sku_count"]`；不打 A1 会显示 `sku_count`（仍能过评测，但文案很难看）。
> 预演脚本是一次性的，未写入仓库；应用补丁后请用 §7 的命令做正式验证。

## 6. 给前端（Vue 3 + ECharts）的两个提醒

1. **可直接用 `chart_data.dimension_label` 当 X 轴名 / tooltip 前缀**（"门店"、"城市"、"等级"），
   前端不必再维护一份中文映射。
2. **表格视图的表头同样会露英文列名**——`table` 意图下 `chart_data` 为 `null`，前端只能拿 `rows` 的 key。
   两个选择（推荐前一个）：
   - **后端在 `QueryResult` 增加 `columns: [{"name","label","is_numeric"}]`**（映射复用 `column_label`），
     前端直接渲染中文表头 + 数值列右对齐；
   - 或前端本地维护一份列名字典（**不推荐**：与后端 `DIMENSION_LABELS` 双份维护，必然漂移）。

   契约若要加 `columns`，我建议作为 §5.1 的**追加可选字段**，不破坏现有 4 个字段。

## 7. 验收方式

```bash
python eval/run_chart_nl_eval.py
# 期望：[SUMMARY] total=10 passed=10 failed=0
```

补丁应用后 `eval/report-chart-nl.md` 会同步刷新（报告已改为展示全部 10 条的解释文本，方便下轮 diff）。

## 8. 遗留 nit（本轮**未**改，避免补丁膨胀）

| nit | 例子 | 建议 |
|---|---|---|
| 单位与指标名语义重复 | `数量为 1,458个` | 可在指标名以"数/量"结尾且单位为"个"时省略单位；但会削弱 C008 的 `3,838个`，需权衡 |
| 数字与中文单位之间无空格 | `34,475,986.52元` | 排版细节，可选 |
| `_topic()` 仍是硬编码词表 | "缺货" 等新词要手加 | Phase 3.5 若接 LLM 兜底可一并替换 |
| comparison 阈值 5 | 6 类时只列 TOP3 | 现规则够用，先不动 |
| 评测集偏小 | 10 条 | 前端联调后建议补到 15–20 条，含**空结果**与**多指标 trend** 两类边界 |

## 9. 签收

- [ ] 应用补丁 A（presentation.py）
- [ ] 应用补丁 B（explanation.py）
- [ ] 跑 `python eval/run_chart_nl_eval.py` 确认 10/10
- [ ] 决定是否在 `QueryResult` 加 `columns`（影响前端表头）
- [ ] 进入 Phase 3 第 4 步：Vue 3 + ECharts 查询结果页
