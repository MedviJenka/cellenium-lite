from typing import Optional, Union
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from qasharedinfra.infra.common.services.bini_ai.src.tools.image_compressor import CompressAndUploadImage
from qasharedinfra.infra.common.services.bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ComputerVisionAgent(AgentInfrastructure):

    def __init__(self, debug: Optional[bool] = False) -> None:
        self.debug = debug
        super().__init__(debug=self.debug)

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.debug)

    @task
    def determine_images(self) -> Task:
        return Task(config=self.tasks_config['determine_images'])

    @task
    def describe_main_image(self) -> Task:
        return Task(config=self.tasks_config['describe_main_image'])

    @task
    def describe_sample_images(self) -> Task:
        return Task(config=self.tasks_config['describe_sample_images'])

    @task
    def chain_of_thought(self) -> Task:
        return Task(config=self.tasks_config['chain_of_thought'])

    @task
    def decision(self) -> Task:
        return Task(config=self.tasks_config['decision'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)

    def execute(self, prompt: str, image_path: str, sample_image: Optional[Union[list, str]] = '') -> str:
        compressor = CompressAndUploadImage()
        image = compressor.upload_image(prompt='', image_path=image_path, sample_image=sample_image)
        return self.crew().kickoff({'prompt': prompt, 'image': image, 'sample_image': sample_image}).raw
