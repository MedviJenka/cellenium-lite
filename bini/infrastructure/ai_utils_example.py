from bini.core.modules.environment import get_dotenv_data
from bini.engine.engine import Bini


class BiniUtils(Bini):

    """
    A utility class for interacting with the OpenAI API using Azure's infrastructure.

    This class extends the `Bini` class and initializes the necessary attributes such as
    the model, API key, API version, and endpoint by retrieving these values from environment
    variables.

    Attributes:
        model (str): The model to be used with the OpenAI API, retrieved from environment variables.
        api_key (str): The API key for authenticating requests to the OpenAI API, retrieved from environment variables.
        version (str): The version of the OpenAI API to be used, retrieved from environment variables.
        endpoint (str): The Azure endpoint for the OpenAI API, retrieved from environment variables.

    Methods:
        __init__: Initializes the IRBiniUtils class by setting up the model, API key, version, and endpoint.

    """

    def __init__(self) -> None:
        self.model: str = get_dotenv_data('MODEL')
        self.api_key: str = get_dotenv_data('OPENAI_API_KEY')
        self.version: str = get_dotenv_data('OPENAI_API_VERSION')
        self.endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')
        super().__init__(endpoint=self.endpoint, model=self.model, version=self.version)

    def __str__(self) -> None:
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

    def functions(self) -> any:
        """add your own functions below"""
        ...
