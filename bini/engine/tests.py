from bini.engine.agents import EnvironmentConfig, AgentSetup, ToolsSetup, TaskSetup, CrewSetup


def test_agent_1() -> None:

    # Configure environment
    azure_llm = EnvironmentConfig(deployment_name='MODEL',
                                  openai_api_version='OPENAI_API_VERSION',
                                  azure_endpoint='AZURE_OPENAI_ENDPOINT',
                                  api_key='OPENAI_API_KEY')

    # Setup agent
    validation_agent = AgentSetup.get_agent(azure_llm)

    # Setup tools
    tools = ToolsSetup.get_tools()

    # Define tasks
    tasks = TaskSetup.get_tasks(validation_agent)

    # Assemble and kickoff the crew
    crew = CrewSetup.assemble_crew([validation_agent], tasks, tools=[tools])
    crew.kickoff()
