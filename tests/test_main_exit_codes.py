from src import main


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


class DummySuccessLLM:
    def generate(self, request):
        from src.llm.models import LLMResponse
        return LLMResponse(text="ok")


class DummyFailLLM:
    def generate(self, request):
        from src.llm.models import LLMFailure
        return LLMFailure("fail", retryable=False)
