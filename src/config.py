import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = "my_llm_system"
    environment: str = os.getenv("ENVIRONMENT", "local")

    llm_provider: str | None = os.getenv("LLM_PROVIDER", None)
    llm_model: str | None = os.getenv("LLM_MODEL", None)

    llm_mode: str = os.getenv("LLM_MODE", "mock")
    llm_api_key: str | None = os.getenv("LLM_API_KEY", None)

    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
