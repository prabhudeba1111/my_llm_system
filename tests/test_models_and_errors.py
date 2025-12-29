import pytest

from src.errors import CallerError, TransientError
from src.llm.models import LLMFailure, LLMResponse


def test_llm_failure_positional_and_keyword():
    f1 = LLMFailure(user_message="bad input", error_type=CallerError)
    assert f1.user_message == "bad input"
    assert f1.internal_message is None


def test_llm_failure_invalid_error_type():
    with pytest.raises(TypeError):
        LLMFailure("bad", error_type=str)


def test_llm_response_latency_validation():
    # None latency is allowed
    r = LLMResponse(text="ok", latency_ms=None)
    assert r.latency_ms is None

    # Negative latency is invalid
    with pytest.raises(ValueError):
        LLMResponse(text="ok", latency_ms=-1)


def test_llm_system_error_init_and_str():
    e = CallerError("user msg", "internal msg")
    assert e.user_message == "user msg"
    assert e.internal_message == "internal msg"
    assert str(e).startswith(CallerError.code)


def test_retryable_and_exit_code():
    f = LLMFailure(user_message="timeout", error_type=TransientError)
    assert f.retryable is True
    assert f.exit_code == TransientError.exit_code
