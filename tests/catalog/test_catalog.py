from pathlib import Path
from app.catalog.descriptions import TABLE_DESCRIPTIONS
from app.catalog.schema import SchemaCatalog
from app.db.sqlite import SQLiteDatabase

DB = Path(__file__).parents[2] / "data" / "test_catalog.db"
def setup_module():
    import sqlite3
    con = sqlite3.connect(DB); con.executescript((Path(__file__).parents[2] / "data" / "init.sql").read_text(encoding="utf-8")); con.close()
def teardown_module():
    try:
        DB.unlink(missing_ok=True)
    except PermissionError:
        # Windows may release SQLite's final handle slightly after the test.
        pass
def test_catalog_contains_ten_business_tables():
    assert set(SchemaCatalog(SQLiteDatabase(DB), TABLE_DESCRIPTIONS).tables) == set(TABLE_DESCRIPTIONS)
def test_validator_shape_and_prompt_context():
    catalog = SchemaCatalog(SQLiteDatabase(DB), TABLE_DESCRIPTIONS)
    assert "refunds" in catalog.prompt_context()
    assert any(t["name"] == "order_items" and {c["name"] for c in t["columns"]} >= {"line_paid_amount", "subtotal_profit"} for t in catalog.to_table_infos())

def test_chinese_question_keeps_join_dimensions():
    catalog = SchemaCatalog(SQLiteDatabase(DB), TABLE_DESCRIPTIONS)
    names = {t.name for t in catalog.relevant(["长沙门店销售额"])}
    assert {"orders", "stores"}.issubset(names)
