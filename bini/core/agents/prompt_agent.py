from dataclasses import dataclass
from crewai import Agent, Task, Crew
from bini.core.agents.agents import CustomAgent
from bini.engine.azure_config import EnvironmentConfig


@dataclass
class SetAgent:

    config: EnvironmentConfig

    def __post_init__(self) -> None:
        self.custom_agent = CustomAgent(config=self.config)
        self.agent = self.custom_agent.prompt_expert_agent

    @property
    def set_task(self) -> Crew:
        task = Task(
            expected_output="professional prompt engineer: {input}",
            description="rephrase prompt in more professional text {input}",
            agent=self.agent,
        )

        agent = Agent(
            role="prompt expert",
            goal="rephrase {input}",
            backstory="agent backstory",
            verbose=True,
        )

        crew = Crew(agents=[self.agent, agent], tasks=[task])
        return crew

    def enhance_given_prompt(self, prompt: str) -> str:
        crew = self.set_task.kickoff(inputs={"input": prompt})
        return crew.split('Final Answer')[0]
