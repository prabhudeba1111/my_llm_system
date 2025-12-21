import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = "my_llm_system"
    environment: str = os.getenv("ENVIRONMENT", "local")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
