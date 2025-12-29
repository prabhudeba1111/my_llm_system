import pytest

from src.llm.async_mock import AsyncMockLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse


@pytest.mark.asyncio
async def test_async_mock_success(monkeypatch):
    monkeypatch.setattr("random.random", lambda:0.9)

    llm = AsyncMockLLM()
    request = LLMRequest(prompt="Hello LLM")

    result = await llm.generate(request)

    assert isinstance(result, LLMResponse)
    assert result.text


@pytest.mark.asyncio
async def test_async_mock_empty_prompt():
    with pytest.raises(ValueError):
        LLMRequest(prompt="")


@pytest.mark.asyncio
async def test_async_mock_timeout(monkeypatch):
    def always_timeout():
        raise TimeoutError("Simulated timeout")

    monkeypatch.setattr(AsyncMockLLM, "generate", always_timeout)