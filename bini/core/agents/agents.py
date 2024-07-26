from textwrap import dedent
from dataclasses import dataclass
from crewai import Agent, Crew
from bini.engine.azure_config import EnvironmentConfig


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
    def prompt_expert_agent(self) -> Agent:
        return Agent(
            role='Prompt Expert',
            goal=dedent(f"""Rephrasing user prompt in more professional way"""),
            backstory=dedent(f"""Rephrasing user prompt in more professional way"""),
            allow_delegation=False,
            llm=self.config.set_azure_llm,
            verbose=True)


@dataclass
class CallCrew(CustomAgent):

    config: EnvironmentConfig

    def assemble_crew(self):
        return Crew(agents=[self.prompt_expert_agent]).kickoff()


agent = CallCrew(config=config)
if __name__ == '__main__':
    print(agent.assemble_crew())
