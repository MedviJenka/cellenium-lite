import os
from dotenv import load_dotenv


def get_env(value: str) -> any:
    load_dotenv()
    return os.getenv(value)
