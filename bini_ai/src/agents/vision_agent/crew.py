import uuid
from typing import Optional, Union
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from bini_ai.src.agents.vision_agent.schemas import DecisionOutput
from bini_ai.src.tools.image_compressor import CompressAndUploadImage
from bini_ai.src.utils.infrastructure import AgentInfrastructure


@CrewBase
class ComputerVisionAgent(AgentInfrastructure):

    def __init__(self, chain_of_thought: bool, to_json: bool) -> None:
        self.chain_of_thought = chain_of_thought
        self.to_json = to_json
        super().__init__(chain_of_thought=self.chain_of_thought, to_json=self.to_json)

    @agent
    def agent(self) -> Agent:
        return Agent(config=self.agents_config['agent'], llm=self.llm, verbose=self.chain_of_thought)

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
    def conclusion(self) -> Task:
        return Task(config=self.tasks_config['conclusion'])

    @task
    def chain_of_thought_output(self) -> Task:
        return Task(config=self.tasks_config['chain_of_thought_output'])

    @task
    def decision(self) -> Task:
        match self.to_json:
            case True:
                return Task(config=self.tasks_config['decision'],
                            output_json=DecisionOutput,
                            output_file=fr'output/bini-{uuid.uuid4()}.json')
            case _:
                return Task(config=self.tasks_config['decision'])

    @crew
    def crew(self) -> Crew:
        # Consider changing to Process.parallel if tasks are independent for runtime improvement
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)

    def execute(self, prompt: str, image_path: str, sample_image: Optional[Union[list, str]] = '') -> str:
        compressor = CompressAndUploadImage()
        image = compressor.upload_image(prompt='', image_path=image_path, sample_image=sample_image)
        return self.crew().kickoff({'prompt': prompt, 'image': image, 'sample_image': sample_image}).raw
