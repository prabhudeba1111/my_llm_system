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
    llm = MockLLM()
    request = LLMRequest(prompt="")

    result = llm.generate(request)

    assert isinstance(result, LLMFailure)
    assert result.retryable is False

def test_mock_llm_timeout(monkeypatch):
    monkeypatch.setattr("random.random", lambda:0.1)

    llm = MockLLM()
    request = LLMRequest(prompt="Hello LLM")

    result = llm.generate(request)

    assert isinstance(result, LLMFailure)
    assert result.retryable is True