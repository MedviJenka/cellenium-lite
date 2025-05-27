import os
from dotenv import load_dotenv
from functools import cached_property
from crewai import LLM
from langchain_openai import AzureChatOpenAI
from crewai.telemetry import Telemetry


load_dotenv()


class TelemetryPatch:
    def __init__(self) -> None:
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, self.__nop)

    def __nop(*args: any, **kwargs: any) -> None:
        pass


class AzureLLMConfig(TelemetryPatch):

    def __init__(self) -> None:
        super().__init__()

        # Inject environment variables for litellm compatibility
        os.environ["AZURE_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        os.environ["AZURE_DEPLOYMENT_NAME"] = os.getenv("MODEL", "")
        os.environ["AZURE_API_VERSION"] = os.getenv("OPENAI_API_VERSION", "")

        # Store values as instance attributes
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.version = os.getenv("OPENAI_API_VERSION")
        self.model = os.getenv("MODEL")
        self.temperature = 0

        if not all([self.api_key, self.endpoint, self.version, self.model]):
            raise ValueError("Missing Azure OpenAI environment variables!")

    @cached_property
    def llm(self) -> LLM:
        return LLM(
            model=f'azure/{self.model}',
            api_version=self.version,
            temperature=self.temperature
        )

    @cached_property
    def langchain_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            azure_deployment=self.model,
            api_version=self.version,
            # model_kwargs={"azure_api_key": self.api_key}
        )
