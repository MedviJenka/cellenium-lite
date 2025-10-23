from pydantic import BaseModel
from typing import Optional, Type
from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from core.bini.backend.utils.infrastructure import AgentInfrastructure


@CrewBase
class ChatAgent(AgentInfrastructure):

    """
    TODO: add file reader tool in the future
    ---
    TextAgent is a CrewBase class that defines a crew for refining text prompts.
    takes an optional file_path to read content from a file.
    execute function takes a prompt and optional content and sample_content to process.

    """

    def __init__(self,
                 file_path: Optional[str] = None,
                 chain_of_thought: Optional[bool] = False,
                 schema_output: Optional[Type[BaseModel]] = None
                 ) -> None:

        self.schema_output = schema_output
        self.file_path = file_path
        self.chain_of_thought = chain_of_thought
        self.schema_output = schema_output
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent(self, **kwargs) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought, **kwargs)

    @task
    def task1(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['task1'], **kwargs)

    @task
    def task2(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['task2'], output_pydantic=self.schema_output, **kwargs)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks)

    def execute(self, prompt: str) -> str:

        # file_content = ''
        # path = Path(self.file_path)
        #
        # if path.exists() and path.is_file():
        #     file_content = path.read_text(encoding="utf-8")

        return self.crew().kickoff(inputs={"prompt": prompt}).raw
