from __future__ import annotations
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from app.agent.query_service import QueryService
from app.catalog.descriptions import TABLE_DESCRIPTIONS
from app.catalog.schema import SchemaCatalog
from app.db.sqlite import SQLiteDatabase
from app.llm.client import MockLLMClient, OpenAICompatibleClient
import os
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError
from app.feedback import FeedbackStore
import httpx

ROOT = Path(__file__).resolve().parents[2]
class QueryRequest(BaseModel): question: str
class FeedbackRequest(BaseModel):
    query_id: str = Field(min_length=8, max_length=64)
    rating: Literal["correct", "incorrect"]
    comment: str | None = Field(default=None, max_length=500)

def create_app(db_path: str | Path | None = None, cases_path: str | Path | None = None, feedback_path: str | Path | None = None) -> FastAPI:
    db = SQLiteDatabase(db_path or ROOT / "data" / "enterprise.db")
    catalog = SchemaCatalog(db, TABLE_DESCRIPTIONS)
    glossary = MetricsGlossary.load(ROOT / "config" / "metrics.yaml")
    # An explicit cases_path is the deterministic/offline test contract.
    if cases_path is None and os.getenv("LLM_MODE", "mock") == "real":
        llm = OpenAICompatibleClient()
    else:
        llm = MockLLMClient(str(cases_path or ROOT / "eval" / "cases.jsonl"))
    service = QueryService(catalog, glossary, llm)
    feedback = FeedbackStore(feedback_path or ROOT / "data" / "feedback.db")
    app = FastAPI(title="Enterprise Data Analysis Agent")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    @app.get("/api/health")
    def health():
        db_ok = db.health()
        llm_ok = os.getenv("LLM_MODE", "mock") == "mock" or bool(os.getenv("LLM_API_KEY"))
        return {"status": "ok" if db_ok and llm_ok else "degraded", "db": "ok" if db_ok else "error", "llm": "ok" if llm_ok else "error"}
    @app.post("/api/query")
    def query(request: QueryRequest):
        try:
            payload = service.query(request.question).to_dict()
            try:
                feedback.record_query(payload)
            except sqlite3.Error:
                payload["warnings"].append("feedback_store_unavailable")
            return payload
        except SQLValidationError as exc: raise HTTPException(400, detail={"error": "sql_invalid", "violations": exc.violations})
        except RuntimeError as exc: raise HTTPException(400, detail={"error": "db_error", "message": str(exc)})
        except httpx.HTTPError as exc: raise HTTPException(502, detail={"error": "llm_error", "message": str(exc)})
        except (ValueError, FileNotFoundError) as exc: raise HTTPException(422, detail=str(exc))
    @app.post("/api/feedback")
    def save_feedback(request: FeedbackRequest):
        try:
            if not feedback.save_feedback(request.query_id, request.rating, request.comment):
                raise HTTPException(404, detail={"error": "query_not_found"})
            return {"ok": True, "query_id": request.query_id, "rating": request.rating}
        except sqlite3.Error as exc:
            raise HTTPException(503, detail={"error": "feedback_store_error"}) from exc

    @app.get("/api/feedback/summary")
    def feedback_summary():
        """Return aggregate feedback metrics for an admin dashboard."""
        try:
            return feedback.summary()
        except sqlite3.Error as exc:
            raise HTTPException(503, detail={"error": "feedback_store_error"}) from exc
    return app
