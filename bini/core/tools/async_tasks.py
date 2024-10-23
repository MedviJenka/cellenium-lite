from abc import ABC, abstractmethod


class BaseAgentFactory(ABC):

    def __init__(self, role: str, goal: str, backstory: str, allow_delegation: bool, verbose: bool, max_iter: int, tools: list, llm: object) -> None:
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.allow_delegation = allow_delegation
        self.verbose = verbose
        self.max_iter = max_iter
        self.tools = tools
        self.llm = llm

    @abstractmethod
    def setup_agent(self) -> None:
        pass
