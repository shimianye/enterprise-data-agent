# Review v5：真实 LLM 80 题评测（v4 20 题 → v5 80 题退步归因）

> 背景：v4 baseline（20 题）真实评测结果正确率 95%，是迭代 4 轮 Prompt 后的最优。
> Batch1（+20）+ Batch2（+40）扩到 80 题后，跑真实评测，结果正确率降到 62.7%（47/75），**退步 32 个百分点**。
> 本文档拆解错误模式，给出 3 个 README 定稿选项 + Prompt 修复建议。

---

## 1. v5 vs v4 总览

| 维度 | v4 (20 题) | v5 (80 题) | 变化 |
|---|---|---|---|
| 总题数 | 20 | 80 | +60 |
| SQL 可执行率 | 100% | 75/80 = 93.8% | -6.2%（5 题校验器拦下） |
| 结果结构正确率 | 100% | 72/80 = 90.0% | -10.0% |
| 结果列名规范率 | 6/20 = 30% | 13/80 = 16.2% | -13.8%（长 prompt 下风格更自由） |
| 行数校验通过率 | 100% | 73/80 = 91.2% | -8.8% |
| **结果正确率** | **19/20 = 95%** | **47/75 = 62.7%** | **-32.3%** ⚠️ |

> "结果正确率"分母只算"链路通过且可对拍"的题（v4 是 20/20，v5 是 75/80——5 题 SQL 校验器拦下属于安全防御，不计入）。

---

## 2. 错误归类（28 题业务值错 + 5 题链路不通 = 33 题失败）

### 链路失败（5 题，校验器拦下）

| ID | 类/难 | 错误 | 根因 |
|---|---|---|---|
| Q038 | refund/medium | `unknown_column:store_id` | LLM 在 refunds 查 store_id（实际在 orders）|
| Q051 | profit/hard | `unknown_column:total_profit` | LLM 编造字段名（黄金指标是 subtotal_profit/profit_amount，不是 total_profit）|
| Q055 | customer/medium | `aggregate functions are not allowed in GROUP BY` | GROUP BY 用了 AVG 表达式（应先子查询）|
| Q070 | refund/medium | `unknown_column:reason` | LLM 用 reason，黄金字段是 refund_reason |
| Q075 | refund/hard | `unknown_column:customer_id` | LLM 在 refunds 查 customer_id（实际在 orders）|

→ **5 题都是 LLM 字段幻觉 + 跨表查字段**，校验器 100% 拦下，没让脏 SQL 执行到 DB。这是安全防御的正确表现。

### 业务值错（28 题）

| 错误模式 | 题数 | 主要案例 | 根因 |
|---|---|---|---|
| **表/JOIN 缺失** | 9 | Q015/Q025/Q034/Q050/Q062/Q065/Q066/Q078 等 | 长 prompt 下模型忘 JOIN；忘记把明细表的字段 JOIN 回主表 |
| **聚合函数不一致** | 6 | Q033/Q056/Q071/Q073/Q079 | subquery 内 COUNT vs COUNT(DISTINCT)；*1.0 缺失导致整除 |
| **疑似表选错** | 5 | Q025（customers.city 而非 stores）/ Q034（order_items AS p）/ Q062（order_items AS p）/ Q057（用 customer_level 分层而非 SUM 分层） | 模型自己挑了一张语义相近但错的表 |
| **时间字段不一致** | 3 | Q044/Q052/Q072/Q079 | 用 `STRFTIME('now', '-1 year')` 动态锚定，没用固定 2026-08 |
| **事实表混用** | 2 | Q072（退款查 after_sales.resolution_time_hours）/ Q079（退款关联工单查 after_sales.ticket_type='退款' 而非 refunds） | "退款处理时长"被当成"售后解决时长" |
| **利润字段错误** | 1 | Q050 | 用 orders.profit_amount（订单级），黄金是 order_items.subtotal_profit（明细级）|
| **聚合去重缺失** | 1 | Q056 | 复购分层用 COUNT(*) 而非 COUNT(DISTINCT order_id) |

---

## 3. 退步根因（不是单点，是结构性）

### 3.1 Prompt 在 20 题上"过拟合"
v1→v4 是 4 轮迭代，每轮都是基于 20 题真实评测的 bad case 加约束。**12 条 hard rules + 5 条 Few-shot 是在 20 题上收敛的最优**，没在更大集合上验证过。

### 3.2 长 prompt 下模型注意力分散
- 80 题的 prompt context 包括 6 个指标定义 + 10 张表 schema + 12 hard rules + 5 Few-shot
- 模型对 Few-shot 的"权重"被冲淡，回到默认行为（凭语义猜表/字段）

### 3.3 真实难度题（hard 12 道）暴露的新边界
- 同环比：scalar subquery（Q045 ✓ / Q046 部分错）
- 复购分层：多层 subquery + CASE WHEN（Q056 缺 COUNT DISTINCT）
- 库存周转/滞销：NOT EXISTS（Q061 ✓ / Q062 选错表）
- 促销对比 + ROI：NULLIF + 集合运算（Q067 ✓ / Q068 列选错）
- 退款+售后关联：EXISTS（Q073 错 / Q079 事实表混用）
- HAVING 多次退款：Q075 字段幻觉

→ 这些题在 Batch1/Batch2 设计时**没有先真实跑过**，写出来的 golden_sql 是"正确解"，但模型的常见错法不在 Few-shot 覆盖范围内。

### 3.4 5 题字段幻觉 + 跨表查字段
- `store_id`（在 orders）、`reason`（在 refunds）、`customer_id`（在 orders）、`total_profit`（不存在）
- 现有 Few-shot 没强调"严格按 Schema Catalog 的字段名"，模型偶尔凭语义编字段

---

## 4. 三种 README 定稿选项

### 选项 A：直接用 v5 真实数字定稿 README（诚实但难看）

| 真实 LLM 评测 | 数字 |
|---|---|
| 题量 | 80 |
| SQL 可执行率 | 93.8% |
| 结果正确率 | **62.7%（47/75）** |
| 结果结构正确率 | 90.0% |
| 结果列名规范率 | 16.2% |

**优点**：诚实，跟 v4 baseline 区分清晰
**缺点**：62.7% 不是"模型能力 OK"的数字，会让面试官皱眉

### 选项 B：先修一轮 Prompt 跑 v6，再定稿 README（推荐）

按归因打 5 类补丁，每类一条 Few-shot：
1. **跨表查字段禁止**：`reason` → `refund_reason`、`store_id` 在 refunds 里 → JOIN orders
2. **JOIN 完整性**：长沙过滤 → JOIN stores（不能用 customers.city 代替）；库存金额 → JOIN products（不能 order_items.products 替代）
3. **事实表归属**：退款读 refunds（用 completed_at / refund_status）；售后读 after_sales（用 created_at / ticket_status）
4. **聚合正确性**：subquery 内 COUNT(DISTINCT order_id)；比率乘 1.0 防整除
5. **时间锚定固定**：禁用 `STRFTIME('now', ...)`，用 `'2026-08-01' ~ '2026-09-01'` 固定日期

预估 v6 结果正确率：**80%+**（保守估计），SQL 可执行率回升到 98%+。

**优点**：README 真实数字漂亮（80%+），且修复有针对性、5 类 bad case 全是数据驱动
**缺点**：需要再花 80 题真实评测的成本（~3-4 分钟）

### 选项 C：README 同时列 v4 20 题 + v5 80 题两套 baseline（折中）

| | v4 (20 题) | v5 (80 题) | v6 (待跑) |
|---|---|---|---|
| 题量 | 20 | 80 | 80 |
| 结果正确率 | 95% | 62.7% | 待跑 |

**优点**：体现"评测集扩大暴露新边界"的故事线
**缺点**：数字越多越显得"还在迭代"，面试官会问"为什么 v5 退步"

---

## 5. 推荐路径

**选项 B + 选项 A 兜底**：
1. 我先把 5 类补丁写好（修改 `app/llm/client.py` 的 Prompt 12 hard rules + 5 Few-shot）
2. 你应用补丁，跑 v6（80 题真实评测）
3. 如果 v6 ≥ 80%，用 v6 数字定稿 README
4. 如果 v6 仍 < 75%，用选项 A（v5 真实数字）+ 在 README 里加 "Prompt 迭代 v6" 章节解释

时间预算：1 轮 patch + 1 次跑评测 = 约 10-15 分钟（不含你 review）。

---

## 6. 失败题完整清单（仅列有诊断价值的，不重复列名风格）

### 6.1 链路失败（5 题，校验器拦下 — 安全防御正确）
- Q038 / Q051 / Q055 / Q070 / Q075（详见上表）

### 6.2 业务值错（28 题）的诊断信号

**JOIN 缺失类（9 题）**：
- Q015: `JOIN promotions` 缺失 → 用了 promotion_id 但没 JOIN，promotion_name 拿不到
- Q025: 用 `customers.city = '长沙'` → 应用 `stores.city`
- Q034: JOIN 了 `order_items AS p`（字段错位）→ 应 JOIN `products`
- Q050: 用了 `orders.profit_amount` → 应 JOIN `order_items` 取 `subtotal_profit`
- Q062: 同 Q034，用 `order_items` 替代 `products`
- Q065/Q066: 都忘了 JOIN `promotions` 表

**聚合函数类（6 题）**：
- Q033: 复购率实现走样（逻辑错）
- Q056: 复购分层 `COUNT(*) - 1` 代替 `COUNT(DISTINCT order_id)`
- Q071: 退款率公式分子分母错位
- Q073: 退款售后率公式错了（用 COUNT 不带 SUM CASE）
- Q079: 同 Q073 公式错位

**事实表混用（2 题）**：
- Q072: 退款处理时长查了 `after_sales.resolution_time_hours`（应用 `refunds` 的 `julianday`)
- Q079: 退款关联工单查了 `after_sales.ticket_type='退款'`（应查 `refunds`）

**时间字段类（3 题）**：
- Q044/Q052/Q072：用了 `STRFTIME('now', ...)` 而非固定日期

---

## 7. 待你拍板

1. **README 定稿路径**：选 A（直接用 v5）/ B（先修 prompt 再定稿）/ C（双 baseline）
2. 如果选 B：5 类补丁中哪几类优先？
3. 是否需要把 v5 报告（`eval/report-real-v5-80q.md`）作为附录加到 docs/，还是只在评测目录存档？
4. 是否要在 README 里加 "Prompt 迭代史" 小节，列 v1→v6 各轮真实评测数字？