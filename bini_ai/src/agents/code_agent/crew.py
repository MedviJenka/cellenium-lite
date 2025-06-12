from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class CodeAgent(AgentInfrastructure):
    """CodeAgent is a CrewBase class that defines a crew for performing file operations and analysis."""

    def __init__(self, chain_of_thought: Optional[bool] = False, tools: list = None) -> None:
        self.chain_of_thought = chain_of_thought
        self.tools = tools
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent_1(self) -> Agent:
        return Agent(config=self.agents_config['agent_1'], llm=self.llm, verbose=self.chain_of_thought)

    @agent
    def agent_2(self) -> Agent:
        return Agent(config=self.agents_config['agent_2'], llm=self.llm, verbose=self.chain_of_thought)

    @agent
    def agent_3(self) -> Agent:
        return Agent(config=self.agents_config['agent_3'], llm=self.llm, verbose=self.chain_of_thought)

    @task
    def file_reader(self) -> Task:
        return Task(config=self.tasks_config['file_reader'], tools=self.tools)

    @task
    def file_modifier(self) -> Task:
        return Task(config=self.tasks_config['file_modifier'], tools=self.tools)

    @task
    def file_manager(self) -> Task:
        return Task(config=self.tasks_config['file_manager'], tools=self.tools)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw


if __name__ == "__main__":
    code_agent = CodeAgent(chain_of_thought=True)
    code_agent.execute("Review the code for best practices and potential improvements.")
