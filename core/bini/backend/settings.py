import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):

    """base settings class which will retrieve environment variables"""

    API_VERSION: str = os.getenv("API_VERSION")

    ENV: str  = os.getenv("ENV")

    HOST: str  = os.getenv("HOST")

    PORT: int  = int(os.getenv("PORT"))

    AZURE_API_KEY: str  = os.getenv("AZURE_API_KEY")

    AZURE_API_BASE: str  = os.getenv("AZURE_API_BASE")

    AZURE_API_VERSION: str  = os.getenv("AZURE_API_VERSION")

    AZURE_DEPLOYMENT_NAME: str  = os.getenv("AZURE_DEPLOYMENT_NAME")

    LOGFIRE_TOKEN: str  = os.getenv("LOGFIRE_TOKEN")

    SMITHERY_API_KEY: str  = os.getenv("SMITHERY_API_KEY")

    SMITHERY_PROFILE: str  = os.getenv("SMITHERY_PROFILE")


Config = Settings()
