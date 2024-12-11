import inspect
from abc import ABCMeta
from typing import Protocol, Optional, Generator, AsyncGenerator, cast


class LLMProtocol(Protocol):
    
    model_name: Optional[str]
    system_prompt: Optional[str]
    
    @classmethod
    def get_model_names(cls) -> list[str]: ...
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None: ...
        
    def generate(self, user_prompt: str) -> Generator[str, None, None]: ...
    
    async def generate_async(self, user_prompt: str) -> AsyncGenerator[str, None]: ...
    

class LLMMeta(ABCMeta):
    
    registry: dict[str, type[LLMProtocol]] = {}
    
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if not inspect.isabstract(cls):
            type(cls).registry[cls.__name__] = cast(type[LLMProtocol], cls)
            