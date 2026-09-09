from app.agent.quality import assess_query_quality


def test_basic_grounded_result_is_high_confidence():
    result = assess_query_quality(
        question="2026 年 8 月总销售额",
        metric_keys=["sales_amount"],
        warnings=["limit_injected"],
        rows=[{"sales": 100}],
        intent="metric_query",
    )
    assert result.confidence == "high"
    assert result.needs_review is False


def test_advanced_query_is_low_and_explains_review():
    result = assess_query_quality(
        question="今年各月销售额环比增长率",
        metric_keys=["sales_amount"],
        warnings=[],
        rows=[{"month": "2026-01", "growth": 0.1}],
        intent="trend",
    )
    assert result.confidence == "low"
    assert result.needs_review is True
    check = next(c for c in result.checks if c.code == "advanced_query")
    assert check.passed is False


def test_empty_result_is_medium_not_false_success():
    result = assess_query_quality(
        question="各等级客户数",
        metric_keys=[],
        warnings=[],
        rows=[],
        intent="comparison",
    )
    assert result.confidence == "medium"
    assert result.needs_review is True
