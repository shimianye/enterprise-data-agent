import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.app import create_app


ROOT = Path(__file__).parents[2]


def _database(path: Path) -> None:
    with sqlite3.connect(path) as connection:
        connection.executescript((ROOT / "data/init.sql").read_text(encoding="utf-8"))
        connection.execute("insert into stores values(1,'测试店','长沙','华中','直营','2024-01-01',1)")
        connection.execute("insert into customers values(1,'测试客户','男',30,'长沙','华中','普通','2024-01-01')")
        connection.execute("insert into orders(order_id,order_no,customer_id,store_id,order_status,order_amount,discount_amount,freight_amount,paid_amount,cost_amount,profit_amount,item_count,channel,created_at,paid_at) values(1,'x',1,1,'paid',1,0,0,1,0,1,1,'x','2026-08-01','2026-08-01')")


def test_feedback_records_and_updates_known_query(tmp_path):
    database = tmp_path / "business.db"
    feedback = tmp_path / "feedback.db"
    _database(database)
    client = TestClient(create_app(database, ROOT / "eval/cases.jsonl", feedback))

    query = client.post("/api/query", json={"question": "2026 年 8 月的总销售额"})
    assert query.status_code == 200
    payload = query.json()
    assert payload["confidence"] == "high"

    response = client.post(
        "/api/feedback",
        json={"query_id": payload["query_id"], "rating": "incorrect", "comment": "口径需确认"},
    )
    assert response.status_code == 200
    with sqlite3.connect(feedback) as connection:
        row = connection.execute(
            "SELECT rating, comment FROM query_feedback WHERE query_id = ?", (payload["query_id"],)
        ).fetchone()
    assert row == ("incorrect", "口径需确认")


def test_feedback_rejects_unknown_query_and_invalid_rating(tmp_path):
    database = tmp_path / "business.db"
    _database(database)
    client = TestClient(create_app(database, ROOT / "eval/cases.jsonl", tmp_path / "feedback.db"))

    missing = client.post(
        "/api/feedback",
        json={"query_id": "missing-query", "rating": "correct"},
    )
    assert missing.status_code == 404
    invalid = client.post(
        "/api/feedback",
        json={"query_id": "missing-query", "rating": "maybe"},
    )
    assert invalid.status_code == 422
