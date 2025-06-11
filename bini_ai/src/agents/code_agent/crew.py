from typing import Optional
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from bini_ai.src.tools.file_tool import FileReaderTool
from crewai_tools import CodeDocsSearchTool
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class CodeAgent(AgentInfrastructure):
    """CodeAgent is a CrewBase class that defines a crew for performing file operations and analysis."""

    def __init__(self, chain_of_thought: Optional[bool] = False) -> None:
        self.chain_of_thought = chain_of_thought
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def file_reader_agent(self) -> Agent:
        return Agent(config=self.agents_config['file_reader'], llm=self.llm, verbose=self.chain_of_thought)

    # @agent
    # def file_modifier_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['file_modifier'], llm=self.llm, verbose=self.chain_of_thought)
    #
    # @agent
    # def file_manager_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['file_manager'], llm=self.llm, verbose=self.chain_of_thought)

    @task
    def file_reader_task(self) -> Task:
        return Task(config=self.tasks_config['file_reader'])
    #
    # @task
    # def file_modifier_task(self) -> Task:
    #     return Task(config=self.tasks_config['file_modifier'])
    #
    # @task
    # def file_manager_task(self) -> Task:
    #     return Task(config=self.tasks_config['file_manager'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'prompt': prompt}).raw


if __name__ == "__main__":
    code_agent = CodeAgent(chain_of_thought=True)
    result = code_agent.execute("Review the code for best practices and potential improvements.")
    print(result)
