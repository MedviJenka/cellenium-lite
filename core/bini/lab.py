import os
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode


load_dotenv()

SMITHERY_API_KEY = os.getenv('SMITHERY_API_KEY')

SMITHERY_PROFILE = os.getenv('SMITHERY_PROFILE')

base_url = "https://server.smithery.ai/@iremaltunay55/deneme1/mcp"

params = {"api_key": SMITHERY_API_KEY, "profile": SMITHERY_PROFILE}

url = f"{base_url}?{urlencode(params)}"


async def main():
    # Connect to the server using an HTTP client
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())



# from pathlib import Path
# from agents import Agent, Runner
# from agents.mcp import MCPServerStdio
#
#
# current_dir = Path(__file__).parent
# samples_dir = current_dir / "sample_files"
#
#
# async with MCPServerStdio(
#     name="Filesystem Server via npx",
#     params={
#         "command": "npx",
#         "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
#     },
# ) as server:
#     agent = Agent(
#         name="Assistant",
#         instructions="Use the files in the sample directory to answer questions.",
#         mcp_servers=[server],
#     )
#     result = await Runner.run(agent, "List the files available to you.")
#     print(result.final_output)
