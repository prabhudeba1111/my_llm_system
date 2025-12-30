from abc import ABC, abstractmethod
from typing import Union

from src.llm.models import LLMFailure, LLMRequest, LLMResponse


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> Union[LLMResponse, LLMFailure]:
        pass

class AsyncBaseLLM(ABC):
    @abstractmethod
    async def generate(self, request: LLMRequest) -> Union[LLMResponse, LLMFailure]:
        pass