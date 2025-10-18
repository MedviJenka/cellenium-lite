from typing import Optional, Union, Type
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from openai import BaseModel
from bini_ai.src.tools.image_compressor import CompressAndUploadImage
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ComputerVisionAgent(AgentInfrastructure):

    def __init__(self, chain_of_thought: bool, output_schema: Optional[Type[BaseModel]] = None) -> None:
        self.chain_of_thought = chain_of_thought
        self.output_schema = output_schema
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent(self, **kwargs) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought, **kwargs)

    @task
    def determine_images(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['determine_images'], **kwargs)

    @task
    def describe_main_image(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['describe_main_image'], **kwargs)

    @task
    def describe_sample_images(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['describe_sample_images'], **kwargs)

    @task
    def conclusion(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['conclusion'], **kwargs)

    @task
    def chain_of_thought_output(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['chain_of_thought_output'], **kwargs)

    @task
    def decision(self, **kwargs) -> Task:
        return Task(config=self.tasks_config['decision'], output_pydantic=self.output_schema, **kwargs)

    @crew
    def crew(self) -> Crew:
        # Consider changing to Process.parallel if tasks are independent for runtime improvement
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)

    def execute(self, prompt: str, image_path: str, sample_image: Optional[Union[list, str]] = '') -> str:
        compressor = CompressAndUploadImage()
        image = compressor.upload_image(prompt='', image_path=image_path, sample_image=sample_image)
        return self.crew().kickoff({'prompt': prompt, 'image': image, 'sample_image': sample_image}).raw
