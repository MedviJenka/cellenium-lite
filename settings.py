import os
import logfire
from dotenv import load_dotenv
from dataclasses import dataclass
from functools import cached_property
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY:        str = os.getenv('OPENAI_API_KEY')
    SMITHERY_API_KEY:      str = os.getenv('SMITHERY_API_KEY')
    LOGFIRE_TOKEN:         str = os.getenv('LOGFIRE_TOKEN')
    GOOGLE_SHEET_ID:       str = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_CREDENTIALS:    str = r"C:\Users\medvi\Downloads\credentials_1.json"  # C:\Users\evgenyp\Downloads\credentials_1.json
    GOOGLE_SCOPES:         list[str] = ['https://www.googleapis.com/auth/spreadsheets']
    AZURE_API_KEY:         str = os.getenv('AZURE_API_KEY')
    AZURE_API_BASE:        str = os.getenv('AZURE_API_BASE')
    AZURE_API_VERSION:     str = os.getenv('AZURE_API_VERSION')
    AZURE_DEPLOYMENT_NAME: str = os.getenv('AZURE_DEPLOYMENT_NAME')
    ENV:                   str = os.getenv('ENV')
    HOST:                  str = os.getenv('HOST')
    PORT:                  int = str(os.getenv('PORT'))


Config = Settings()


@dataclass
class Logfire:

    name: str

    @cached_property
    def fire(self) -> logfire:
        return logfire.configure(service_name=self.name, token=Config.LOGFIRE_TOKEN)
