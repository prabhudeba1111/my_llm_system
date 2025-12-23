import asyncio
import random
import time

from src.llm.base import AsyncBaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger


class AsyncMockLLM(AsyncBaseLLM):
    def __init__(self, max_retries: int = 3, max_concurrency: int = 5):
        self.max_retries = max_retries
        self.logger = setup_logger()
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        async with self._semaphore:
            attempt = 0

            while attempt <= self.max_retries:
                attempt += 1
                start_time = time.time()

                try:
                    await asyncio.sleep(0.5)

                    # Simulated Failures
                    if not request.prompt.strip():
                        raise ValueError("Empty Prompt")

                    if random.random() < 0.7:
                        raise TimeoutError("Simulated Network Timeout")

                    if random.random() < 0.2:
                        return LLMFailure(
                            reason="Empty model output",
                            retryable=False,
                        )

                    # Simulated Success
                    latency = (time.time() - start_time) * 1000
                    response = LLMResponse(
                        text=f"[Async MOCK LLM] Response to: {request.prompt}",
                        tokens_used=len(request.prompt.split()),
                        latency_ms=latency,
                    )

                    self.logger.info(
                        f"Async Mock LLM call succeeded in {latency:.2f} ms "
                        f"(tokens={response.tokens_used})"
                    )
                    return response

                except TimeoutError as e:
                    self.logger.warning(f"Attempt {attempt}: timeout ({e})")
                    if attempt >= self.max_retries:
                        return LLMFailure(
                            reason=str(e),
                            retryable=True,
                        )

                except Exception as e:
                    self.logger.error(f"Attempt {attempt}: failure ({e})")
                    return LLMFailure(
                        reason=str(e),
                        retryable=False,
                    )

            return LLMFailure(reason="Unknown failure", retryable=False)
