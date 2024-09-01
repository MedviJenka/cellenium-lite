from dataclasses import dataclass
from crewai import Agent, Crew, Task
from crewai.telemetry import Telemetry
from requests.exceptions import ReadTimeout, ConnectionError
from bini.core.agents.agents import CustomAgent
from bini.engine.azure_config import AzureOpenAIConfig
from bini.infrastructure.prompts import Prompts


@dataclass
class SetAgent:

    """
    Sets up and manages an agent using environment configuration.

    :param: config ............... takes values from .env azure api setup

    """

    config = AzureOpenAIConfig()

    def __post_init__(self) -> None:
        self.__initialize_agents()
        self.__disable_telemetry()

    def __initialize_agents(self) -> None:
        """Initializes custom and predefined agents."""
        self.custom_agent = CustomAgent(config=self.config)
        self.agent = self.custom_agent.prompt_expert_agent
        self.validator = self.custom_agent.final_result_agent

    @staticmethod
    def __disable_telemetry() -> None:
        """Disables telemetry methods as a temporary fix."""
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, lambda *args, **kwargs: None)

    @property
    def set_task(self) -> Crew:
        """
        Creates a task crew for rephrasing prompts.
        """
        task = Task(
            expected_output="professional prompt engineer: {input}",
            description="Rephrase prompt in a more professional text {input}",
            agent=self.agent,
        )

        supporting_agent = Agent(
            role="prompt expert",
            goal="Rephrase {input}",
            backstory="Agent backstory",
            verbose=True,
        )

        return Crew(ready=False, agents=[self.agent, supporting_agent], tasks=[task])

    @property
    def set_result(self) -> Crew:
        """
        Creates a task crew for validating results.
        """
        task = Task(
            expected_output="{input}",
            description="{input}",
            agent=self.validator,
        )

        supporting_agent = Agent(
            role=Prompts.validation_agent,
            goal="validate {input} in a professional manner",
            backstory="You're a professional prompt validation engineer",
            verbose=True,
        )

        return Crew(ready=False, agents=[self.validator, supporting_agent], tasks=[task])

    @staticmethod
    def _process_with_crew(crew: Crew, input_data: str) -> str:
        """
        Processes the input data with the given crew and returns the result.
        """
        try:
            crew.kickoff(inputs={"input": input_data})
            print(crew)
            return str(crew).split('Final Answer')[0]
        except (ReadTimeout, ConnectionError):
            return "Error: Unable to process the input."

    def enhance_given_prompt(self, prompt: str) -> str:
        """
        Enhances a given prompt using the agent.
        """
        crew = self.set_task
        return self._process_with_crew(crew, prompt)

    def enhance_given_result(self, result: str) -> str:
        """
        Enhances a given result using the agent.
        """
        crew = self.set_result
        return self._process_with_crew(crew, result)
