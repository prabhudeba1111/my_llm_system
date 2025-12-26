import pytest

from src.config import validate_settings
from src.errors import FatalError


class DummySettings:
    def __init__(
        self,
        llm_mode="mock",
        max_retries=3,
        timeout_seconds=5,
        max_concurrency=2,
        log_level="INFO",
    ):
        self.llm_mode = llm_mode
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.max_concurrency = max_concurrency
        self.log_level = log_level


def test_valid_config_passes():
    settings = DummySettings()
    validate_settings(settings)  # should not raise


def test_invalid_llm_mode_fails():
    settings = DummySettings(llm_mode="invalid")

    with pytest.raises(FatalError) as exc:
        validate_settings(settings)

    assert "Invalid LLM_MODE" in str(exc.value)


def test_negative_retries_fail():
    settings = DummySettings(max_retries=-1)

    with pytest.raises(FatalError):
        validate_settings(settings)
