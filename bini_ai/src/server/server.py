import os
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from bini_ai.src.agents.code_agent.crew import CodeAgent


server_params = StdioServerParameters(command="npx",
                                      args=["-y", "@wonderwhy-er/desktop-commander@latest"],
                                      cwd=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\tests',
                                      env={**os.environ})


def main():
    # Use context manager for proper connection lifecycle
    with MCPServerAdapter(server_params) as desktop_tools:
        print(f"Available Desktop Commander tools: {[tool.name for tool in desktop_tools]}")
        code_agent = CodeAgent(chain_of_thought=True, tools=desktop_tools)
        code_agent.execute(prompt=r'write 3 tests based on this dir: C:\Users\evgenyp\PycharmProjects\cellenium-lite\tests')


if __name__ == "__main__":
    main()
