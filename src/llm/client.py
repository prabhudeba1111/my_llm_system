from src.config import settings
from src.llm.async_local import AsyncLocalLLM
from src.llm.async_mock import AsyncMockLLM
from src.llm.base import AsyncBaseLLM, BaseLLM
from src.llm.local import LocalLLM
from src.llm.mock import MockLLM


def get_llm_client() -> BaseLLM:
    mode = settings.llm_mode

    if mode == "mock":
        return MockLLM()

    if mode == "local":
        return LocalLLM()


def get_async_llm_client() -> AsyncBaseLLM:
    mode = settings.llm_mode

    if mode == "mock":
        return AsyncMockLLM()

    if mode == "local":
        return AsyncLocalLLM()

