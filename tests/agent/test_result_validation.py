from app.agent.result_validation import validate_result


def test_flags_empty_and_percentage_outliers():
    assert validate_result("销售额", [], "metric_query") == ("empty", ["empty_result"])
    status, warnings = validate_result("占比", [{"ratio": 120}], "metric_query")
    assert status == "warning"
    assert "percentage_out_of_range" in warnings


def test_flags_missing_time_dimension_for_trend():
    status, warnings = validate_result("按月看销售趋势", [{"sales": 10}], "trend")
    assert status == "warning"
    assert "time_dimension_missing" in warnings
