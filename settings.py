import os
import logfire
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from dataclasses import dataclass
from functools import cached_property


load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    SMITHERY_API_KEY: str = os.getenv('SMITHERY_API_KEY')
    LOGFIRE_TOKEN: str = os.getenv('LOGFIRE_TOKEN')


Config = Settings()


@dataclass(frozen=True)
class Logfire:

    name: str

    @cached_property
    def fire(self) -> logfire:
        return logfire.configure(service_name=self.name, token=Config.LOGFIRE_TOKEN)
