from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from bini.core.modules.environment import get_secured_data


@dataclass
class EnvironmentConfig:

    deployment_name: str
    openai_api_version: str
    azure_endpoint: str
    api_key: str

    @property
    def azure_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            deployment_name=get_secured_data(self.deployment_name),
            openai_api_version=get_secured_data(self.openai_api_version),
            azure_endpoint=get_secured_data(self.azure_endpoint),
            api_key=get_secured_data(self.api_key)
        )
