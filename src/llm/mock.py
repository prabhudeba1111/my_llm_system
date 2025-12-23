import random
import time

from src.llm.base import BaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger


class MockLLM(BaseLLM):
    def __init__(self):
        self.logger = setup_logger()

    def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        start = time.time()

        if not request.prompt.strip():
            return LLMFailure("Empty prompt", retryable=False)

        if random.random() < 0.2:
            return LLMFailure("Simulated timeout", retryable=True)

        if random.random() < 0.2:
            return LLMFailure("Empty model output", retryable=False)

        latency = (time.time() - start) * 1000

        self.logger.info(
            f"Mock LLM succeeded in {latency:.2f} ms"
        )

        return LLMResponse(
            text=f"[MOCK] {request.prompt}",
            tokens_used=len(request.prompt.split()),
            latency_ms=latency,
        )
