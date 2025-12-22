from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMRequest:
    prompt: str
    max_token: int = 256
    temperature: float = 0.9
    timeout_seconds: float = 10.0

@dataclass
class LLMResponse:
    text: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None

@dataclass
class LLMFailure:
    reason: str
    retryable: bool
