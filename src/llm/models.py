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

    def __post_init__(self):
        if not self.prompt or not self.prompt.strip():
            raise ValueError("LLMRequest.prompt must be non-empty")

@dataclass
class LLMResponse:
    text: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None

    def __post_init__(self):
        if not self.text or not self.text.strip():
            raise ValueError("LLMResponse.text must be non-empty")

        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("LLMResponse.latency_ms must be >= 0")


@dataclass
class LLMFailure:
    error_type: Type[LLMSystemError]
    user_message: str
    internal_message: Optional[str] = None

    @property
    def retryable(self) -> bool:
        return self.error_type.retryable

    @property
    def exit_code(self) -> int:
        return self.error_type.exit_code
