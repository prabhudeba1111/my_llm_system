import time

import httpx

from src.llm.base import AsyncBaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger
from src.config import settings
from src.errors import TransientError, CallerError, FatalError


class AsyncLocalLLM(AsyncBaseLLM):
    def __init__(self, max_retries: int = settings.max_retries):
        self.max_retries = max_retries
        self.logger = setup_logger()
        self.url = "http://localhost:11434/v1/completions"

    async def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        start_time = time.time()

        if not request.prompt.strip():
            return LLMFailure("Empty Prompt", error_type=CallerError)

        payload = {
            "model": "phi",
            "prompt": request.prompt,
            "max_tokens": 300
        }

        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                response = await client.post(self.url, json=payload)

                if response.status_code != 200:
                    return LLMFailure(
                        f"Local LLM HTTP {response.status_code}",
                        error_type=FatalError
                    )
                
                data = response.json()
                text = data["choices"][0]["text"]
                
                if not text.strip():
                    return LLMFailure("Empty model output", error_type=TransientError)
                
                latency = (time.time() - start_time) * 1000

                self.logger.info(f"Async Local LLM succeded in {latency:.2f} ms")

                return LLMResponse(
                    text,
                    latency_ms=latency
                )
            
        except httpx.TimeoutException:
            return LLMFailure("Local LLM timeout", error_type=TransientError)

        except Exception as e:
            return LLMFailure(str(e), error_type=FatalError)
