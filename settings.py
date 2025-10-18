import os
import logfire
from dotenv import load_dotenv
from dataclasses import dataclass
from functools import cached_property
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    SMITHERY_API_KEY: str = os.getenv('SMITHERY_API_KEY')
    LOGFIRE_TOKEN: str = os.getenv('LOGFIRE_TOKEN')
    GOOGLE_SHEET_ID: str = os.getenv('GOOGLE_SHEET_ID')


Config = Settings()


@dataclass(frozen=True)
class Logfire:

    name: str

    @cached_property
    def fire(self) -> logfire:
        return logfire.configure(service_name=self.name, token=Config.LOGFIRE_TOKEN)
