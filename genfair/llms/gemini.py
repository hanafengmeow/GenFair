from __future__ import annotations

from typing import Optional, Generator, AsyncGenerator, override

import google.generativeai as genai

from .base_llm import BaseLLM


class Gemini(BaseLLM):
    
    model: genai.GenerativeModel
    
    @classmethod
    def get_model_names(cls) -> list[str]:
        return [
            'gemini-1.5-pro',
            'gemini-1.5-flash',
        ]
    
    def __init__(
        self,
        model_name: Optional[str] = 'gemini-1.5-pro',
        system_prompt: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            system_prompt=system_prompt,
            api_key=api_key,
        )
        genai.configure(api_key=api_key)
        assert self.model_name
        self.model = genai.GenerativeModel(self.model_name, system_instruction=system_prompt)
        
    def generate(self, user_prompt: str) -> Generator[str, None]:
        response = self.model.generate_content(user_prompt, stream=True)
        for chunk in response:
            yield chunk.text
            
    @override
    async def generate_async(self, user_prompt: str) -> AsyncGenerator[str, None]:
        raise NotImplementedError
        yield