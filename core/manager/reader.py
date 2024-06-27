import json
from typing import Optional
from core.manager.config import get_env


def read_json(env_key: str, json_key: Optional[str] = None) -> str:
    path = get_env(env_key)
    with open(path, 'r') as file:
        data = json.load(file)
        if json_key:
            return data[json_key]
        return data
