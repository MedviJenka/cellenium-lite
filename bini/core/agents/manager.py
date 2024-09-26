from crewai import Agent, Crew, Task
from crewai.telemetry import Telemetry
from requests.exceptions import ReadTimeout, ConnectionError
from bini.core.agents.agents import CustomAgent
from bini.engine.azure_config import AzureOpenAIConfig


class WorkaroundHandler:

    @staticmethod
    def _disable_telemetry():

        """Disables telemetry methods temporarily to avoid unwanted behavior."""

        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, lambda *args, **kwargs: None)


class AgentManager(WorkaroundHandler):

    """
    Handles the initialization and management of agents and task crews.
    doc:  https://docs.crewai.com/core-concepts/Agents/#agent-attributes

    """

    def __init__(self) -> None:
        self.config = AzureOpenAIConfig()
        self._initialize_agents()
        self._disable_telemetry()
        super().__init__()

    def _initialize_agents(self):
        """Initializes the agents using the provided configuration."""
        self.custom_agent = CustomAgent(config=self.config)
        self.prompt_agent = self.custom_agent.prompt_expert_agent
        self.validation_agent = self.custom_agent.final_result_agent

    @staticmethod
    def create_task_crew(task_description: str,
                         task_output: str,
                         agent: Agent,
                         supporting_role: str,
                         supporting_goal: str,
                         supporting_backstory: str) -> Crew:

        """
        Creates and returns a task crew with the given configuration.

        :param task_description: The description of the task.
        :param task_output: Expected output for the task.
        :param agent: The primary agent responsible for the task.
        :param supporting_role: The role of the supporting agent.
        :param supporting_goal: The goal of the supporting agent.
        :param supporting_backstory: The backstory for the supporting agent.
        :return: Configured Crew instance.

        """

        task = Task(expected_output=task_output, description=task_description, agent=agent)

        supporting_agent = Agent(
            role=supporting_role,
            goal=supporting_goal,
            backstory=supporting_backstory,
            memory=True,
            verbose=True,
        )

        return Crew(ready=False, agents=[agent, supporting_agent], tasks=[task])

    @staticmethod
    def process_with_crew(crew: Crew, input_data: str) -> str:
        """
        Processes the input data using the provided crew.

        :param crew: The Crew instance responsible for processing the input.
        :param input_data: The input data to process.
        :return: The processed result or error message if it fails.
        """
        try:
            crew.kickoff(inputs={"input": input_data})
            return str(crew).split('Final Answer')[0]
        except (ReadTimeout, ConnectionError):
            return "Error: Unable to process the input."
