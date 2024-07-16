from textwrap import dedent
from dataclasses import dataclass
from crewai import Agent, Task, Crew
from langchain.tools import tool
from crewai_tools import RagTool, FileReadTool
from bini.engine.azure_config import EnvironmentConfig
from bini.infrastructure.prompts import IMAGE_VISUALIZATION_AGENT, VALIDATION_AGENT


config = EnvironmentConfig(deployment_name='MODEL',
                           openai_api_version='OPENAI_API_VERSION',
                           azure_endpoint='AZURE_OPENAI_ENDPOINT',
                           api_key='OPENAI_API_KEY')


@dataclass
class CustomAgent:

    """
    Notes for agents:
        1. Agents should be result driven and have a clear goal in mind
        2. Role is their job title
        3. Goal should be actionable
        4. Backstory should be their resume

    """

    config: EnvironmentConfig

    @property
    def tool_kit(self) -> list:
        return [FileReadTool(), RagTool()]

    @property
    def image_expert_agent(self) -> Agent:
        return Agent(
            role='Image Visualization Expert',
            goal=dedent(IMAGE_VISUALIZATION_AGENT),
            backstory=dedent(f"""An expert in image visualization understanding"""),
            allow_delegation=False,
            llm=self.config.set_azure_llm,
            verbose=True)

    @property
    def validation_expert_agent(self) -> Agent:
        return Agent(
            role='Validation Expert',
            goal=dedent(VALIDATION_AGENT),
            backstory=dedent(f"""An expert in prompt validation"""),
            allow_delegation=False,
            llm=self.config.set_azure_llm,
            verbose=True)


@dataclass
class CallCrew(CustomAgent):

    config = EnvironmentConfig(deployment_name='MODEL',
                               openai_api_version='OPENAI_API_VERSION',
                               azure_endpoint='AZURE_OPENAI_ENDPOINT',
                               api_key='OPENAI_API_KEY')

    def assemble_crew(self):
        return Crew(
            agents=[self.image_expert_agent],

        ).kickoff()


agent = CallCrew(config=config)
if __name__ == '__main__':
    agent.assemble_crew()

