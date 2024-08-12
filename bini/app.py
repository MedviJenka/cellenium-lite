import requests
from cffi import api

from functions import get_dotenv_data
from prompt import SYSTEM_PROMPT, PYTHON
from langchain_openai import AzureChatOpenAI


class AzureConfig:

    @property
    def azure_setup(self) -> AzureChatOpenAI:

        return AzureChatOpenAI(api_key=get_dotenv_data("OPENAI_API_KEY"),
                               azure_endpoint=get_dotenv_data("AZURE_OPENAI_ENDPOINT"),
                               deployment_name=get_dotenv_data("DEPLOYMENT_NAME"),
                               openai_api_version=get_dotenv_data('OPENAI_API_VERSION'))


config = AzureConfig()
config.azure_setup

# ENDPOINT = f"{config.azure_endpoint}/openai/deployments/{config.deployment_name}/chat/completions?api-version={config.model_version}"
#
#
