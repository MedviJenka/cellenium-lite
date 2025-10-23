from typing import List, Optional
from crewai.tools import BaseTool
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from core.bini.backend.ai.agents.reflection_agent.schemas import ReflectionOutputSchema
from core.bini.backend.utils.infrastructure import AgentInfrastructure
from settings import Logfire


log = Logfire(name='reflection-agent')


@CrewBase
class ReflectionAgent(AgentInfrastructure):

    """Reflection agent will reflect on what user had asked and what the actual answer is"""

    def __init__(self, chain_of_thought: bool) -> None:
        self.chain_of_thought = chain_of_thought
        self.mcp_tools: Optional[List[BaseTool]] = []
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent(self, **kwargs: any) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought, **kwargs)

    @task
    def task(self, **kwargs: any) -> Task:
        response = Task(config=self.tasks_config['task'], output_pydantic=ReflectionOutputSchema, **kwargs)
        log.fire.info(f'{response}')
        return response

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=self.chain_of_thought)

    def execute(self, original_question: str, final_answer: str) -> str:
        """Execute the browser agent crew with the given URL and prompt."""
        return self.crew().kickoff(inputs={'original_question': original_question, 'final_answer': final_answer}).raw
