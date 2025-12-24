import asyncio
import random
import time

from src.llm.base import AsyncBaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger


class AsyncRateLimiter:
    def __init__(self, rate_per_sec: int):
        self._interval = 1.0 / rate_per_sec
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            wait = self._interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
                self._last = time.time()


class AsyncMockLLM(AsyncBaseLLM):
    def __init__(
        self,
        max_retries: int = 3,
        max_concurrency: int = 5,
        total_timeout: int = 10.0,
        rate_limiter_per_sec: int = 5,
    ):
        self.max_retries = max_retries
        self.total_timeout = total_timeout
        self.logger = setup_logger()

        self._rate_limiter = AsyncRateLimiter(rate_limiter_per_sec)
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        async with self._semaphore:
            try:
                return await asyncio.wait_for(
                    self._generate_with_retries(request),
                    timeout=self.total_timeout,
                )

            except asyncio.TimeoutError:
                return LLMFailure(
                    reason="Total timeout budget exceeded", retryable=False
                )

    async def _generate_with_retries(
        self, request: LLMRequest
    ) -> LLMResponse | LLMFailure:
        attempt = 0

        while attempt <= self.max_retries:
            attempt += 1
            start_time = time.time()

            try:
                await self._rate_limiter.acquire()
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

            except asyncio.CancelledError:
                self.logger.warning("Async LLM request cancelled")
                raise

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
