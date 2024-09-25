from abc import ABC


class BiniFactory(ABC):

    def __init__(self, *, model: str, version: str, endpoint: str) -> None:
        self.model = model
        self.version = version
        self.endpoint = f"{endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"
