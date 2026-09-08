from pathlib import Path
from app.metrics.glossary import MetricsGlossary

PATH = Path(__file__).parents[2] / "config" / "metrics.yaml"
def test_load_and_match_metrics():
    glossary = MetricsGlossary.load(PATH)
    assert {m.key for m in glossary.match("2026 年 8 月的销售额和客单价")} == {"sales_amount", "average_order_value"}
def test_refund_and_after_sales_are_separate():
    glossary = MetricsGlossary.load(PATH)
    assert glossary.metrics["refund_amount"].table == "refunds"
    assert glossary.metrics["after_sales_resolution_hours"].table == "after_sales"
