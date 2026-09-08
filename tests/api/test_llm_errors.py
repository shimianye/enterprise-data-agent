from pathlib import Path
import sqlite3
import httpx
from fastapi.testclient import TestClient
from app.api.app import create_app
from app.agent.query_service import QueryService

ROOT = Path(__file__).parents[2]
DB = ROOT / "data" / "test_llm_error.db"

def setup_module():
    try: DB.unlink(missing_ok=True)
    except (FileNotFoundError, PermissionError): pass
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "data/init.sql").read_text(encoding="utf-8"))
    con.execute("insert into stores values(1,'测试店','长沙','华中','直营','2024-01-01',1)")
    con.execute("insert into customers values(1,'测试客户','男',30,'长沙','华中','普通','2024-01-01')")
    con.commit(); con.close()

def teardown_module():
    try: DB.unlink()
    except PermissionError: pass

def test_http_error_maps_to_502():
    app = create_app(DB, ROOT / "eval/cases.jsonl")
    # Exercise the public error contract with a provider-like failure.
    class Failing:
        def generate_sql(self, question, context):
            raise httpx.ConnectError("upstream unavailable")
    # Replace the service captured by the route closure.
    route = next(r for r in app.routes if getattr(r, "path", "") == "/api/query")
    for cell in route.endpoint.__closure__ or ():
        if isinstance(cell.cell_contents, QueryService):
            cell.cell_contents.llm = Failing()
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/api/query", json={"question": "2026 年 8 月的总销售额"})
    assert response.status_code == 502
    assert response.json()["detail"]["error"] == "llm_error"
