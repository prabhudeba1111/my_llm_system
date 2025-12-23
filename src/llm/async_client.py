import os

from src.llm.async_local import AsyncLocalLLM
from src.llm.async_mock import AsyncMockLLM


def get_async_llm_client():
    mode = os.getenv("LLM_MODE", "mock").lower()

    if mode == "mock":
        return AsyncMockLLM()

    if mode == "local":
        return AsyncLocalLLM()

    raise ValueError(f"Invalid LLM_MODE '{mode}'")
