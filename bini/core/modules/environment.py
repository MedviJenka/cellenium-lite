import os
from dotenv import load_dotenv


def get_dotenv_data(key: str) -> str:
    load_dotenv()
    return os.getenv(key)
