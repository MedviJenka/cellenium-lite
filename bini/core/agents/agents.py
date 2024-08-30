from textwrap import dedent
from dataclasses import dataclass
from crewai import Agent, Crew
from bini.engine.azure_config import AzureOpenAIEnvironmentConfig


@dataclass
class CustomAgent:

    """
    Notes for agents:
        1. Agents should be result driven and have a clear goal in mind
        2. Role is their job title
        3. Goal should be actionable
        4. Backstory should be their resume

    """

    config: object

    def prompt_expert_agent(self) -> Agent:
        return Agent(
            role='Prompt Expert',
            goal=dedent(f"""Rephrasing user prompt in more professional way"""),
            backstory=dedent(f"""Rephrasing user prompt in more professional way"""),
            allow_delegation=False,
            llm=self.config,
            verbose=True)


class CallCrew(CustomAgent):

    config: AzureOpenAIEnvironmentConfig

    def assemble_crew(self) -> str:
        return Crew(agents=[self.prompt_expert_agent]).kickoff()
