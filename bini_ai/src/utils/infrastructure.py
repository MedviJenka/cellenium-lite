from abc import ABC, abstractmethod
from typing import Optional, Union
from crewai import Agent, Task
from bini_ai.src.utils.azure_llm import LLMConfig


class AgentInfrastructure(ABC, LLMConfig):

    def __init__(self, chain_of_thought: Optional[bool] = True) -> None:
        super().__init__()
        self.chain_of_thought = chain_of_thought
        self.agents: list[Agent] = []
        self.tasks: list[Task] = []
        self.agents_config: Union[dict, str] = "config/agents.yaml"
        self.tasks_config: Union[dict, str] = "config/tasks.yaml"

    @abstractmethod
    def execute(self, *args: Optional[any], **kwargs: Optional[any]) -> None: ...
