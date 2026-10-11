"""Unit tests for typed AnalysisError taxonomy and error codes."""

import pytest
from app.core.models import AnalysisError, AnalysisErrorCode


def test_error_code_enumeration():
    expected_codes = {
        "SYNTAX_ERROR",
        "REFERENCE_MISMATCH",
        "OUT_OF_BOUNDS",
        "INVALID_COORDINATE",
        "UNSUPPORTED_VARIANT",
        "AMBIGUOUS_VARIANT",
        "EXTERNAL_SOURCE_UNAVAILABLE",
    }
    actual_codes = {c.value for c in AnalysisErrorCode}
    assert expected_codes.issubset(actual_codes)


def test_analysis_error_properties():
    err = AnalysisError(
        code=AnalysisErrorCode.SYNTAX_ERROR,
        message="Malformed query string",
        details={"raw_query": "foo_bar"},
    )
    assert isinstance(err, Exception)
    assert err.code == AnalysisErrorCode.SYNTAX_ERROR
    assert err.message == "Malformed query string"
    assert err.details["raw_query"] == "foo_bar"
    assert str(err) == "[SYNTAX_ERROR] Malformed query string"


def test_raise_and_catch_analysis_error():
    with pytest.raises(AnalysisError) as exc_info:
        raise AnalysisError(
            code=AnalysisErrorCode.REFERENCE_MISMATCH,
            message="Base mismatch at c.118",
        )
    assert exc_info.value.code == AnalysisErrorCode.REFERENCE_MISMATCH
    assert "Base mismatch at c.118" in str(exc_info.value)
