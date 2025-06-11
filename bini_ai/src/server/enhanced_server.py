import os
import mcp
import json
import base64
import asyncio
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from typing import List, Any


load_dotenv()
config = {}


class DesktopCommanderClient:
    """Enhanced MCP client for Desktop Commander integration."""
    
    def __init__(self):
        self.write_stream = None
        self.read_stream = None
        self.client = None
        self.config_b64 = base64.b64encode(json.dumps(config).encode())
        self.smithery_api_key = os.getenv('SMITHERY_API_KEY')
        self.url = f"https://server.smithery.ai/@wonderwhy-er/desktop-commander/mcp?config={self.config_b64}&api_key={self.smithery_api_key}"
        self.session = None
        
    async def connect(self):
        """Establish connection to MCP server."""
        self.client = streamablehttp_client(self.url)
        self.read_stream, self.write_stream, _ = await self.client.__aenter__()
        self.session = mcp.ClientSession(self.read_stream, self.write_stream)
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def disconnect(self):
        """Clean up connections."""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if hasattr(self, 'client'):
            await self.client.__aexit__(None, None, None)
    
    async def list_available_tools(self) -> List[str]:
        """Get list of available tools from the server."""
        tools_result = await self.session.list_tools()
        return [tool.name for tool in tools_result.tools]
    
    async def take_screenshot(self, path: str = None) -> str | None | Any:
        """Take a screenshot using the desktop commander."""
        try:
            # Use get_screenshot tool if available
            result = await self.session.call_tool(
                "get_screenshot",
                arguments={"path": path} if path else {}
            )
            return result.content[0].text if result.content else "Screenshot taken successfully"
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    async def execute_command(self, command: str, timeout_ms: int = 30000) -> str | None | Any:
        """Execute a system command."""
        try:
            result = await self.session.call_tool(
                "execute_command",
                arguments={
                    "command": command,
                    "timeout_ms": timeout_ms
                }
            )
            return result.content[0].text if result.content else "Command executed"
        except Exception as e:
            print(f"Error executing command: {e}")
            return None
    
    async def read_file(self, path: str, offset: int = 0, length: int = 1000) -> str | None | Any:
        """Read contents of a file."""
        try:
            result = await self.session.call_tool(
                "read_file",
                arguments={
                    "path": path,
                    "offset": offset,
                    "length": length
                }
            )
            return result.content[0].text if result.content else ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    async def write_file(self, path: str, content: str, mode: str = "rewrite") -> bool:
        """Write content to a file."""
        try:
            await self.session.call_tool(
                "write_file",
                arguments={
                    "path": path,
                    "content": content,
                    "mode": mode
                }
            )
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    async def list_directory(self, path: str) -> List[str]:
        """List contents of a directory."""
        try:
            result = await self.session.call_tool(
                "list_directory",
                arguments={"path": path}
            )
            return result.content[0].text.split('\n') if result.content else []
        except Exception as e:
            print(f"Error listing directory: {e}")
            return []


async def main() -> None:
    """Main function demonstrating Desktop Commander usage."""
    client = DesktopCommanderClient()
    
    try:
        # Connect to the server
        await client.connect()
        print("Connected to Desktop Commander")
        
        # List available tools
        tools = await client.list_available_tools()
        print(f"Available tools: {', '.join(tools)}")
        
        # Example usage - take a screenshot
        screenshot_result = await client.take_screenshot("test_screenshot.png")
        print(f"Screenshot result: {screenshot_result}")
        
        # Example usage - list current directory
        dir_contents = await client.list_directory(".")
        print(f"Current directory contents: {dir_contents[:5]}...")  # Show first 5 items
        
        # Example usage - read a file
        file_content = await client.read_file("README.md", length=100)
        print(f"README.md preview: {file_content[:100]}...")
        
    except Exception as e:
        print(f"Error in main: {e}")
    
    finally:
        await client.disconnect()
        print("Disconnected from Desktop Commander")


if __name__ == "__main__":
    asyncio.run(main())
