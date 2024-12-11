from __future__ import annotations

from typing import Iterable, Optional, AsyncGenerator, override

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from .base_llm import BaseLLM
from ..async_helper import async_to_sync


class ChatGPT(BaseLLM):
    
    client: AsyncOpenAI
    
    @classmethod
    def get_model_names(cls) -> list[str]:
        return [
            'gpt-4o',
            'gpt-4o-mini',
        ]
    
    def __init__(
        self,
        model_name: Optional[str] = 'gpt-4o',
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            system_prompt=system_prompt,
            api_key=api_key,
        )
        self.client = AsyncOpenAI(api_key=api_key)
        
    @override
    async def generate_async(self, user_prompt: str) -> AsyncGenerator[str, None]:
        message: Iterable[ChatCompletionMessageParam] = []
        if self.system_prompt:
            message.append({"role": "system", "content": self.system_prompt})
        message.append({"role": "user", "content": user_prompt})
        assert self.model_name
        async for chunk in await self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            stream=True,
        ):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content