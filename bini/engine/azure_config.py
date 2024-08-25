from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI, OpenAI
from bini.infrastructure.environment import get_dotenv_data


@dataclass
class AzureOpenAIEnvironmentConfig:

    deployment_name: str
    openai_api_version: str
    azure_endpoint: str
    api_key: str

    @property
    def set_azure_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            deployment_name=get_dotenv_data(self.deployment_name),
            openai_api_version=get_dotenv_data(self.openai_api_version),
            azure_endpoint=get_dotenv_data(self.azure_endpoint),
            api_key=get_dotenv_data(self.api_key),
            temperature=0
        )


@dataclass
class OpenaiEnvironmentConfig:

    api_key: str

    @property
    def set_openai_llm(self) -> OpenAI:
        return OpenAI(openai_api_key=get_dotenv_data(self.api_key))


config = AzureOpenAIEnvironmentConfig(deployment_name='MODEL',
                                      openai_api_version='OPENAI_API_VERSION',
                                      azure_endpoint='AZURE_OPENAI_ENDPOINT',
                                      api_key='OPENAI_API_KEY')
