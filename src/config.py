import os

from dotenv import load_dotenv
from pydantic import BaseModel

from src.errors import FatalError

load_dotenv()

VALID_LLM_MODES = {"mock", "local"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


class Settings(BaseModel):
    app_name: str = "my_llm_system"

    llm_mode: str = os.getenv("LLM_MODE", None)
    max_retries: int = int(os.getenv("MAX_RETRIES", None))
    timeout_seconds: float = float(os.getenv("TIMEOUT_SECONDS", None))
    max_concurrency: int = int(os.getenv("MAX_CONCURRENCY", None))
    
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY", None)

    log_level: str = os.getenv("LOG_LEVEL", None)
    local_llm_url: str | None = os.getenv("LOCAL_LLM_URL")


def validate_settings(settings) -> None:
    errors: list[str] = []

    if settings.llm_mode not in VALID_LLM_MODES:
        errors.append(f"Invalid LLM_MODE='{settings.llm_mode}'")

    if settings.max_retries < 0 or settings.max_retries > 10:
        errors.append("MAX_RETRIES must be between 0 and 10")
    
    if not settings.timeout_seconds > 0:
        errors.append("TIMEOUT_SECONDS must be > 0")

    if settings.max_concurrency <= 0:
        errors.append("MAX_CONCURRENCY must be > 0")

    if settings.log_level not in VALID_LOG_LEVELS:
        errors.append(f"Invalid LOG_LEVEL='{settings.log_level}'")
    
    if settings.llm_mode == "local" and not settings.local_llm_url:
        errors.append("LOCAL_LLM_URL is required when LLM_MODE=local")

    if errors:
        raise FatalError("\nInvalid configuration:\n- " + "\n- ".join(errors))


def resolved_config(settings: Settings) -> dict:
    return {
        "backend": settings.llm_mode,
        "max_retries": settings.max_retries,
        "timeout_seconds": settings.timeout_seconds,
        "max_concurrency": settings.max_concurrency,
        "log_level": settings.log_level,
    }


settings = Settings()
