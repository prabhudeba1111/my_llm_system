import time

import httpx

from src.llm.base import BaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger


class LocalLLM(BaseLLM):
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.logger = setup_logger()
        self.url = "http://localhost:11434/v1/completions"

    def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        start_time = time.time()

        payload = {
            "model": "phi",
            "prompt": request.prompt,
            "temperature": 0.9,
            "max_tokens": 50
        }

        try:
            with httpx.Client(timeout=request.timeout_seconds) as client:
                response = client.post(self.url, json=payload)

                if response.status_code != 200:
                    return LLMFailure(
                        f"Local LLM HTTP {response.status_code}",
                        retryable=False,
                    )
                
                data = response.json()
                text = data["choices"][0]["text"]
                
                if not text.strip():
                    return LLMFailure("Empty model output", retryable=False)
                
                latency = (time.time() - start_time) * 1000

                self.logger.info(f"Local LLM succeded in {latency:.2f} ms")

                return LLMResponse(
                    text,
                    latency_ms=latency
                )
            
        except httpx.TimeoutException:
            return LLMFailure("Local LLM timeout", retryable=True)

        except Exception as e:
            return LLMFailure(str(e), retryable=False)
