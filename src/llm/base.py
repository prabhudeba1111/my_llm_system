from abc import ABC, abstractmethod

from src.llm.models import LLMFailure, LLMRequest, LLMResponse


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse | LLMFailure:
        pass
