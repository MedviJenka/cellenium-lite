import os
from functools import cached_property
from crewai import LLM
from crewai.telemetry import Telemetry
from langchain_openai import AzureChatOpenAI
from backend.settings import Config


class TelemetryPatch:
    def __init__(self) -> None:
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, self.__nop)

    def __nop(*args: any, **kwargs: any) -> None:
        pass


class AzureLLMConfig(TelemetryPatch):

    def __init__(self, temperature: int = 0) -> None:

        super().__init__()
        self.temperature = temperature
        env_list = [Config.AZURE_API_KEY, Config.AZURE_API_BASE, Config.AZURE_API_VERSION, Config.AZURE_DEPLOYMENT_NAME]
        if not all(env_list):
            raise ValueError("Missing Azure OpenAI environment variables!")

        # Disable CrewAI telemetry only
        os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'
        # Disable all OpenTelemetry (including CrewAI)
        os.environ['OTEL_SDK_DISABLED'] = 'true'

    @cached_property
    def llm(self) -> LLM:
        return LLM(
            model=f'azure/{Config.AZURE_DEPLOYMENT_NAME}',
            api_version=Config.AZURE_API_VERSION,
            temperature=self.temperature
        )

    @cached_property
    def langchain_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            api_key=Config.AZURE_API_KEY,
            azure_endpoint=Config.AZURE_API_BASE,
            azure_deployment=Config.AZURE_DEPLOYMENT_NAME,
            api_version=Config.AZURE_API_VERSION
        )
