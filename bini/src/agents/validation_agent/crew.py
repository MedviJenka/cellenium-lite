from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from qasharedinfra.infra.common.services.bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ValidationAgent(AgentInfrastructure):

    """ValidationAgent is a CrewBase class that defines a crew for validating image data."""

    def __init__(self, debug: Optional[bool] = False) -> None:
        super().__init__()
        self.debug = debug

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.debug)

    @task
    def decision(self) -> Task:
        return Task(config=self.tasks_config['decision'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, output: str) -> str:
        return self.crew().kickoff({'output': output}).raw
