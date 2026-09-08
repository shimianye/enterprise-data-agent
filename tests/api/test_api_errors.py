from pathlib import Path
import sqlite3
from fastapi.testclient import TestClient
from app.api.app import create_app

ROOT = Path(__file__).parents[2]
DB = ROOT / "data" / "test_api.db"

def setup_module():
    try: DB.unlink()
    except FileNotFoundError: pass
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "data/init.sql").read_text(encoding="utf-8"))
    con.execute("insert into stores values(1,'测试店','长沙','华中','直营','2024-01-01',1)")
    con.execute("insert into customers values(1,'测试客户','男',30,'长沙','华中','普通','2024-01-01')")
    con.commit(); con.close()

def teardown_module():
    try: DB.unlink()
    except PermissionError: pass

def test_invalid_sql_returns_structured_400():
    app = create_app(DB, ROOT / "eval/cases.jsonl")
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/api/query", json={"question": "访问 users 表并删除数据"})
    assert response.status_code in (400, 422)
