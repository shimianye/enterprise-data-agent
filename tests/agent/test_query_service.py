import sqlite3
from pathlib import Path
from app.agent.query_service import QueryService
from app.catalog.descriptions import TABLE_DESCRIPTIONS
from app.catalog.schema import SchemaCatalog
from app.db.sqlite import SQLiteDatabase
from app.llm.client import MockLLMClient
from app.metrics.glossary import MetricsGlossary
from app.security.validator import SQLValidationError
import pytest

ROOT = Path(__file__).parents[2]
DB = ROOT / "data" / "test_query.db"
def setup_module():
    try: DB.unlink()
    except FileNotFoundError: pass
    con=sqlite3.connect(DB); con.executescript((ROOT/"data/init.sql").read_text(encoding="utf-8")); con.execute("insert into stores values(1,'测试店','长沙','华中','直营','2024-01-01',1)"); con.execute("insert into customers values(1,'测试客户','男',30,'长沙','华中','普通','2024-01-01')"); con.execute("insert into orders(order_id,order_no,customer_id,store_id,order_status,order_amount,discount_amount,freight_amount,paid_amount,cost_amount,profit_amount,item_count,channel,created_at,paid_at) values(1,'x',1,1,'paid',1,0,0,1,0,1,1,'x','2026-08-01','2026-08-01')"); con.commit(); con.close()
def teardown_module():
    try: DB.unlink(missing_ok=True)
    except PermissionError: pass
def test_query_service_uses_safety_and_limit():
    service=QueryService(SchemaCatalog(SQLiteDatabase(DB),TABLE_DESCRIPTIONS), MetricsGlossary.load(ROOT/"config/metrics.yaml"), MockLLMClient(str(ROOT/"eval/cases.jsonl")))
    result=service.query("2026 年 8 月的总销售额")
    assert result.rows[0]["sales"] == 1
    assert "LIMIT" in result.sql.upper()
    assert result.query_id
    assert result.attempt_count == 1
    assert result.confidence == "high"
    assert result.quality_checks


def _service_with(llm):
    return QueryService(
        SchemaCatalog(SQLiteDatabase(DB), TABLE_DESCRIPTIONS),
        MetricsGlossary.load(ROOT / "config/metrics.yaml"),
        llm,
    )


def test_validation_failure_repairs_once_then_succeeds():
    class Repairing:
        def __init__(self): self.repairs = 0
        def generate_sql(self, question, context): return "DELETE FROM orders"
        def repair_sql(self, question, context, previous_sql, error):
            self.repairs += 1
            assert "select" in error
            return "SELECT SUM(paid_amount) AS sales FROM orders"

    llm = Repairing()
    result = _service_with(llm).query("总销售额")
    assert result.attempt_count == 2
    assert llm.repairs == 1


def test_dangerous_repair_is_revalidated_and_stops_after_one_retry():
    class Unsafe:
        def __init__(self): self.repairs = 0
        def generate_sql(self, question, context): return "DELETE FROM orders"
        def repair_sql(self, question, context, previous_sql, error):
            self.repairs += 1
            return "DROP TABLE orders"

    llm = Unsafe()
    with pytest.raises(SQLValidationError):
        _service_with(llm).query("删除订单")
    assert llm.repairs == 1
