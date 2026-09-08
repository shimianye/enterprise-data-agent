"""Controlled question -> SQL -> validated execution service."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any
import sqlite3

from app.catalog.schema import SchemaCatalog
from app.llm.client import LLMClient
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError, check_sql_safety
from app.agent.explanation import explain
from app.agent.presentation import build_presentation, column_label

@dataclass
class QueryResult:
    question: str
    sql: str
    rows: list[dict[str, Any]]
    duration_ms: int
    metric_keys: list[str]
    warnings: list[str]
    intent: str
    chart_type: str
    chart_data: dict[str, Any] | None
    nl_explanation: str
    columns: list[dict[str, Any]]
    def to_dict(self): return asdict(self)

class QueryService:
    def __init__(self, catalog: SchemaCatalog, glossary: MetricsGlossary, llm: LLMClient):
        self.catalog, self.glossary, self.llm = catalog, glossary, llm

    def query(self, question: str) -> QueryResult:
        started = perf_counter()
        metrics = self.glossary.match(question)
        context = (
            "业务指标定义（指标名不是字段名，请按定义展开）:\n"
            + self.glossary.prompt_context(metrics)
            + "\n\n数据库表结构:\n"
            + self.catalog.prompt_context(self.catalog.relevant([question] + [m.name for m in metrics]))
        )
        raw_sql = self.llm.generate_sql(question, context)
        safety = check_sql_safety(raw_sql, table_infos=self.catalog.to_table_infos())
        if not safety.is_safe:
            raise SQLValidationError(safety.violations)
        try:
            rows = self.catalog.db.execute(safety.normalized_sql)
        except sqlite3.Error as exc:
            raise RuntimeError(f"database query failed: {exc}") from exc
        intent, chart_type, chart_data = build_presentation(question, rows)
        nl_explanation = explain(question, intent, chart_data, rows)
        columns = []
        if rows:
            for name in rows[0]:
                values = [row.get(name) for row in rows[:20]]
                columns.append({"name": name, "label": column_label(name), "is_numeric": any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values)})
        return QueryResult(
            question, safety.normalized_sql, rows,
            int((perf_counter() - started) * 1000),
            [m.key for m in metrics], safety.warnings,
            intent, chart_type, chart_data, nl_explanation, columns,
        )
