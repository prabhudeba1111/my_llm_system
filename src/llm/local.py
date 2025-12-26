import time

import httpx

from src.llm.base import BaseLLM
from src.llm.models import LLMFailure, LLMRequest, LLMResponse
from src.utils import setup_logger
from src.config import settings
from src.errors import TransientError, CallerError, FatalError

class LocalLLM(BaseLLM):
    def __init__(self, max_retries: int = settings.max_retries):
        self.max_retries = max_retries
        self.logger = setup_logger()
        self.url = "http://localhost:11434/v1/completions"

    def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        attempt = 0

        while attempt <= self.max_retries:
            attempt += 1
            start_time = time.time()

            try:
                if not request.prompt.strip():
                    return LLMFailure("Empty Prompt", error_type=CallerError)


                payload = {
                    "model": "phi",
                    "prompt": request.prompt,
                    "temperature": 0.9,
                    "max_tokens": 300
                }
            
                with httpx.Client(timeout=request.timeout_seconds) as client:
                    response = client.post(self.url, json=payload)

                    if response.status_code != 200:
                        return LLMFailure(
                            f"Local LLM HTTP {response.status_code}",
                            error_type=FatalError
                        )
                    
                    data = response.json()
                    text = data["choices"][0]["text"]
                    
                    if not text.strip():
                        raise ValueError("Response Empty")
                    
                    latency = (time.time() - start_time) * 1000

                    self.logger.info(f"Local LLM succeded in {latency:.2f} ms")

                    return LLMResponse(
                        text,
                        latency_ms=latency
                    )
                
            except ValueError as e:
                self.logger.warning(f"Attempt {attempt}: Empty Response")
                if attempt >= self.max_retries:
                    return LLMFailure("Local LLM Empty Response", error_type=TransientError)

            except httpx.TimeoutException:
                self.logger.warning(f"Attempt {attempt}: timeout")
                if attempt >= self.max_retries:
                    return LLMFailure("Local LLM timeout", error_type=TransientError)

            except Exception as e:
                return LLMFailure(str(e), error_type=FatalError)

        return LLMFailure(
            reason="Unknown Local LLM failure",
            error_type=FatalError,
        )