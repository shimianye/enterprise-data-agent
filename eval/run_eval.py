"""
Text2SQL 评测执行脚本
======================

两种模式：
  1. Mock 模式（默认）—— LLM 返回 golden_sql，验证「链路完整性」
     （SQL 可执行率 / 形状正确率 / 端到端成功率）
  2. 真实 LLM 模式 —— LLM 自行生成 SQL，验证「生成质量」
     （SQL 可执行率 / 结果正确率 / 形状正确率）

结果正确率：LLM 生成的 SQL 执行结果 vs golden_sql 执行结果，
做「浮点容忍 + 行序无关」的等价比较。

用法（在项目根目录）：
    python eval/run_eval.py                            # 默认 Mock 模式（读 LLM_MODE）
    python eval/run_eval.py --mode real                # 真实 LLM（读 LLM_API_KEY/LLM_BASE_URL/LLM_MODEL）
    python eval/run_eval.py --db data/enterprise.db
    python eval/run_eval.py --report eval/report.md

真实 LLM 模式环境变量（见 app/llm/client.py）：
    LLM_MODE=real        # 或 --mode real
    LLM_API_KEY=...      # 必填
    LLM_BASE_URL=...     # 可选，默认 https://api.deepseek.com（不带 /v1 结尾）
    LLM_MODEL=...        # 可选，默认 deepseek-chat
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent.query_service import QueryService
from app.catalog.descriptions import TABLE_DESCRIPTIONS
from app.catalog.schema import SchemaCatalog
from app.db.sqlite import SQLiteDatabase
from app.llm.client import LLMClient, MockLLMClient, OpenAICompatibleClient
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError, check_sql_safety

import sqlglot
from sqlglot import exp


# ============================================================
# 结果比较（浮点容忍 + 行序无关）
# ============================================================
def _normalize_rows(rows: list[dict[str, Any]]) -> list[tuple]:
    """把查询结果规范化为可比较的 tuple 列表（浮点四舍五入、行序无关）。"""
    normalized = []
    for row in rows:
        norm_row = tuple(
            round(float(v), 6) if isinstance(v, (int, float)) else str(v)
            for v in row.values()
        )
        normalized.append(norm_row)
    return sorted(normalized)


def results_equal(a: list[dict], b: list[dict]) -> bool:
    """比较两个查询结果是否等价。"""
    return _normalize_rows(a) == _normalize_rows(b)


# ============================================================
# SQL 差异诊断（golden vs 生成，供 Prompt 调优）
# ============================================================
_TIME_FIELDS = (
    "paid_at", "created_at", "completed_at", "requested_at",
    "snapshot_date", "registered_at", "opened_at", "launched_at",
    "shipped_at", "delivered_at", "cancelled_at", "first_response_at",
    "resolved_at", "closed_at",
)
_AGG_FUNCS = ("SUM", "COUNT", "AVG", "MAX", "MIN")


def _sql_features(sql: str) -> dict:
    """提取 SQL 的结构特征（表、列、时间列、聚合函数）。解析失败时返回空特征。"""
    feats = {
        "tables": set(),
        "columns": set(),
        "time_cols": set(),
        "aggs": set(),
        "lower": (sql or "").lower(),
    }
    try:
        tree = sqlglot.parse_one(sql, read="sqlite")
    except Exception:
        return feats
    for t in tree.find_all(exp.Table):
        feats["tables"].add(t.name)
    for c in tree.find_all(exp.Column):
        feats["columns"].add(c.name.lower())
    for col in feats["columns"]:
        if col in _TIME_FIELDS:
            feats["time_cols"].add(col)
    for fn in tree.find_all(exp.Func):
        name = (fn.sql_name() or "").upper()
        if name in _AGG_FUNCS:
            feats["aggs"].add(name)
    return feats


def diff_sql(golden: str, generated: str) -> list[str]:
    """对比 golden 与生成 SQL，输出差异标签（启发式，供诊断非精确判定）。"""
    if not generated:
        return []
    g = _sql_features(golden)
    d = _sql_features(generated)
    tags: list[str] = []

    # 1. 缺少业务过滤 paid_amount > 0
    if "paid_amount > 0" in g["lower"] and "paid_amount > 0" not in d["lower"]:
        if "paid_amount" in d["lower"]:
            tags.append("缺少业务过滤：paid_amount > 0")

    # 2. 指标字段错误（order_amount vs paid_amount；利润粒度）
    if ("paid_amount" in g["columns"] and "order_amount" in d["columns"]
            and "paid_amount" not in d["columns"]):
        tags.append("指标字段错误：用了 order_amount，应为 paid_amount")
    if ("subtotal_profit" in g["columns"] and "profit_amount" in d["columns"]
            and "subtotal_profit" not in d["columns"]):
        tags.append("利润字段错误：用了 profit_amount，明细粒度应为 subtotal_profit")

    # 3. 时间字段不一致
    if g["time_cols"] and d["time_cols"] and g["time_cols"] != d["time_cols"]:
        tags.append(f"时间字段不一致：golden={sorted(g['time_cols'])} 生成={sorted(d['time_cols'])}")

    # 4. 缺少 strftime 时间分桶
    if "strftime" in g["lower"] and "strftime" not in d["lower"]:
        tags.append("缺少 strftime 时间分桶")

    # 5. 聚合去重缺失（COUNT(DISTINCT) vs COUNT）
    if ("count(distinct" in g["lower"]
            and "count(distinct" not in d["lower"]
            and "count(" in d["lower"]):
        tags.append("聚合去重缺失：应 COUNT(DISTINCT ...)")

    # 6. 聚合函数不一致
    if g["aggs"] and d["aggs"] and g["aggs"] != d["aggs"]:
        tags.append(f"聚合函数不一致：golden={sorted(g['aggs'])} 生成={sorted(d['aggs'])}")

    # 7. 表/JOIN 缺失（golden 引用了、生成没引用）
    missing = g["tables"] - d["tables"]
    if missing:
        tags.append(f"表/JOIN 缺失：{sorted(missing)}")

    # 8. 疑似表选错（生成引用了 golden 没用的表）
    extra = d["tables"] - g["tables"]
    if extra:
        tags.append(f"疑似表选错（golden 未用）：{sorted(extra)}")

    # 9. 退款/售后事实表混用
    if "refunds" in g["tables"] and "after_sales" in d["tables"] and "refunds" not in d["tables"]:
        tags.append("事实表混用：退款应读 refunds，不是 after_sales")
    if "after_sales" in g["tables"] and "refunds" in d["tables"] and "after_sales" not in d["tables"]:
        tags.append("事实表混用：售后应读 after_sales，不是 refunds")

    return tags


# ============================================================
# 形状校验
# ============================================================
def check_shape(rows: list[dict], expected_shape: str) -> bool:
    n_rows = len(rows)
    n_cols = len(rows[0]) if rows else 0
    if expected_shape == "single_value":
        return n_rows == 1 and n_cols == 1
    if expected_shape == "list":
        return n_rows >= 1
    if expected_shape == "time_series":
        return n_rows >= 2
    if expected_shape == "table":
        return n_rows >= 1
    return False


def check_row_count(rows: list[dict], expected_check: str) -> bool:
    if not expected_check or "row_count" not in expected_check:
        return True
    n_rows = len(rows)
    try:
        left, right = expected_check.split("==")
        if "row_count" in left:
            return n_rows == int(right.strip())
    except (ValueError, IndexError):
        pass
    return True


def check_columns_named(rows: list[dict], expected_columns: list[str]) -> bool:
    """列名是否严格匹配预期（列名规范率：多列/少列/改名都判不一致）。"""
    if not expected_columns:
        return True
    if not rows:
        return False
    return set(rows[0].keys()) == set(expected_columns)


def check_structure(rows: list[dict], expected_shape: str, expected_columns: list[str]) -> bool:
    """结果结构是否正确（行形状 + 列数，别名无关）。"""
    if not check_shape(rows, expected_shape):
        return False
    if expected_columns and (not rows or len(rows[0]) != len(expected_columns)):
        return False
    return True


# ============================================================
# 评测主逻辑
# ============================================================
def load_cases(cases_path: Path) -> list[dict]:
    cases = []
    with cases_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def run(
    cases_path: Path,
    db_path: Path,
    metrics_path: Path,
    llm: LLMClient | None = None,
) -> list[dict]:
    """对每个 case 跑链路，统计各项指标。

    Mock 模式下 `llm` 用 MockLLMClient（question → golden_sql）。
    真实 LLM 模式下传入真实 LLMClient 实现，即可评测「结果正确率」。
    """
    cases = load_cases(cases_path)
    db = SQLiteDatabase(db_path)
    catalog = SchemaCatalog(db, TABLE_DESCRIPTIONS)
    glossary = MetricsGlossary.load(metrics_path)
    llm = llm or MockLLMClient(str(cases_path))
    service = QueryService(catalog, glossary, llm)
    table_infos = catalog.to_table_infos()

    results = []
    for case in cases:
        cid = case["id"]
        question = case["question"]
        golden_sql = case["golden_sql"]
        entry = {
            "id": cid,
            "category": case.get("category", ""),
            "difficulty": case.get("difficulty", ""),
            "question": question,
            "golden_sql": golden_sql,
            "status": "failed",
            "error": "",
            "structure_ok": False,
            "row_count_ok": False,
            "columns_named_ok": False,
            "actual_columns": [],
            "expected_columns": case.get("expected_columns", []),
            "result_correct": False,
            "result_correct_checkable": False,  # golden_sql 无法执行时置 False
            "duration_ms": 0,
            "sql": "",
            "diff_tags": [],
            "metric_keys": [],
        }

        # 1. 跑主链路（LLM 生成 SQL → 校验 → 执行）
        try:
            qr = service.query(question)
            entry["status"] = "passed"
            entry["duration_ms"] = qr.duration_ms
            entry["sql"] = qr.sql
            entry["metric_keys"] = qr.metric_keys
            entry["actual_columns"] = list(qr.rows[0].keys()) if qr.rows else []
            entry["columns_named_ok"] = check_columns_named(
                qr.rows, case.get("expected_columns", [])
            )
            entry["structure_ok"] = check_structure(
                qr.rows,
                case.get("expected_shape", ""),
                case.get("expected_columns", []),
            )
            entry["row_count_ok"] = check_row_count(
                qr.rows, case.get("expected_result_check", "")
            )
            llm_rows = qr.rows
        except SQLValidationError as exc:
            entry["error"] = f"sql_invalid: {exc.violations}"
            results.append(entry)
            continue
        except (ValueError, FileNotFoundError) as exc:
            entry["error"] = str(exc)
            results.append(entry)
            continue
        except Exception as exc:  # noqa: BLE001
            entry["error"] = f"{type(exc).__name__}: {exc}"
            results.append(entry)
            continue

        # 2. 执行 golden_sql 作为基准，对比「结果正确率」
        try:
            golden = check_sql_safety(golden_sql, table_infos=table_infos)
            if golden.is_safe:
                golden_rows = db.execute(golden.normalized_sql)
                entry["result_correct"] = results_equal(llm_rows, golden_rows)
                entry["result_correct_checkable"] = True
        except Exception:
            # golden_sql 执行失败 → 该题结果正确率不可评估
            entry["result_correct_checkable"] = False

        # 3. 差异诊断：结果错误时，对比 golden 与生成 SQL 的差异
        if (entry["status"] == "passed" and entry["result_correct_checkable"]
                and not entry["result_correct"]):
            entry["diff_tags"] = diff_sql(golden_sql, entry["sql"])

        results.append(entry)
    return results


def summarize(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    structure_ok = sum(1 for r in results if r["structure_ok"])
    row_count_ok = sum(1 for r in results if r["row_count_ok"])
    columns_named_ok = sum(1 for r in results if r["columns_named_ok"])
    checkable = sum(1 for r in results if r["result_correct_checkable"])
    result_correct = sum(1 for r in results if r["result_correct"])
    return {
        "total": total,
        "sql_executable": passed,
        "sql_executable_rate": passed / total if total else 0.0,
        "structure_correct": structure_ok,
        "structure_correct_rate": structure_ok / total if total else 0.0,
        "row_count_correct": row_count_ok,
        "row_count_correct_rate": row_count_ok / total if total else 0.0,
        "column_name_correct": columns_named_ok,
        "column_name_correct_rate": columns_named_ok / total if total else 0.0,
        "result_correct": result_correct,
        "result_correct_rate": result_correct / checkable if checkable else 0.0,
        "result_checkable": checkable,
    }


def format_report(results: list[dict], summary: dict) -> str:
    lines = []
    lines.append("=" * 62)
    lines.append("Text2SQL 评测报告")
    lines.append("=" * 62)
    lines.append("")
    lines.append(f"总题数: {summary['total']}")
    lines.append(f"SQL 可执行率: {summary['sql_executable']}/{summary['total']} "
                 f"= {summary['sql_executable_rate']:.1%}")
    lines.append(f"结果结构正确率: {summary['structure_correct']}/{summary['total']} "
                 f"= {summary['structure_correct_rate']:.1%}")
    lines.append(f"结果列名规范率: {summary['column_name_correct']}/{summary['total']} "
                 f"= {summary['column_name_correct_rate']:.1%}")
    lines.append(f"行数校验通过率: {summary['row_count_correct']}/{summary['total']} "
                 f"= {summary['row_count_correct_rate']:.1%}")
    lines.append(f"结果正确率: {summary['result_correct']}/{summary['result_checkable']} "
                 f"= {summary['result_correct_rate']:.1%}")
    lines.append("")
    lines.append("-" * 62)
    lines.append(f"{'ID':<6}{'状态':<6}{'结构':<5}{'结果':<5}{'耗时':<7}类别/难度")
    lines.append("-" * 62)
    for r in results:
        status = "✓" if r["status"] == "passed" else "✗"
        struct = "✓" if r["structure_ok"] else "✗"
        correct = "✓" if r["result_correct"] else ("-" if not r["result_correct_checkable"] else "✗")
        cat_diff = f"{r['category']}/{r['difficulty']}"
        lines.append(
            f"{r['id']:<6}{status:<6}{struct:<5}{correct:<5}"
            f"{r['duration_ms']:<7}{cat_diff}"
        )
        if r["error"]:
            lines.append(f"       ↳ 错误: {r['error']}")
        if r["status"] == "passed" and r.get("expected_columns") and not r.get("columns_named_ok"):
            lines.append(f"       ↳ 列名不符（风格/字段）：实际={r.get('actual_columns')} 预期={r.get('expected_columns')}")
        for tag in r.get("diff_tags", []):
            lines.append(f"       ↳ {tag}")

    # 结果错误明细：逐题对比 golden vs 生成 SQL
    wrong = [r for r in results if r["status"] == "passed" and r["result_correct_checkable"] and not r["result_correct"]]
    if wrong:
        lines.append("")
        lines.append("=" * 62)
        lines.append("结果错误明细（golden vs 生成）")
        lines.append("=" * 62)
        for r in wrong:
            lines.append(f"\n【{r['id']}】{r['question']}")
            lines.append(f"  golden   : {r['golden_sql']}")
            lines.append(f"  生成     : {r['sql']}")
            if r.get("expected_columns") and not r.get("columns_named_ok"):
                lines.append(f"  ↳ 列名不符：实际={r.get('actual_columns')} 预期={r.get('expected_columns')}")
            for tag in r.get("diff_tags", []):
                lines.append(f"  ↳ {tag}")
    lines.append("")
    lines.append("=" * 62)
    return "\n".join(lines)


def build_llm(mode: str, cases_path: Path) -> LLMClient:
    """按模式构建 LLM 客户端。

    - mock: MockLLMClient（question → golden_sql，确定性，验证链路完整性）
    - real: OpenAICompatibleClient（读取 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL）

    缺 LLM_API_KEY 时抛 ValueError，由调用方给出友好提示。
    """
    if mode == "real":
        return OpenAICompatibleClient()
    return MockLLMClient(str(cases_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Text2SQL 评测")
    parser.add_argument("--db", default=str(PROJECT_ROOT / "data" / "enterprise.db"))
    parser.add_argument("--cases", default=str(PROJECT_ROOT / "eval" / "cases.jsonl"))
    parser.add_argument("--metrics", default=str(PROJECT_ROOT / "config" / "metrics.yaml"))
    parser.add_argument("--report", default=None, help="额外输出报告到文件")
    parser.add_argument("--save-sql", default=None, help="额外输出每题的 golden/生成 SQL 及差异标签到 JSONL")
    parser.add_argument(
        "--mode",
        default=os.getenv("LLM_MODE", "mock"),
        choices=["mock", "real"],
        help="mock 或 real（默认读 LLM_MODE 环境变量）",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"错误：数据库不存在 {db_path}")
        print("请先运行数据生成器生成 enterprise.db，例如：")
        print("  python data/generate_data.py --db sqlite --output data/enterprise.db")
        return 1

    try:
        llm = build_llm(args.mode, Path(args.cases))
    except ValueError as exc:
        print(f"错误：{exc}")
        print("真实 LLM 模式需要配置环境变量：")
        print("  LLM_MODE=real")
        print("  LLM_API_KEY=<你的 key>     # 必填")
        print("  LLM_BASE_URL=<base url>    # 可选，默认 https://api.deepseek.com")
        print("  LLM_MODEL=<model>          # 可选，默认 deepseek-chat")
        return 1

    if args.mode == "real":
        client = llm  # type: OpenAICompatibleClient
        print(f"真实 LLM 模式：base_url={client.base_url} model={client.model}")
        print()

    results = run(Path(args.cases), db_path, Path(args.metrics), llm=llm)
    summary = summarize(results)
    report = format_report(results, summary)
    print(report)

    if args.report:
        Path(args.report).write_text(report + "\n", encoding="utf-8")
        print(f"\n报告已写入: {args.report}")

    if args.save_sql:
        Path(args.save_sql).write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n",
            encoding="utf-8",
        )
        print(f"SQL 明细已写入: {args.save_sql}")

    return 0 if summary["sql_executable"] == summary["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
