import os
from crewai import Agent, Crew, Task, CrewOutput
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.adapters.mcp_adapter import MCPServerAdapter
from backend.utils.infrastructure import AgentInfrastructure
from typing import List, Optional
from crewai.tools import BaseTool
from mcp import StdioServerParameters
from backend.utils.logger import Logfire


logger = Logfire(name='browser-agent')


# Alternative implementation using CrewBase decorators (if you prefer)
@CrewBase
class BrowserAgentWithDecorators(AgentInfrastructure):
    """Alternative implementation using CrewBase decorators."""

    def __init__(self, chain_of_thought: bool, to_json: bool) -> None:
        self.to_json = to_json
        self.chain_of_thought = chain_of_thought
        self.mcp_tools: Optional[List[BaseTool]] = []  # Initialize with empty list
        super().__init__(chain_of_thought=self.chain_of_thought)

    @agent
    def agent(self) -> Agent:
        # Use empty list if mcp_tools is None
        tools = self.mcp_tools if self.mcp_tools is not None else []
        return Agent(
            config=self.agents_config['agent'],
            llm=self.llm,
            verbose=self.chain_of_thought,
            tools=tools
        )

    @task
    def task(self) -> Task:
        return Task(config=self.tasks_config['task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=self.chain_of_thought)

    def execute(self, url: str, prompt: str) -> CrewOutput:
        """Execute the browser agent crew with the given URL and prompt."""
        try:
            # Create server parameters
            server_config = {
                "command": "cmd",
                "args": [
                    "/c",
                    "npx",
                    "-y",
                    "@smithery/cli@latest",
                    "run",
                    "@bytedance/mcp-server-browser",
                    "--key",
                    "5c4619fb-d8b9-4843-b6b8-c6b789df9f76",
                    "--profile",
                    "yelping-rooster-5FYBLt"
                ]
            }

            server = StdioServerParameters(**server_config, **os.environ)

            logger.info("Initializing MCP server adapter...")

            with MCPServerAdapter(server) as mcp_tools:
                logger.info(f"MCP tools available: {len(mcp_tools) if mcp_tools else 0}")

                # Update tools before crew creation
                self.mcp_tools = mcp_tools or []

                # Clear any cached crew/agent instances
                if hasattr(self, '_agents'):
                    delattr(self, '_agents')
                if hasattr(self, '_tasks'):
                    delattr(self, '_tasks')
                if hasattr(self, '_crew'):
                    delattr(self, '_crew')

                # Prepare execution parameters
                execution_params = {
                    'url': url,
                    'prompt': prompt
                }

                # Execute the crew (this will create new instances with updated tools)
                logger.info("Starting crew execution...")
                result = self.crew().kickoff(execution_params)

                logger.info("Crew execution completed successfully")
                return result

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise


# Usage examples
if __name__ == "__main__":

    # Example 1: Using the basic implementation
    logger.info("Testing BrowserAgent...")
    agent = BrowserAgentWithDecorators(chain_of_thought=True, to_json=False)
    result = agent.execute('https://www.example.com', 'What is the title of this page?')
    print("Result:", result)
