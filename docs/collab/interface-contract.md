# 接口契约 Interface Contract

> 状态：**v1 已对齐 `app/api/app.py` 实际实现**（2026-09-07）
> 双方都不得单方面改动字段名；改动需在此文件更新并同步对方。
> 带 `（Phase 2）` 标记的字段为规划中、**尚未实现**，前端/评测不要依赖。

## 1. 查询接口

### `POST /api/query`

**请求体**
```json
{
  "question": "上个月长沙地区 iPhone 销售额"
}
```

> `session_id` 为 Phase 2 预留，v1 不接受，传了会被忽略（pydantic 模型只定义了 `question`）。

**成功响应（200）— v1 实际结构**
```json
{
  "question": "上个月长沙地区 iPhone 销售额",
  "sql": "SELECT SUM(orders.paid_amount) ...",
  "rows": [ { "month": "2026-08", "sales": 1234567.89 } ],
  "duration_ms": 1420,
  "metric_keys": ["sales_amount"],
  "warnings": []
}
```

**字段说明**

| 字段 | 类型 | 说明 |
|---|---|---|
| question | string | 原样回传 |
| sql | string | 经安全校验后**规范化过的**实际执行 SQL（审计用，前端可折叠展示）|
| rows | list[dict] | 查询结果（SQLite 返回的 dict 行）|
| duration_ms | int | 端到端耗时（指标匹配 → 上下文 → 生成 → 校验 → 执行）|
| metric_keys | list[string] | 命中的指标 key，如 `["sales_amount"]` |
| warnings | list[string] | 安全校验的告警（非致命），如 `["LIMIT 已自动补为 1000"]` |

**Phase 2 预留字段（v1 暂无，勿依赖）**

| 字段 | 类型 | 说明 |
|---|---|---|
| session_id | string | 多轮上下文用 |
| intent | string | `metric_query` / `trend` / `comparison` / `ranking` / `chitchat` / `out_of_scope` |
| chart | object | `{ "type": "kpi"\|"line"\|"bar"\|"pie"\|"table", "option": {...ECharts option} }` |
| explanation | string | 自然语言结论 |

> ⚠️ 上表是 Phase 2 的**旧草案**。Phase 3 实际落地方案改为**拆成 3 个扁平字段**（见 §5），
> 不再用嵌套 `chart.option`——理由是后端只负责"选图 + 归一化数据"，ECharts option 由前端拼装，
> 前后端职责更清晰、也更好测。以 §5 为准。

**错误响应（4xx）**

```json
{
  "detail": {
    "error": "sql_invalid",
    "violations": ["禁止访问表 users"]
  }
}
```

> 注意：v1 错误体包在 FastAPI 的 `detail` 字段里（`HTTPException(400, detail={...})`）。

**错误码枚举**

| error | HTTP 状态 | 触发条件 | detail 附加字段 |
|---|---|---|---|
| `sql_invalid` | 400 | SQL 未通过安全校验 | `violations` |
| `db_error` | 400 | 数据库查询失败（SQLite 异常） | `message` |
| `llm_error` | 502 | 真实 LLM 调用失败（网络/鉴权/限流/上游 5xx） | `message` |
| —（未命名） | 422 | Mock 无对应 golden SQL / 文件缺失 | `detail` 为字符串 |

> 注：`llm_error` 已实现（`app/api/app.py` 捕获 `httpx.HTTPError` → 502）。

## 2. 健康检查

### `GET /api/health`

```json
{
  "status": "ok",
  "db": "ok",
  "llm": "ok"
}
```

v1 实际逻辑：
- `status`: `ok` / `degraded`（db 健康 && llm 健康）
- `db`: `ok` / `error`（由 `SQLiteDatabase.health()` 决定）
- `llm`: `ok` / `error`
  - `LLM_MODE=mock`（默认）→ 恒 `ok`
  - `LLM_MODE=real` → 有 `LLM_API_KEY` 则 `ok`，否则 `error`
  - **注意**：这里只检查「配置是否存在」，不做真实连通性/鉴权探测；API 实际不可达或 key 失效时仍会显示 `ok`，直到 `/api/query` 才报 `llm_error`

## 3. 评测接口（预留）

### `POST /api/eval/run`

> 第二版再实现，第一版评测在 `eval/run_eval.py` 离线跑。

```json
{
  "case_ids": ["Q001", "Q002"],
  "return_detail": true
}
```

## 4. 数据层约定

- **数据库：SQLite（`data/enterprise.db`），只读连接**（`PRAGMA query_only = ON` + 安全校验，双层防御）
- MySQL 8.0 为未来生产化可选迁移方向，当前不做
- SQL 校验规则见 `docs/sql_safety.md`

---

## 5. Phase 3 新增字段（图表 + NL 解释）

> 状态：**草案待实现**（2026-09-08）。前端按本节字段开发，后端实现后双方联调。

### 5.1 响应新增 3 个字段

`/api/query` 成功响应在 v1 基础上**追加** 3 个字段（v1 字段全部保留，向后兼容）：

```json
{
  "question": "2026 年 8 月销量最高的品牌",
  "sql": "SELECT oi.brand, SUM(oi.quantity) AS total_qty FROM ...",
  "rows": [ { "brand": "Orbit", "total_qty": 25741 }, { "brand": "Cedar", "total_qty": 24276 } ],
  "duration_ms": 1420,
  "metric_keys": ["order_count"],
  "warnings": [],

  "intent": "ranking",
  "chart_type": "bar",
  "chart_data": {
    "categories": ["Orbit", "Cedar", "Nova", "Aster", "Pulse"],
    "series": [ { "name": "销量", "data": [25741, 24276, 23634, 23625, 23285] } ],
    "unit": "件"
  },
  "nl_explanation": "2026 年 8 月销量最高的品牌是 Orbit（25,741 件），TOP5 合计 120,561 件。",
  "columns": [
    { "name": "brand", "label": "品牌", "is_numeric": false },
    { "name": "total_qty", "label": "销量", "is_numeric": true }
  ]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| intent | string enum | 问题意图（见 5.2），决定 NL 解释模板 |
| chart_type | string enum | `kpi` / `line` / `bar` / `pie` / `table`（见 5.3）|
| chart_data | object | **归一化**图表数据（见 5.4），前端据此拼 ECharts option |
| nl_explanation | string | 自然语言结论（见 5.5）|
| columns | array | **2026-09-08 新增**：`{name,label,is_numeric}`，中文表头来源（见 5.8）|

> **为什么不用 `chart.option`（嵌套 ECharts option）**：后端只负责"选图型 + 归一化数据"，
> ECharts 的样式/配色/交互属前端职责。这样后端可离线单测，前端可自由换图表库。

### 5.2 intent 枚举

| intent | 含义 | 例 |
|---|---|---|
| `metric_query` | 单值指标（总额/比率/均值/计数）| "8 月总销售额" |
| `trend` | 时间序列 | "上半年各月销售额" |
| `ranking` | 排行 TOP N | "销量最高的品牌" |
| `comparison` | 少量分类对比/占比 | "各渠道销售额"（3 个渠道）|
| `distribution` | 分桶分布 | "订单金额分布" |
| `table` | 兜底明细（多维/多行）| "各等级客户城市分布" |
| `out_of_scope` | 非数据问题/越界 | "今天天气怎么样" |

### 5.3 chart_type 选型规则（**确定性**，按序匹配）

后端按以下顺序匹配，**先命中先返回**（保证可离线单测、无 LLM 随机性）：

| 序 | 条件 | intent | chart_type |
|---|---|---|---|
| 1 | `rows` 为 1 行 × 1 列 | `metric_query` | **`kpi`** |
| 2 | 含时间列（`ym`/`month`/`week`/`yweek`/`date`/`snapshot_date`）且 >1 行 | `trend` | **`line`** |
| 3 | 含分桶列（`bucket`/`amount_range`/`segment`/`repurchase_tier`/`*_range`）| `distribution` | **`bar`** |
| 4 | 1 维 + 1 指标，行数 2–6 | `comparison` | **`pie`** |
| 5 | 1 维 + 1 指标，行数 > 6 | `ranking` | **`bar`** |
| 6 | ≥3 列 或 行数 > 30 | `table` | **`table`** |
| 兜底 | 其余 | `table` | **`table`** |

> 规则 3 必须排在规则 4 之前：Q043「订单金额分布」只有 4 个桶，若按"2–6 行 → pie"会错判成饼图，
> 但分布题用柱状图（看区间形态）比饼图（看占比）更合适。

### 5.4 chart_data 结构

```json
{
  "categories": ["Orbit", "Cedar"],        // X 轴标签；kpi / table 时为 []
  "series": [ { "name": "销量", "data": [25741, 24276] } ],  // 通常 1 条；多维时多条
  "unit": "件",                             // 单位（元/件/单/小时/%），无则 ""
  "dimension": "brand",                    // 维度物理列名（kpi / table 时省略）
  "dimension_label": "品牌"                 // 维度中文名（kpi / table 时省略）
}
```

- `categories` 与 `series[i].data` **长度必须一致**
- `kpi` 时：`categories` 为 `[]`，`series` 为 1 条、`data` 为长度 1 的数组
- `table` 时：`chart_data` 可为 `null`（前端直接渲染 `rows`）
- `dimension` / `dimension_label` 为 **2026-09-08 追加的可选字段**（见 `docs/collab/review-chart-nl-round1.md`）：
  - `dimension_label` 由后端 `presentation.column_label()` 生成，前端可直接当 X 轴名 / tooltip 前缀，
    **不要在前端再维护一份中文字典**（否则必然与后端漂移）
  - `table` 意图下表头也会露英文列名，建议后端追加 `columns: [{name,label,is_numeric}]`（待定）

### 5.5 nl_explanation 模板（v1 用**确定性模板**，不额外调 LLM）

| intent | 模板 |
|---|---|
| `metric_query` | `{问题}：{指标名}为 {值}{单位}` |
| `trend` | `{指标名}从 {首期} 的 {值1}{单位} 变化到 {末期} 的 {值2}{单位}` |
| `ranking`（单行 TOP1）| `{问题}：{答案}（{值}{单位}）` |
| `ranking`（多行）| `{指标名}{最高/最多}的是 {维度名} {维度值}（{值}{单位}）` |
| `comparison` | 分类 ≤5：`{N} 个{维度}中，{TOP1}最高（{值}{单位}，占 {pct}%）、{其余各类}（…）`；>5 只列 TOP3 并注明省略 |
| `distribution` | `{最大桶} 区间占比最高（{值}{单位}，占 {pct}%）；共 {N} 个区间` |
| `table` | `共 {行数} 条记录，涵盖 {中文维度列表}` |
| `out_of_scope` | `抱歉，该问题不在经营数据分析范围内。` |

> **解释里不允许出现物理列名**（`store_id` / `customer_level` / `city` 等），
> 一律经 `presentation.column_label()` 转中文。维度值若是英文/数字，补维度名前缀（`门店 19`）；
> 中文值（普通、长沙）直接用。详见 `docs/collab/review-chart-nl-round1.md`。

> **v1 用模板而非 LLM 生成**：可离线单测、无随机性、零额外 token 成本。
> 若后续想要更自然的措辞，再加 LLM 兜底（标为 Phase 3.5，需单独评测）。

### 5.6 前端职责（后端不做）

1. 按 `chart_type` 选组件：`kpi`→大数字卡 / `line`→折线 / `bar`→柱状 / `pie`→饼图 / `table`→表格
2. 由 `chart_data` 拼 ECharts `option`（配色、图例、tooltip、响应式属前端）
3. 渲染 `nl_explanation` 为结论区，`rows` 为明细表（可折叠）
4. `sql` 折叠展示（审计/调试用）

### 5.7 columns（中文表头，2026-09-08 新增）

`table` 意图下 `chart_data` 为 `null`，前端只能拿 `rows` 的 key 当表头（会露出 `customer_level`）。
因此后端在 `QueryResult` 追加 `columns`：

```json
"columns": [
  { "name": "customer_level", "label": "等级", "is_numeric": false },
  { "name": "city",           "label": "城市", "is_numeric": false },
  { "name": "cnt",            "label": "数量", "is_numeric": true }
]
```

- `label` 由 `presentation.column_label()` 生成（与解释层同一份 `DIMENSION_LABELS`，**前端不要再维护字典**）
- `is_numeric` 由前 20 行采样判定，前端据此**数值列右对齐 + 千分位**
- `rows` 为空时 `columns` 为 `[]`

### 5.8 评测

- 评测集：`eval/cases-chart-nl.jsonl`（10 条，覆盖全部 7 种 intent）
- 校验项：`intent` 精确匹配、`chart_type` 精确匹配、`chart_data` 结构（categories/series 长度一致）、
  `nl_explanation` 必须包含指定实体名与关键词
- 说明见 `eval/README.md` §"图表/NL 解释评测集"
