import random
import time

from src.config import settings
from src.errors import CallerError, FatalError, TransientError
from src.llm.base import BaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger


class MockLLM(BaseLLM):
    def __init__(self, max_retries: int = settings.max_retries):
        self.max_retries = max_retries
        self.logger = setup_logger()

    def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        attempt = 0

        while attempt <= self.max_retries:
            attempt += 1
            start_time = time.time()

            try:
                # Simulated Failures
                if not request.prompt.strip():
                    raise ValueError("Empty Prompt")
                
                if random.random() < 0.7:
                    raise TimeoutError("Simulated Network Timeout")

                if random.random() < 0.2:
                    return LLMFailure(
                        reason = "Empty model output",
                        error_type=TransientError
                    )
                
                # Simulated Success
                latency = (time.time() - start_time) * 1000
                response = LLMResponse(
                    text = f"[MOCK LLM] Response to: {request.prompt}",
                    tokens_used = len(request.prompt.split()),
                    latency_ms = latency,
                )
                
                if not response.text.strip():
                    return LLMFailure(
                        reason="Empty model output",
                        error_type=TransientError
                    )

                self.logger.info(
                    f"Mock LLM call succeeded in {latency:.2f} ms"
                    f"(tokens={response.tokens_used})"
                )
                return response
            
            except ValueError as e:
                return LLMFailure(reason = str(e), error_type=CallerError)

            except TimeoutError as e:
                self.logger.warning(f"Attempt {attempt}: timeout ({e})")
                if attempt >= self.max_retries:
                    return LLMFailure(reason = str(e), error_type=TransientError)
                
            except Exception as e:
                return LLMFailure(reason = str(e), error_type=FatalError)
            
        return LLMFailure(reason = "Unknown failure", error_type=FatalError)
