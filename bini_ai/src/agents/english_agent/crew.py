from typing import Optional, Type
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from openai import BaseModel
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class EnglishAgent(AgentInfrastructure):

    """EnglishAgent is a CrewBase class that defines a crew for refining English prompts."""

    def __init__(self, chain_of_thought: bool, output_schema: Optional[Type[BaseModel]] = None) -> None:
        self.chain_of_thought = chain_of_thought
        self.output_schema = output_schema
        super().__init__()

    @agent
    def agent(self, **kwargs) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought, **kwargs)

    @task
    def grammar(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['grammar'], **kwargs)

    @task
    def question_validation(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['question_validation'], output_pydantic=self.output_schema, **kwargs)

    @crew
    def crew(self, **kwargs) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, **kwargs)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw
