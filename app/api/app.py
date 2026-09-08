from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent.query_service import QueryService
from app.catalog.descriptions import TABLE_DESCRIPTIONS
from app.catalog.schema import SchemaCatalog
from app.db.sqlite import SQLiteDatabase
from app.llm.client import MockLLMClient, OpenAICompatibleClient
import os
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError
import httpx

ROOT = Path(__file__).resolve().parents[2]
class QueryRequest(BaseModel): question: str
def create_app(db_path: str | Path | None = None, cases_path: str | Path | None = None) -> FastAPI:
    db = SQLiteDatabase(db_path or ROOT / "data" / "enterprise.db")
    catalog = SchemaCatalog(db, TABLE_DESCRIPTIONS)
    glossary = MetricsGlossary.load(ROOT / "config" / "metrics.yaml")
    if os.getenv("LLM_MODE", "mock") == "real":
        llm = OpenAICompatibleClient()
    else:
        llm = MockLLMClient(str(cases_path or ROOT / "eval" / "cases.jsonl"))
    service = QueryService(catalog, glossary, llm)
    app = FastAPI(title="Enterprise Data Analysis Agent")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    @app.get("/api/health")
    def health():
        db_ok = db.health()
        llm_ok = os.getenv("LLM_MODE", "mock") == "mock" or bool(os.getenv("LLM_API_KEY"))
        return {"status": "ok" if db_ok and llm_ok else "degraded", "db": "ok" if db_ok else "error", "llm": "ok" if llm_ok else "error"}
    @app.post("/api/query")
    def query(request: QueryRequest):
        try: return service.query(request.question).to_dict()
        except SQLValidationError as exc: raise HTTPException(400, detail={"error": "sql_invalid", "violations": exc.violations})
        except RuntimeError as exc: raise HTTPException(400, detail={"error": "db_error", "message": str(exc)})
        except httpx.HTTPError as exc: raise HTTPException(502, detail={"error": "llm_error", "message": str(exc)})
        except (ValueError, FileNotFoundError) as exc: raise HTTPException(422, detail=str(exc))
    return app
