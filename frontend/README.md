# frontend —— 查询结果页（Vue 3 + Vite + Tailwind + ECharts）

第一版只做**查询结果页**：输入问题 → 结论 + 图表 + 明细表 + SQL。
登录、历史会话、Dashboard 不在本版范围内。

## 技术选型

| 项 | 选择 | 说明 |
|---|---|---|
| 构建 | Vite 5 | dev 走 `/api` 代理到 8000 |
| 框架 | Vue 3（`<script setup>`） | 不上 TS / UI 库，保持轻量 |
| 样式 | Tailwind CSS 3 | 设计令牌在 `tailwind.config.js` |
| 图标 | `lucide-vue-next`（Triangle / ChevronDown / ArrowRight） | |
| 图表 | ECharts 5（按需引入） | 后端只给归一化 `chart_data`，前端负责拼 option |
| 请求 | 原生 `fetch` | 只有一个接口 |

## 运行

```bash
# 1) 后端（默认走 .env 的 LLM_MODE，mock 模式不需要 Key）
cd ..
C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe -m uvicorn app.api.app:create_app --factory --host 127.0.0.1 --port 8000

# 2) 前端
cd frontend
npm install
npm run dev        # http://127.0.0.1:5173
```

后端未启动时页面自动降级为**内置真实响应样例**（`src/mock/querySamples.json`，
由 `python eval/dump_query_samples.py` 从真实 SQLite 生成），仍可完整演示 7 种图表形态。

## 设计系统（cream / forest 编辑感）

| 令牌 | 值 | 用途 |
|---|---|---|
| `brand-dark` | `#2d3a2e` | 正文、按钮、图标 |
| `brand-green` | `#3d5a3e` | hover、强调竖条 |
| `brand-light` | `#f5f3ef` | 徽章底 |
| `brand-cream` | `#faf8f5` | 页面底、导航滚动态 |

字体：正文 `Helvetica Neue Light`；展示字体 Playfair / Oswald / Montserrat / Roboto Slab / Raleway
只用于 `Built with` 那一行 wordmark。

动效（`src/styles.css`）：`fade-up`（内容）/ `fade-down`（导航）+ `stagger-1..6` 交错延迟。
导航 0/120/240ms，公告 pill、标题、提问区、wordmark 行依次 240/360/480/600ms。

导航：fixed，`scrollY > 20` 时切换为 `bg-brand-cream/90 + backdrop-blur-md + shadow-sm`；
移动端汉堡两条 2px 横杠，展开为全屏奶油遮罩并锁定 `body.overflow`。

> 参考了一套"安静、编辑感"的落地页视觉语言并做了本地化适配：
> **没有**引入外部营销视频（不属于本项目、也不该出现在数据分析页），
> **没有**照搬任何营销文案——公告 pill 用的是本项目真实评测数字（80 题 64.0% / 安全 25/25），
> wordmark 行是真实技术栈（FastAPI / SQLite / sqlglot / DeepSeek / ECharts）。

## 目录

```
src/
├── main.js
├── App.vue                  # 状态机：idle/loading/success/empty/error
├── api.js                   # /api/query 封装 + 错误码归一化
├── chartOption.js           # chart_data -> ECharts option（纯函数）
├── styles.css               # Tailwind 入口 + 全局 reset + keyframes
└── components/
    ├── Navbar.vue           # fixed 导航 + 移动端全屏遮罩
    ├── Hero.vue             # 公告 pill + 标题 + 提问框 + 示例 chips
    ├── TrustedBy.vue        # Built with wordmark 行
    ├── Conclusion.vue       # nl_explanation + badges + warnings
    ├── KpiCard.vue          # chart_type = kpi 的大数字卡（不画图）
    ├── ChartPanel.vue       # line / bar / pie（含 resize、dispose）
    ├── ResultTable.vue      # 明细表（优先用后端 columns 做中文表头）
    └── SqlPanel.vue         # SQL 折叠
```

## 渲染规则（与后端契约一致）

| chart_type | 渲染 |
|---|---|
| `kpi` | 大数字卡（`series[0].data[0]` + `unit`），**不初始化 ECharts** |
| `line` / `bar` / `pie` | `ChartPanel`，option 由 `chartOption.js` 生成 |
| `table` | 只渲染明细表（后端 `chart_data` 为 `null`） |

- 类目 > 8 自动转**横向条形**（20 个门店标签才不挤）
- `unit === '元'` 且 ≥ 1 万时轴标签显示为「万」，tooltip 仍给完整值 + 单位
- `kpi` / `table` 没有 `dimension` / `dimension_label`，取用时一律给默认值
- 空结果：`rows.length === 0` → 走空态，展示后端返回的「未查询到符合条件的数据。」
- 表头中文名**优先用后端 `columns[].label`**，缺失时退化成原始列名

## 错误处理

| 场景 | 表现 |
|---|---|
| 400 `sql_invalid` | 「安全校验拦截」+ violations（**防御生效，不是缺陷**） |
| 400 `db_error` / 502 `llm_error` / 422 | 对应文案 + detail |
| 网络失败 | 提示后端未启动；若该问题命中内置样例则自动降级渲染样例 |

## 构建

```bash
npm run build      # 产物 frontend/dist（约 612KB JS / 18KB CSS）
```
