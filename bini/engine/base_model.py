from abc import ABC


class BiniBaseModel(ABC):

    """
    Abstract class which will force the modules to initialize the parameters bellow
    """

    def __init__(self, model: str, version: str, endpoint: str) -> None:
        self.model = model
        self.version = version
        self.endpoint = f"{endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"
