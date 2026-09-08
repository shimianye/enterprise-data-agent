# 技术尽调报告：text-to-sql-agent-system

> 审查人：WorkBuddy（夜灯）
> 审查时间：2026-09-07 12:17
> 对象：`fengyede79/text-to-sql-agent-system` @ `31b87b31`（MIT License）
> 位置：`vendor/text-to-sql-agent-system`（本地浅克隆，400 文件）

## 一、项目概况（实测数据）

| 指标 | 数值 |
|---|---|
| Python 文件 | 117 个 |
| 代码行数 | 11,004 行（仅 `app/`）|
| 测试函数 | 464 个（非 299，且部分被 pytest ignore）|
| 声明 Python | `>=3.14` |
| License | MIT |
| 数据库 | MySQL（`aiomysql`）|
| 检索 | Elasticsearch 8 + Qdrant |
| 编排 | LangGraph 1.x + LangChain 1.x |

目录分层：
```
app/agent(+nodes)  app/api(+routers,schemas)  app/clients  app/conf
app/core  app/entities  app/eval(+scenarios)  app/events  app/models
app/observability  app/prompt  app/repositories(es,mysql,qdrant)
app/runtime  app/scripts  app/security  app/semantic_plan  app/services
```

## 二、关键发现

### ✅ 发现 1：Python 3.14 不是硬障碍（推翻原判断）

项目声明 `requires-python = ">=3.14"`，但实际依赖**均可降级安装**。实测（managed Python 3.13.12，`--dry-run`）：

| 依赖 | 要求 | 实测结果 |
|---|---|---|
| `sqlglot>=30.12.0` | — | ✅ 装 30.18.0（`py3-none-any` 纯 Python）|
| `langgraph>=1.1.6` | — | ✅ 装 1.2.11 |
| `langchain>=1.2.15` | — | ✅ 装 1.4.0 |

**结论**：3.14 是作者的开发环境声明，非依赖强制。降到 3.13 可行，无需为此放弃该参考项目。

### ⚠️ 发现 2：零 SQLite 支持

全仓库 grep `sqlite`（`app/` + `conf/`）**返回空**。数据层完全建立在 `aiomysql` + ES + Qdrant 之上。
→ "第一版用 SQLite" 意味着**重写整个 `app/repositories/` 层**，不是改配置。

### ⚠️ 发现 3：ES/Qdrant 耦合较深

- `app/repositories/` 下有 `es/`、`mysql/dw/`、`mysql/meta/`、`qdrant/` 四组实现
- **16 个 Python 文件**直接 import `qdrant` 或 `elasticsearch`
- 多路召回（Schema/指标/字段/枚举值）依赖 Qdrant 向量检索 + ES 值检索
→ 砍掉 ES/Qdrant 后，召回层需要自建替代方案（如 Chroma / 内存向量 / BM25）

### ✅ 发现 4：安全校验模块质量高于预期

真实位置是 `app/agent/sql_safety_types.py`（**不在 `app/security/`**，该目录仅 156 行且与 SQL 安全无关）。
324 行，实现质量高，覆盖：

| 能力 | 实现 |
|---|---|
| 注释注入检测 | `_has_comment_markers_outside_literals` —— 手写词法分析，正确跳过单/双引号、反引号字符串内的 `--` `/*` `#` |
| 多语句拦截 | `len(statements) != 1` → `multiple_statements` |
| 只读拦截 | 仅允许 `exp.Select` / `exp.With`（CTE 也算安全）|
| 表白名单 | `_validate_tables` |
| 列白名单 + 歧义检测 | `_validate_columns`，同名字段多表存在时要求限定（`ambiguous_column`）|
| CTE/子查询作用域 | `_virtual_table_names` + `_inner_scope_column_ids` 区分虚拟表名与物理表 |
| 投影别名 | `_projection_aliases` —— `ORDER BY total_sales` 引用 SELECT 别名不算错 |
| SELECT * 拦截 | `_check_stars` |
| LIMIT 注入/钳制 | `_ensure_limit` —— 无 LIMIT 注入默认值，超限钳制 |

**这是全项目最值得参考的部分**，也是用户描述的"sqlglot AST 安全校验"的真实载体。
注意：`read="mysql"` / `sql(dialect="mysql")` 方言写死，适配 SQLite 需改。

### ⚠️ 发现 5：测试可迁移性有限

- 464 个 test 函数，分布在 `tests/{agent,api,security,eval,semantic_plan,...}`
- `pyproject.toml` 中 pytest **默认 ignore** `tests/{connectivity,integration,llm,repository}`
- 真正可离线迁移的主要是 `tests/security/`（纯函数测试，不依赖 DB/LLM）
- 其余测试绑定原项目的数仓 Schema 与 ES/Qdrant，迁移后**基本失效**

## 三、可迁移性评估（按模块）

| 模块 | 行数 | 可迁移性 | 建议 |
|---|---|---|---|
| `sql_safety_types.py` | 324 | **高**（纯函数，仅方言需改）| ⭐ 重点参考，改写为 SQLite 版 |
| `app/eval/` + `scenarios/` | — | **中**（结构可借鉴，用例需重写）| 借鉴"场景化评测"结构 |
| `app/semantic_plan/` | — | 中 | 借鉴"语义计划"分层思路 |
| `app/agent/nodes/` | — | 中 | 借鉴节点划分（预检/召回/生成/校验/执行/恢复）|
| `app/api/` | — | 低（绑定原 Schema 定义）| 自己写 |
| `app/repositories/` | — | **极低**（ES+Qdrant+MySQL 已耦合）| 完全重写 |
| `training/`（torch 等）| — | 无 | 不需要（我们不训模型）|
| `frontend/`（React/Vite）| — | 低 | 自己写（ECharts 工作台）|

## 四、风险提示

### 风险 1：简历可信度（最重要）

用户此前明确反对"开源复现项目"：
> 「三个开源复现项目的可信度不如一个你自己真正做完整的 Text2SQL Agent。」

复制 11,004 行代码后，面试被追问实现细节时若答不上来，风险高于收益。

### 风险 2：掌控度 vs 工作量

改造所需工作（重写 `repositories/`、砍 ES/Qdrant 并自建召回、改 SQLite 方言、重写 Schema Catalog 与评测集）**不低于自行实现核心链路**。

### 风险 3：License 合规

MIT 允许修改与二次开发，但**若直接复制代码文件，须保留原版权声明与 License 文件**。
若为"借鉴设计思路后自行实现"，无法律义务，但工程伦理上建议在项目 README 注明。

## 五、结论与建议

### 推荐：借鉴设计 + 自行实现（不整仓复制）

| 做法 | 内容 |
|---|---|
| ⭐ 参考改写 | `sql_safety_types.py` 的 6 个设计点，改写为 `app/security/validator.py`（SQLite 方言）|
| 借鉴结构 | 评测场景化组织、语义计划分层、Agent 节点划分 |
| 自行实现 | 数据连接层、Schema Catalog、指标 Glossary、Prompt、图表选择、API、前端 |
| vendor 保留 | 作为只读参考，`.gitignore` 排除或明确标注 |

### 可讲的面试叙事

> 「安全校验部分我参考了开源项目 text-to-sql-agent-system 的设计（MIT），针对 SQLite 做了方言适配，并补充了 XX 改进。」

这比「我把一个开源项目改了改」可信度高得多，且体现调研能力。

### 待用户决策

- **A**：借鉴设计、自行实现（推荐）
- **B**：整仓复制后改造（用户原建议，工作量与掌控度风险更高）
