from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from bini.core.modules.environment import get_dotenv_data


@dataclass
class AzureOpenAIConfig:

    """
    A configuration class to manage environment settings for Azure OpenAI deployment.

    """

    model: str = get_dotenv_data('MODEL')
    api_key: str = get_dotenv_data('OPENAI_API_KEY')
    openai_api_version: str = get_dotenv_data('OPENAI_API_VERSION')
    azure_endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')

    @property
    def set_azure_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            deployment_name=self.model,
            openai_api_version=self.openai_api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key
        )


def get_azure_config() -> AzureOpenAIConfig:
    config = AzureOpenAIConfig(model='MODEL',
                               openai_api_version='OPENAI_API_VERSION',
                               azure_endpoint='AZURE_OPENAI_ENDPOINT',
                               api_key='OPENAI_API_KEY')
    return config
