from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class EnglishAgent(AgentInfrastructure):

    """EnglishAgent is a CrewBase class that defines a crew for refining English prompts."""

    def __init__(self, chain_of_thought: bool, to_json: bool) -> None:
        self.to_json = to_json
        self.chain_of_thought = chain_of_thought
        super().__init__(chain_of_thought=self.chain_of_thought, to_json=self.to_json)

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought)

    @task
    def grammar(self) -> Task:
        return Task(config=self.tasks_config['grammar'])

    @task
    def question_validation(self) -> Task:
        return Task(config=self.tasks_config['question_validation'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw


EnglishAgent(chain_of_thought=True, to_json=True).execute('hi he u are')
