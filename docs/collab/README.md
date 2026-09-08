# 协作说明（Codex ↔ WorkBuddy）

> 本目录是 **Codex** 与 **WorkBuddy（夜灯）** 之间的所有协作交流载体。
> 所有接口契约、任务清单、审查笔记、交接说明，一律写成本目录下的 Markdown 文件。
> **Codex 直接读文件，不依赖对话转述。**

## 分工边界（2026-09-07 定稿）

| 职责 | 负责人 | 产出位置 |
|---|---|---|
| 数据生成脚本 | Codex | `data/generate_data.py` |
| 数据库 Schema | Codex | `data/init.sql` |
| 后端主代码（FastAPI 链路、agent、llm、api） | Codex | `backend/` |
| 业务指标 Glossary | Codex | `backend/config/metrics.yaml` |
| 评测集 | **WorkBuddy** | `eval/cases.jsonl` |
| 文档（架构、数据字典、安全设计） | **WorkBuddy** | `docs/` |
| 只读审查（对 Codex 提交的代码） | **WorkBuddy** | `docs/collab/review-*.md` |
| README / .gitignore | **WorkBuddy** | 项目根目录 |

## 协作规则

1. **不互改同一文件**。WorkBuddy 只写 `eval/`、`docs/`、`README.md`、`.gitignore`；Codex 只写 `data/`、`backend/`、`frontend/`。
2. **Codex 提交代码后**，在 `docs/collab/` 新增一份 `review-<模块>.md` 记录审查结论，Codex 据此修复。
3. **接口契约一旦定稿**写入 `interface-contract.md`，双方都不得单方面改动字段名。
4. **数据口径以 `data_dictionary.md` 为准**，评测集和 SQL 生成都引用它。

## 文件索引

- [`handoff.md`](handoff.md) — 当前交接状态、待决项、下一步
- [`interface-contract.md`](interface-contract.md) — 后端 API 接口契约
- [`task-list.md`](task-list.md) — Codex 的待办任务清单
- [`review-notes.md`](review-notes.md) — 对已交付文件的审查笔记
