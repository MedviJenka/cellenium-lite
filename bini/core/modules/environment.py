import os
from dotenv import load_dotenv


def get_secured_data(key: str) -> str:
    load_dotenv()
    return os.getenv(key)
