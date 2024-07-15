from crewai import Agent, Task, Crew
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from bini.core.modules.executor import Executor
from bini.infrastructure.prompts import VALIDATION_AGENT
from bini.core.modules.environment import get_secured_data
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, WebsiteSearchTool


@dataclass
class EnvironmentConfig:

    deployment_name: str
    openai_api_version: str
    azure_endpoint: str
    api_key: str

    @property
    def azure_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            deployment_name=get_secured_data(self.deployment_name),
            openai_api_version=get_secured_data(self.openai_api_version),
            azure_endpoint=get_secured_data(self.azure_endpoint),
            api_key=get_secured_data(self.api_key)
        )


@dataclass
class AgentSetup:

    config: EnvironmentConfig

    def set_agent(self, role: str, goal: str, backstory: str, *tools: list[Task]) -> Agent:
        return Agent(role=role,
                     goal=goal,
                     backstory=backstory,
                     tools=[tools],
                     llm=self.config.azure_llm)


class ToolsSetup:

    """
    Documentation: https://docs.crewai.com/core-concepts/Tools/#introduction
    """

    @staticmethod
    def get_tools() -> list:
        docs_tool = DirectoryReadTool(directory='./blog-posts')
        file_tool = FileReadTool()
        search_tool = SerperDevTool()
        web_rag_tool = WebsiteSearchTool()
        return [docs_tool, file_tool, search_tool, web_rag_tool]


class TaskSetup:
    @staticmethod
    def get_tasks(agent: Agent) -> list[Task]:
        task = Task(
            description='Research the latest trends in the AI industry and provide a summary.',
            expected_output='A summary of the top 3 trending developments in the AI industry with a unique perspective on their significance.',
            agent=agent
        )
        return [task]


class CrewSetup:
    @staticmethod
    def assemble_crew(agents: list[Agent], tasks: list[Task], tools: list) -> Crew:
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=2,
            tools=tools
        )


@dataclass
class CreateAgents(Executor):

    deployment_name: str
    openai_api_version: str
    azure_endpoint: str
    api_key: str

    def __post_init__(self) -> None:
        self.config = EnvironmentConfig(
            deployment_name=self.deployment_name,
            openai_api_version=self.openai_api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key
        )

    def execute(self) -> None:
        # Setup agent
        agent = AgentSetup(self.config)
        validation_agent = agent.set_agent(role='Prompt Validation Agent',
                                           goal=VALIDATION_AGENT,
                                           backstory='A diligent and professional prompt engineer.',)

        # Setup tools
        tools = ToolsSetup.get_tools()

        # Define tasks
        tasks = TaskSetup.get_tasks(validation_agent)

        # Assemble and kickoff the crew
        crew = CrewSetup.assemble_crew(agents=[validation_agent], tasks=tasks, tools=tools)
        crew.kickoff()


if __name__ == "__main__":
    create_agents = CreateAgents(
        deployment_name='MODEL',
        openai_api_version='OPENAI_API_VERSION',
        azure_endpoint='AZURE_OPENAI_ENDPOINT',
        api_key='OPENAI_API_KEY'
    )
    create_agents.execute()
