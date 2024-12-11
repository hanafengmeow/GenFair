from __future__ import annotations

from typing import Optional, Generator, AsyncGenerator
from abc import abstractmethod

from .llm_interface import LLMMeta
from ..async_helper import async_to_sync


class BaseLLM(metaclass=LLMMeta):
    
    model_name: Optional[str]
    system_prompt: Optional[str]
    
    @classmethod
    @abstractmethod
    def get_model_names(cls) -> list[str]:
        raise NotImplementedError
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.model_name = model_name
        
    def generate(self, user_prompt: str) -> Generator[str, None, None]:
        yield from async_to_sync(self.generate_async(user_prompt))
    
    @abstractmethod
    async def generate_async(self, user_prompt: str) -> AsyncGenerator[str, None]:
        raise NotImplementedError
        yield