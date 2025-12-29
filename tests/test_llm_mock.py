import pytest

from src.llm.mock import MockLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse


def test_mock_llm_success(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.9)

    llm = MockLLM()
    request = LLMRequest(prompt="Hello LLM")

    result = llm.generate(request)

    assert isinstance(result, LLMResponse)
    assert result.text

def test_mock_llm_empty_prompt():
    with pytest.raises(ValueError):
        LLMRequest(prompt="")

def test_mock_llm_timeout(monkeypatch):
    def always_timeout():
        raise TimeoutError("Simulated timeout")

    monkeypatch.setattr(MockLLM, "generate", always_timeout)