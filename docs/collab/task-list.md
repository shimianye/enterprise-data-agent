# Codex 任务清单 Task List

> 按依赖顺序排列。完成一项后在 `handoff.md` 里勾掉并更新状态。

## Phase 1 — 数据层（Codex）

- [ ] **P1-1** 确认 5 个待决项（见 handoff.md），更新本清单
- [ ] **P1-2** 编写 `data/init.sql`（10 张表，字段见 handoff.md）
  - 每字段带中文 COMMENT（Schema 检索质量依赖它）
  - 主键、索引、唯一约束
  - 兼容 MySQL 8.0；如用 SQLite 开发，索引需 IF NOT EXISTS
- [ ] **P1-3** 编写 `data/generate_data.py`
  - 规模：5 万订单 / 10 万明细 / 1 万客户 / 20 门店 / 12 个月
  - 遵守业务规则（状态机、时间链单调性、退款触发）
  - 双 11 / 618 大促加权
  - 可重复运行（幂等，不重复插入）
  - 支持 `--db sqlite|mysql`
- [ ] **P1-4** 生成并验证 `data/enterprise.db`（SQLite 演示数据）
  - 输出各表行数统计

## Phase 2 — 后端主链路（Codex）

- [ ] **P2-1** `backend/app/config.py` — 环境变量、DB DSN、LLM 配置
- [ ] **P2-2** `backend/app/db/connector.py` — 只读连接池（SQLite 实现）
- [ ] **P2-3** `backend/app/agent/intent.py` — 意图识别
- [ ] **P2-4** `backend/app/agent/schema_retriever.py` — Schema 检索（embedding）
- [ ] **P2-5** `backend/app/agent/sql_generator.py` — Text2SQL（含 few-shot prompt）
- [x] **P2-6** `backend/app/agent/sql_validator.py` — SQL 安全校验 — **已交付**
  - ✅ WorkBuddy 已交付 `app/security/validator.py`（446 行 + 50 个测试）
  - 集成时 `from app.security.validator import check_sql_safety, SQLValidationError`
  - 接口契约详见文件 docstring
- [ ] **P2-7** `backend/app/agent/chart_selector.py` — 图表类型推断
- [ ] **P2-8** `backend/app/agent/explainer.py` — 结果自然语言解释
- [ ] **P2-9** `backend/app/llm/client.py` — LLM 统一客户端（Qwen/GPT 切换）
- [ ] **P2-10** `backend/config/metrics.yaml` — 业务指标 Glossary
- [ ] **P2-11** `backend/app/main.py` — FastAPI 入口，装配全链路
- [ ] **P2-12** `backend/app/api/query.py` + `health.py` — 按接口契约实现
- [ ] **P2-13** `backend/requirements.txt` + `docker-compose.yml`

## Phase 3 — 前端（可选，第二版）

- [ ] 简单数据工作台（React + ECharts 或 Streamlit 快速 demo）

## 交付约定

- 每完成一个 Phase，在 `handoff.md` 更新状态
- WorkBuddy 会在 Phase 2 每个模块完成后出 `review-<模块>.md`
- 所有接口字段名严格遵循 `interface-contract.md`
