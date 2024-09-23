from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI

from bini.core.modules.environment import get_dotenv_data


@dataclass
class AzureOpenAIConfig:

    """
    A configuration class to manage environment settings for Azure OpenAI deployment.

    This class is designed to capture the necessary configuration settings
    for interacting with Azure's OpenAI services, including the model name,
    API key, API version, and Azure endpoint. It retrieves these values
    from environment variables using the `get_dotenv_data` function, which
    allows for secure configuration management, keeping sensitive data
    such as the API key out of the source code.

    Attributes:
    ----------
    model : str
        The name of the OpenAI model to be used for the deployment.
        Retrieved from the 'MODEL' environment variable.

    api_key : str
        The API key used to authenticate requests to Azure OpenAI services.
        Retrieved from the 'OPENAI_API_KEY' environment variable.

    openai_api_version : str
        The version of the OpenAI API being used in the deployment.
        Retrieved from the 'OPENAI_API_VERSION' environment variable.

    azure_endpoint : str
        The endpoint URL for Azure's OpenAI services.
        Retrieved from the 'AZURE_OPENAI_ENDPOINT' environment variable.

    """

    model: str = get_dotenv_data('MODEL')
    api_key: str = get_dotenv_data('OPENAI_API_KEY')
    openai_api_version: str = get_dotenv_data('OPENAI_API_VERSION')
    azure_endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')

    @property
    def set_azure_llm(self) -> AzureChatOpenAI:

        """Initiates openai with azure"""

        return AzureChatOpenAI(
            deployment_name=self.model,
            openai_api_version=self.openai_api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key
        )
