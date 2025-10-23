from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from core.bini.backend.utils.infrastructure import AgentInfrastructure
from ..english_agent.schemas import ValidateQuestionSchema


@CrewBase
class EnglishAgent(AgentInfrastructure):

    """EnglishAgent is a CrewBase class that defines a crew for refining English prompts."""

    def __init__(self, chain_of_thought: bool) -> None:
        self.chain_of_thought = chain_of_thought
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent(self, **kwargs) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought, **kwargs)

    @task
    def grammar(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['grammar'],  **kwargs)

    @task
    def question_validation(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['question_validation'], output_pydantic=ValidateQuestionSchema, **kwargs)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=self.chain_of_thought)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw
