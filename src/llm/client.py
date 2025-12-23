import os

from src.config import settings
from src.llm.base import BaseLLM
from src.llm.local import LocalLLM
from src.llm.mock import MockLLM


def get_llm_client() -> BaseLLM:
    mode = os.getenv("LLM_MODE", "mock").lower()

    if mode == "mock":
        return MockLLM()

    if mode == "local":
        return LocalLLM()

    raise ValueError(
        f"Invalid LLM_MODE '{settings.llm_mode}'. "
        "Expected 'mock' or 'local'."
    )
