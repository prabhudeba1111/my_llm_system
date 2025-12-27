import pytest
from src.config import validate_settings, Settings
from src.errors import FatalError


def test_valid_config_passes():
    settings = Settings(
        llm_mode="mock",
        max_retries=3,
        timeout_seconds=5,
        max_concurrency=2,
        log_level="INFO",
    )
    validate_settings(settings)


def test_invalid_llm_mode_fails():
    settings = Settings(llm_mode="invalid")

    with pytest.raises(FatalError):
        validate_settings(settings)


def test_local_requires_url():
    settings = Settings(llm_mode="local", local_llm_url=None)

    with pytest.raises(FatalError):
        validate_settings(settings)
