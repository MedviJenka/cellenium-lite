from functools import cached_property
from langchain_openai import ChatOpenAI
from settings import Config


class LLMConfig:

    temperature: float = 0.0

    @cached_property
    def llm(self) -> ChatOpenAI:
        return ChatOpenAI(model='gpt-4o', api_key=Config.OPENAI_API_KEY, temperature=self.temperature)
