# Review：图表 / NL 解释 Round 2（10/10 之后的文案层回退）

> 评审人：夜灯（WorkBuddy）| 2026-09-08 | 対象：`app/agent/explanation.py`（+ 少量 `presentation.py`）
> 性质：**全部是文案层 nit，不阻塞 Step 4 前端**。但 C005 会出现在 KPI 卡片上（演示最显眼的位置），建议顺手修掉。
> 10/10 已复核通过：`[SUMMARY] total=10 passed=10 failed=0`。

## 1. C005 双空格（🔴 用户可见）

```
销量最多的是  Cedar（2,123件）。
              ^^ 两个空格
```

成因（`explanation.py:32`）：`prefix` 为 `""` 时仍拼了空格。

```python
return f"{metric}{verb}的是 {prefix} {categories[best]}（{_format(values[best])}{unit}）。"
```

修法（最小改动）：

```python
name = f"{prefix} {categories[best]}" if prefix else str(categories[best])
return f"{metric}{verb}的是 {name}（{_format(values[best])}{unit}）。"
```

> `kpi` 场景下 `chart_data` 没有 `dimension_label`（见 `build_chart_data` 的 kpi 分支），
> 所以 prefix 必为空——这不是偶发，是**每次单行 TOP1 都会出现**。

## 2. C005 "销量最多" 选词 + 丢问题上下文（🟡）

- 判定规则 `verb = "最多" if any(x in metric for x in ("数","量")) else "最高"` 会命中**"销量"的"量"**，
  于是求和型指标也变成"最多"（求和型用"最高"，计数型才用"最多"）。
  建议改为按**单位**判定：单位 ∈ {件, 个, 人, 单, 次} → "最多"，否则 "最高"。
  （`件` 会同时命中销量/缺货数，语义上都通；至少不会把"销售额"说成"最多"。）
- 上一版单行 TOP1 是 `2026 年 8 月销量最高的品牌：Cedar（2,123件）。`，带上了**时间限定**；
  现在是 `销量最多的是 Cedar（2,123件）。`，`2026 年 8 月` 丢了。
  前端结论区虽会回显原问题，但 KPI 卡单独看时上下文不完整。
  建议 `intent == "ranking" and len(rows) == 1` 单独走一条：`f"{question}：{答案}（{值}{单位}）。"`

## 3. C010 表格维度把度量列也算进去了（🟡）

```
共 32 条记录，涵盖 等级、城市、数量。
                              ^^^^ "数量" 是 cnt（度量），不是维度
```

`explanation.py:21` 现在遍历了 `rows[0]` 的**全部**列；上一版是 `list(rows[0])[:-1]`（排除末列）。
建议改回"排除数值列"：

```python
dims = [c for c in rows[0] if not any(isinstance(r.get(c), Number) and not isinstance(r.get(c), bool) for r in rows[:20])]
return f"共 {len(rows)} 条记录，涵盖 {'、'.join(column_label(c) for c in dims) or '相关维度'}。"
```

## 4. C006 / C007 全量列举没标 TOP1（🟡）

```
3 个渠道中，门店（23,433,862.88元，占 34.1%）、电商平台（…）、小程序（…）。
```

四类平铺，读者要自己比大小。建议给最大值加"最高"标记：

```python
best = max(range(len(values)), key=lambda i: values[i])
parts = [f"{categories[i]}{'最高' if i == best else ''}（{_format(values[i])}{unit}，占 {values[i]/total*100:.1f}%）" for i in range(len(categories))]
```

## 5. C003 单位冗余（⚪ 已知，可不动）

`SKU 数量为 1,458个` —— "数量"+"个" 语义重复。要么单位表把 `cnt` 的"个"去掉，
要么在指标名以"数/量"结尾且单位为"个"时省略单位。会削弱 C008 的 `3,838个`，需权衡，建议暂不动。

## 6. 一句话提醒

现在的 10/10 表示"**解释命中了评测设定的关键词与数字**"，不等于文案已经打磨好。
README / 简历里如果要写"NL 解释通过率 100%"，建议表述为"图表选型与解释关键要素覆盖率 10/10（自评集）"，
避免过度承诺。
