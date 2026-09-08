# 审查笔记 Review Notes

> WorkBuddy 对已交付文件的审查记录。Codex 按"结论"列处理。

## v0 草稿审查（即将废弃，仅留档）

### data/init.sql（v0，9 张表）

| # | 问题 | 严重度 | 结论 |
|---|---|---|---|
| 1 | `CREATE INDEX` 不带 `IF NOT EXISTS`，SQLite 跑会报错 | 中 | Codex 重写时加容错 |
| 2 | 无外键约束（仅索引），表关系隐含在字段名 | 低 | 有意的（写入性能），重写时保留 |
| 3 | TINYINT(1) 在 MySQL 8.0 正常，老版本 deprecated | 低 | 忽略 |

### data/generate_data.py（v0，579 行）

| # | 问题 | 严重度 | 结论 |
|---|---|---|---|
| 1 | 无事务包裹，中断会留脏数据 | 高 | 重写时加 try/except |
| 2 | 重复运行会 PK 冲突（无幂等） | 高 | 重写时用 `if_exists="replace"` 或 TRUNCATE |
| 3 | `generate_for_mysql` 用 `split(";")` 切 SQL，注释里 `;` 会误切 | 中 | 重写时用 SQLAlchemy 逐条执行 |
| 4 | 单进程生成，5 万订单耗时 5-10 分钟 | 低 | 可接受 |
| 5 | 无 seed.sql 导出 | 低 | 按需 |
| 6 | 无 eval 评测集生成钩子 | 中 | 评测集由 WorkBuddy 单独写 eval/cases.jsonl |

### README.md（v0）

| # | 问题 | 严重度 | 结论 |
|---|---|---|---|
| 1 | 未写协作模式（codex + WorkBuddy） | 中 | WorkBuddy 后续补 |
| 2 | 目录结构未含 docs/collab/ | 低 | 一并更新 |

---

## 后续审查计划

Phase 2 每个模块完成后，新增 `review-<模块名>.md`，覆盖：
- 代码规范 / 可读性
- 接口契约一致性
- SQL 安全校验是否真能拦住危险语句
- 错误处理是否完善
- 可测试性（能否被 eval 调用）
