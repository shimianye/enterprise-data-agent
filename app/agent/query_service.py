"""Controlled question -> SQL -> validated execution service."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from time import perf_counter
from typing import Any
import sqlite3
import uuid

from app.catalog.schema import SchemaCatalog
from app.llm.client import LLMClient
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError, check_sql_safety
from app.agent.explanation import explain
from app.agent.presentation import build_presentation, column_label
from app.agent.quality import assess_query_quality
from app.agent.result_validation import validate_result

@dataclass
class QueryResult:
    query_id: str
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
    attempt_count: int
    confidence: str
    needs_review: bool
    quality_checks: list[dict[str, Any]]
    result_status: str
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
        safety = None
        rows = None
        attempt_count = 0
        last_error: SQLValidationError | sqlite3.Error | None = None
        for attempt_count in (1, 2):
            safety = check_sql_safety(raw_sql, table_infos=self.catalog.to_table_infos())
            if not safety.is_safe:
                last_error = SQLValidationError(safety.violations)
            else:
                try:
                    rows = self.catalog.db.execute(safety.normalized_sql)
                    break
                except sqlite3.Error as exc:
                    last_error = exc
            if attempt_count == 2:
                break
            repair = getattr(self.llm, "repair_sql", None)
            if repair is None:
                break
            failure = (
                ",".join(last_error.violations)
                if isinstance(last_error, SQLValidationError)
                else f"database_error:{str(last_error)[:200]}"
            )
            raw_sql = repair(question, context, raw_sql, failure)

        if rows is None or safety is None or not safety.is_safe:
            if isinstance(last_error, SQLValidationError):
                raise last_error
            if isinstance(last_error, sqlite3.Error):
                raise RuntimeError(f"database query failed: {last_error}") from last_error
            raise RuntimeError("database query failed")
        intent, chart_type, chart_data = build_presentation(question, rows)
        nl_explanation = explain(question, intent, chart_data, rows)
        columns = []
        if rows:
            for name in rows[0]:
                values = [row.get(name) for row in rows[:20]]
                columns.append({"name": name, "label": column_label(name), "is_numeric": any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values)})
        metric_keys = [m.key for m in metrics]
        quality = assess_query_quality(
            question=question,
            metric_keys=metric_keys,
            warnings=safety.warnings,
            rows=rows,
            intent=intent,
        )
        result_status, result_warnings = validate_result(question, rows, intent)
        warnings = list(safety.warnings) + result_warnings
        return QueryResult(
            query_id=uuid.uuid4().hex,
            question=question,
            sql=safety.normalized_sql,
            rows=rows,
            duration_ms=int((perf_counter() - started) * 1000),
            metric_keys=metric_keys,
            warnings=warnings,
            intent=intent,
            chart_type=chart_type,
            chart_data=chart_data,
            nl_explanation=nl_explanation,
            columns=columns,
            attempt_count=attempt_count,
            confidence=quality.confidence,
            needs_review=quality.needs_review,
            quality_checks=quality.checks_as_dicts(),
            result_status=result_status,
        )
