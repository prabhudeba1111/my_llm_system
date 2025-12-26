from src import main
from src.errors import CallerError, TransientError
from src.llm.models import LLMResponse, LLMFailure


def test_run_success(monkeypatch):
    monkeypatch.setattr(
        "src.main.get_llm_client",
        lambda: DummySuccessLLM(),
    )

    assert main.run() == 0


def test_run_known_failure(monkeypatch):
    monkeypatch.setattr(
        "src.main.get_llm_client",
        lambda: DummyFailLLM(),
    )

    assert main.run() == 1


def test_caller_error_is_not_retryable():
    failure = LLMFailure("bad input", CallerError)
    assert not issubclass(failure.error_type, TransientError)


def test_transient_error_is_retryable():
    failure = LLMFailure("timeout", TransientError)
    assert issubclass(failure.error_type, TransientError)


class DummySuccessLLM:
    def generate(self, request):
        return LLMResponse(text="ok")


class DummyFailLLM:
    def generate(self, request):
        return LLMFailure("fail", error_type=TransientError)
