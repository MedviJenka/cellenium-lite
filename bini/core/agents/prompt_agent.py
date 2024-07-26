from dataclasses import dataclass
from crewai import Agent, Task, Crew
from bini.core.agents.agents import CustomAgent
from bini.core.modules.executor import Executor
from bini.engine.azure_config import EnvironmentConfig


@dataclass
class SetAgent(Executor):

    config: EnvironmentConfig

    def __post_init__(self) -> None:
        self.custom_agent = CustomAgent(config=self.config)
        self.agent = self.custom_agent.prompt_expert_agent

    @property
    def set_task(self) -> Crew:
        task1 = Task(
            expected_output="professional prompt engineer: {input}",
            description="rephrase prompt in more professional text {input}",
            agent=self.agent,
        )

        agent2 = Agent(
            role="prompt expert",
            goal="rephrase {input}",
            backstory="agent backstory",
            verbose=True,
        )

        crew = Crew(agents=[self.agent, agent2], tasks=[task1])
        return crew

    def execute(self, prompt: str) -> str:
        crew = self.set_task.kickoff(inputs={"input": prompt})
        return crew.split('Final Answer')[0]