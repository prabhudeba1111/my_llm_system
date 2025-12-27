from dataclasses import dataclass
from typing import Optional, Type

from src.config import settings
from src.errors import LLMSystemError


@dataclass
class LLMRequest:
    prompt: str
    max_token: int = 256
    temperature: float = 0.9
    timeout_seconds: float = settings.timeout_seconds

@dataclass
class LLMResponse:
    text: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None

@dataclass
class LLMFailure:
    reason: str
    error_type: Type[LLMSystemError]
