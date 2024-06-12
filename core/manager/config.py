import os
from dotenv import load_dotenv


def get_env(key: str) -> str:
    load_dotenv()
    return os.getenv(key)


def windows_to_linux_path_convert(key: str) -> str:
    path = get_env(key)
    path = path.replace('c:/', '/c/')
    return path
