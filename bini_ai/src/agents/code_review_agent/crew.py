from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class EnglishAgent(AgentInfrastructure):
    """EnglishAgent is a CrewBase class that defines a crew for refining English prompts."""

    def __init__(self, chain_of_thought: Optional[bool] = False) -> None:
        self.chain_of_thought = chain_of_thought
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def file_reader(self) -> Agent:
        return Agent(config=self.agents_config['file_reader'], llm=self.llm, verbose=self.debug)

    @agent
    def file_modifier(self) -> Agent:
        return Agent(config=self.agents_config['file_modifier'], llm=self.llm, verbose=self.debug)

    @agent
    def file_manager(self) -> Agent:
        return Agent(config=self.agents_config['file_modifier'], llm=self.llm, verbose=self.debug)

    @task
    def file_reader(self) -> Task:
        return Task(config=self.tasks_config['file_reader'], tools=[FileReaderTool()])

    @task
    def file_modifier(self) -> Task:
        return Task(config=self.tasks_config['file_modifier'], tools=[FileWriterTool(), FileListTool()])

    @task
    def file_manager(self) -> Task:
        return Task(config=self.tasks_config['file_modifier'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw
