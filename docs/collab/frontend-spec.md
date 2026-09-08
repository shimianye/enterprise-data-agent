# Phase 3 Step 4：Vue 3 + ECharts 查询结果页 —— 实现规格

> 状态：**已实现**（2026-09-08），代码在仓库 `frontend/`，随 Vite dev server 跑在 5173，已与 8000 后端联调通过。
> 编写：夜灯（WorkBuddy）| 2026-09-08 | 対象：第 4 步前端实现
> 前置：图表/NL 评测 10/10（`eval/report-chart-nl.md`），契约见 `docs/collab/interface-contract.md` §5
> 配套产物：
> - 可点开的页面原型 `D:\Administrator\WorkBuddy\outputs\enterprise-data-agent\query-page-prototype.html`（离线可用，真实数据）
> - 真实响应样例 `eval/fixtures/query-samples.json`（10 条，覆盖 7 种 `intent/chart_type` 组合）

---

## 0. 范围（与用户既定一致）

**只做查询结果页**：输入问题 → 展示结论 + 图表 + 明细表 + SQL。
**不做**：登录、历史会话、Dashboard、多轮上下文、权限。

## 1. 技术栈建议

| 项 | 建议 | 理由 |
|---|---|---|
| 构建 | Vite 5 + Vue 3（`<script setup>`） | 启动快；简历项目里够专业 |
| 语言 | JavaScript（不上 TS） | 页面只有 5 个组件，TS 收益不抵配置成本；若想加分可上 TS |
| 图表 | ECharts 5（按需引入或全量均可） | 后端只给归一化数据，前端自由拼 option |
| UI 库 | **不引入**（原生 CSS + CSS 变量） | 组件少；Element Plus 会吃掉"自己写页面"的展示价值 |
| 请求 | 原生 `fetch`（不引 axios） | 只有一个接口 |
| Mock | `eval/fixtures/query-samples.json` 直接 import | 无 LLM Key 也能开发 |

目录建议（放在仓库 `frontend/`）：

```
frontend/
├── index.html
├── vite.config.js            # proxy: /api -> http://127.0.0.1:8000
└── src/
    ├── main.js
    ├── App.vue               # 页面骨架 + 状态机
    ├── api.js                # postQuery()，错误归一化
    ├── components/
    │   ├── QuestionBar.vue   # 输入框 + 示例问题 chips
    │   ├── Conclusion.vue    # nl_explanation 结论区 + badges
    │   ├── ChartPanel.vue    # chart_data -> ECharts option（核心）
    │   ├── KpiCard.vue       # chart_type = kpi 的大数字卡
    │   ├── ResultTable.vue   # rows 明细表（中文表头）
    │   └── SqlPanel.vue      # SQL 折叠
    └── mock/query-samples.json   # 从 eval/fixtures/ 拷贝
```

## 2. 后端对接（**有一个阻塞项**）

### 2.1 接口

```
POST /api/query
body:  { "question": "2026 年 8 月各渠道销售额对比" }
200:   QueryResult（见下）
```

| 字段 | 类型 | 前端用法 |
|---|---|---|
| `question` | string | 回显在结论下方（小字） |
| `sql` | string | 折叠展示 |
| `rows` | array<object> | 明细表 |
| `duration_ms` | int | badge |
| `metric_keys` | string[] | badge（命中指标词表，可为空） |
| `warnings` | string[] | 有值时用黄色提示条展示（如 LIMIT 被截断） |
| `intent` | enum | badge + 决定文案 |
| `chart_type` | enum | 决定渲染哪个组件 |
| `chart_data` | object \| null | ECharts 数据源；`table` 时为 `null` |
| `nl_explanation` | string | 结论区 |

`chart_data`：

```json
{
  "categories": ["门店", "电商平台", "小程序"],
  "series": [{"name": "销售额", "data": [23433862.88, 22733171.4, 22480588.83]}],
  "unit": "元",
  "dimension": "channel",          // ⚠️ kpi / table 时没有这两个字段
  "dimension_label": "渠道"
}
```

**前端必须容错**：`kpi` 与 `table` 下 `dimension` / `dimension_label` 为 `undefined`，取用时给默认值。

### 2.2 🔴 阻塞项：后端未配置 CORS

`app/api/app.py` 目前只有 `/api/health` 与 `/api/query` 两个路由，**没有 `CORSMiddleware`**。
Vite 跑在 5173、FastAPI 跑在 8000，浏览器会直接拦掉跨域请求，前端永远拿不到数据。

二选一（**推荐 A**，联调时不用管前端端口）：

**A. 后端加 CORS**（`app/api/app.py`）：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 本地开发足够；生产要限定来源
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**B. 前端走 Vite 代理**（`vite.config.js`）：

```js
server: { proxy: { '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true } } }
```

> 两个方案可同时做。原型页面里的"调用 /api/query"按钮已经把这两种失败都提示出来了。

### 2.3 错误码映射

| HTTP | `detail.error` | 前端文案 |
|---|---|---|
| 400 | `sql_invalid` | 「该问题无法生成安全查询」+ 展开 `detail.violations`（**这是防御生效，不是 bug**） |
| 400 | `db_error` | 「查询执行失败」+ `detail.message` |
| 502 | `llm_error` | 「模型服务不可用，请稍后重试」 |
| 422 | 字符串 | 「请求不合法」 |
| 网络失败 | — | 「无法连接后端，请检查服务是否启动 / CORS 是否配置」 |

### 2.4 无 Key 开发

后端 `LLM_MODE` 默认为 `mock`（`MockLLMClient` 用 `eval/cases.jsonl` 做问题→SQL 匹配），
**前端不需要 LLM Key 就能联调**；只有 `LLM_MODE=real` 才需要 `LLM_API_KEY`。
mock 模式下问题必须在 `eval/cases.jsonl` 里命中，否则会走真实生成逻辑报错——联调时优先用样例里的原句。

## 3. 页面结构（照原型实现）

```
┌ 标题栏  企业经营数据分析 Agent            [模式徽标]
├ 搜索区  [ 输入框                    ] [提问] [随机样例]
│         chips: 10 个示例问题
│         （可选）后端地址 + [调用 /api/query]
├ 结论区  ▌ 3 个渠道中，门店（…元，占 34.1%）、电商…
│         小字：原问题
│         badges: 意图 / 图表 / 行数 / 耗时 / 指标
├ 可视化  kpi → 大数字卡
│         line / bar / pie → ECharts（标题 = 指标名（单位），轴名 = dimension_label）
│         table → 直接渲染明细表（不画图）
├ 折叠    明细数据（中文表头，数值右对齐，最多 100 行）
└ 折叠    生成 SQL（等宽字体、深色底）
```

## 4. `chart_data` → ECharts option 映射（核心）

| chart_type | 组件 | option 要点 |
|---|---|---|
| `kpi` | `KpiCard.vue` | **不初始化 ECharts**。取 `series[0].data[0]` + `unit` 显示大数字，`series[0].name` 当标签 |
| `line` | ChartPanel | `xAxis= categories`（`name: dimension_label`），`series[0].type='line'`，`smooth:true`，`areaStyle.opacity=0.12` |
| `bar` | ChartPanel | `type='bar'`，`barMaxWidth:28`，圆角 `[4,4,0,0]`；**类目 > 8 时转横向条形**（`xAxis/yAxis` 互换 + `yAxis.inverse=true`），否则 20 个门店标签会挤成一团 |
| `pie` | ChartPanel | 环形 `radius:['42%','68%']`，`tooltip.formatter` 显示 `{b}：{值}{unit}（{d}%）` |
| `table` | ResultTable | 不渲染图表 |

通用细节：

- **轴标签单位换算**：`unit === '元'` 且绝对值 ≥ 10000 时，轴标签显示 `(v/10000).toFixed(0) + '万'`，tooltip 仍显示完整值 + 单位
- **tooltip**：`valueFormatter: v => fmt(v) + unit`，千分位用 `toLocaleString('zh-CN')`
- **配色**：`['#2f6fed','#36cbcb','#f6a623','#f2637b','#7a5af8','#17b26a','#ff8f3f']`
- **销毁**：切结果前 `chart.dispose()`，避免 resize 监听泄漏；`window.resize` 调 `chart.resize()`
- **多系列**：`series.length > 1` 时才显示 legend

## 5. 状态机

| 状态 | 触发 | 展示 |
|---|---|---|
| idle | 首次进入 | 明显示例 chips，引导点击 |
| loading | 请求中 | 图表区骨架屏（LLM 生成 + SQL 执行通常 1–3 s，要有 loading） |
| success | 200 且有 rows | 结论 + 图表 + 明细 |
| **empty** | 200 且 `rows.length === 0` | **注意：此时 `intent='table'`、`chart_data=null`、`nl_explanation='未查询到符合条件的数据。'`** —— 按空态渲染，不要尝试画图 |
| error | 4xx/5xx/网络 | 按 §2.3 文案 |

`warnings` 非空时（如结果被 LIMIT 截断）在结论区下方加一条黄色提示。

## 6. 中文表头（待定的契约项）

`chart_type='table'` 时 `chart_data` 为 `null`，前端只能拿 `rows` 的 key 当表头，会显示 `customer_level` / `city`。
两种解法：

- **推荐**：后端 `QueryResult` 追加 `columns: [{name, label, is_numeric}]`（复用 `presentation.column_label()`），前端直接渲染中文表头 + 数值列右对齐
- 临时：前端自带一份列名字典（**不推荐**，与后端 `DIMENSION_LABELS` 双份维护必然漂移）

原型 `query-page-prototype.html` 用的是临时方案，代码里已标注。若采纳推荐方案，我同步更新契约 §5.1。

## 7. 验收清单（联调后逐条打勾，顺带产出截图）

- [ ] `npm run dev` 能起，无 console 报错
- [ ] 10 条样例问题逐一点一遍，7 种 `intent/chart_type` 全部渲染正确
- [ ] KPI 卡：显示指标名 + 大数字 + 单位（不是空白图表）
- [ ] 折线 6 个月标签完整；柱状 20 个门店转横向且标签不重叠
- [ ] 饼图 tooltip 带单位与百分比
- [ ] 表格 32 行中文表头、数值右对齐、千分位
- [ ] 元单位轴标签显示"万"
- [ ] SQL 折叠可展开、可复制
- [ ] 空结果：输入"2026 年 8 月销售额超过 1 亿的门店"之类无结果问题 → 空态文案，不报错
- [ ] 安全拦截：输入"删除所有订单" → 400 `sql_invalid`，前端给出安全提示（**这是加分项，截图留着**）
- [ ] 后端未启动时 → 网络错误提示而不是白屏
- [ ] 窗口缩放图表自适应

## 8. 下一步（Step 5 联调）

1. 后端加 CORS（§2.2）
2. `LLM_MODE=mock uvicorn app.api.app:app --reload --port 8000`
3. 前端 `npm run dev`，用样例原句逐条验证
4. 按 §7 截图，挑 3–4 张（KPI / 折线 / 饼图 / 表格 + 安全拦截）放进 README
