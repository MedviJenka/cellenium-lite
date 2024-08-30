from typing import Optional, Never
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bini.infrastructure.environment import get_dotenv_data
from bini.engine.engine import Bini


class AbstractUtils(ABC):

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> Never:
        ...


@dataclass
class CustomBiniUtils(Bini, AbstractUtils):

    endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')
    model: str = get_dotenv_data('MODEL')
    api_key: str = get_dotenv_data('OPENAI_API_KEY')
    version: str = get_dotenv_data('OPENAI_API_VERSION')

    def execute(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str:
        ...
