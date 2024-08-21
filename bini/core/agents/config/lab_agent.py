from crewai import Agent, Task, Crew
from dataclasses import dataclass
from bini.engine.azure_config import EnvironmentConfig
from bini.engine.engine import config
from bini.infrastructure.abstract_paths import AGENTS_CONFIG, TASKS_CONFIG
from bini.infrastructure.executor import Executor
from bini.infrastructure.modules import read_yaml


@dataclass
class AgentLab(Executor):

    config: EnvironmentConfig

    @property
    def custom_agent(self) -> Agent:
        return Agent(**read_yaml(AGENTS_CONFIG)['agent'], llm=self.config.set_azure_llm)

    def tasks(self, prompt: str) -> Task:
        # Load task configuration from YAML
        task_config = read_yaml(TASKS_CONFIG)['prompt_validator']

        # Modify the description to include the provided prompt dynamically
        task_config['description'] = f"{task_config['description']} Prompt to validate: {prompt}"

        # Return the task with the modified description and assign the agent
        return Task(**task_config, agent=self.custom_agent)

    def set_crew(self, prompt: str) -> Crew:
        return Crew(
            agents=[self.custom_agent],  # can include more than one agent
            tasks=[self.tasks(prompt=prompt)],
            verbose=2
        )

    def execute(self, prompt: str) -> str:
        return self.set_crew(prompt=prompt).kickoff()


agents = AgentLab(config=config)

print(agents.execute('hello'))
