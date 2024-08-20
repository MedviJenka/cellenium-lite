from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import AzureChatOpenAI
from bini.infrastructure.environment import get_dotenv_data


@CrewBase
class LogAnalyst:

    """researcher crew"""
    tasks_config: str = 'config/tasks.yaml'
    agents_config: str = 'config/agents.yaml'

    def __init__(self) -> None:

        self.openai = AzureChatOpenAI(
            deployment_name=get_dotenv_data('MODEL'),
            openai_api_version=get_dotenv_data('OPENAI_API_VERSION'),
            azure_endpoint=get_dotenv_data('AZURE_OPENAI_ENDPOINT'),
            api_key=get_dotenv_data('OPENAI_API_KEY')
        )

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['log_researcher'],
            llm=self.openai,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['log_researcher'],
            agent=self.research_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # automatically created by decorators
            tasks=self.tasks,  # automatically created by decorators
            process=Process.sequential,
        )


def get_log(file: str) -> any:
    with open(file, 'r') as f:
        return f.read()


def run() -> None:
    inputs = {
        'log': get_log(r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\bini\core\agents\config\dummy.log')
    }
    LogAnalyst().crew().kickoff(inputs=inputs)


if __name__ == '__main__':
    run()
