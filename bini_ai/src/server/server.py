from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()


mcp = FastMCP(name='test', host='0.0.0.0', port='8090')


@mcp.tool()
def add(a: int, b: int) -> int: return a + b


if __name__ == "__main__":
    transport = 'sse'
    if transport == 'stdio':
        print("Starting MCP server with stdio transport...")
        mcp.run(transport='stdio')
    elif transport:
        print("Starting MCP server with SSE transport...")
        mcp.run(transport='sse')
