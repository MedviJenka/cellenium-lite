from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from bini.core.modules.environment import get_dotenv_data


@dataclass
class EnvironmentConfig:

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
            api_key=get_dotenv_data(self.api_key)
        )
