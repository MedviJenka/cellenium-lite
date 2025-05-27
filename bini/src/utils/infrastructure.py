from typing import Optional, Union
from crewai import Agent, Task
from abc import ABC, abstractmethod
from qasharedinfra.infra.common.services.bini_ai.src.utils.azure_llm import AzureLLMConfig


class AgentInfrastructure(ABC, AzureLLMConfig):

    def __init__(self, debug: Optional[bool] = True) -> None:
        super().__init__()
        self.debug = debug
        self.agents: list[Agent] = []
        self.tasks: list[Task] = []
        self.agents_config: Union[dict, str] = "config/agents.yaml"
        self.tasks_config: Union[dict, str] = "config/tasks.yaml"

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> None: ...
