import yaml
from crewai import Agent, Task, Crew
from langchain_openai import AzureChatOpenAI
from bini.infrastructure.environment import get_dotenv_data
from bini.infrastructure.executor import Executor


def read_yaml(file_path) -> dict:

    """
    Reads a YAML file and returns the content as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Dictionary containing YAML data.

    """

    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError:
            raise FileNotFoundError


class AgentLab(Executor):

    tasks_config: str = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\bini\core\agents\config\tasks.yaml'
    agents_config: str = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\bini\core\agents\config\agents.yaml'

    def __init__(self):
        self.config = AzureChatOpenAI(
            deployment_name=get_dotenv_data('MODEL'),
            openai_api_version=get_dotenv_data('OPENAI_API_VERSION'),
            azure_endpoint=get_dotenv_data('AZURE_OPENAI_ENDPOINT'),
            api_key=get_dotenv_data('OPENAI_API_KEY'),
            temperature=0
        )

    @property
    def custom_agent(self) -> Agent:
        return Agent(**read_yaml(self.agents_config)['agent'], llm=self.config)

    def tasks(self, prompt: str) -> Task:
        # Load task configuration from YAML
        task_config = read_yaml(self.tasks_config)['prompt_validator']

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


agents = AgentLab()

print(agents.execute('hello'))
