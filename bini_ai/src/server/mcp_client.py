import os
import mcp
import json
import base64
import asyncio
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    """Enhanced MCP Client for Desktop Commander integration."""
    
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv('SMITHERY_API_KEY')
        if not self.api_key:
            raise ValueError("SMITHERY_API_KEY not found in environment variables")
        
        self.config = {}
        self.config_b64 = base64.b64encode(json.dumps(self.config).encode())
        self.url = f"https://server.smithery.ai/@wonderwhy-er/desktop-commander/mcp?config={self.config_b64}&api_key={self.api_key}"
        
        self.session = None
        self.client_context = None
        self.connected = False
        
    async def connect(self) -> bool:
        """Establish connection to MCP server."""
        try:
            logger.info("Connecting to MCP server...")
            self.client_context = streamablehttp_client(self.url)
            self.read_stream, self.write_stream, _ = await self.client_context.__aenter__()
            
            self.session = mcp.ClientSession(self.read_stream, self.write_stream)
            await self.session.__aenter__()
            await self.session.initialize()
            
            self.connected = True
            logger.info("Successfully connected to MCP server")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return False
    
    async def disconnect(self):
        """Clean up connections."""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
            if self.client_context:
                await self.client_context.__aexit__(None, None, None)
            self.connected = False
            logger.info("Disconnected from MCP server")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
    
    async def list_tools(self) -> List[str]:
        """Get list of available tools."""
        if not self.connected:
            raise RuntimeError("Not connected to MCP server")
        
        try:
            tools_result = await self.session.list_tools()
            tools = [tool.name for tool in tools_result.tools]
            logger.info(f"Available tools: {tools}")
            return tools
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Optional[str]:
        """Call a specific tool with arguments."""
        if not self.connected:
            raise RuntimeError("Not connected to MCP server")
        
        arguments = arguments or {}
        
        try:
            logger.info(f"Calling tool '{tool_name}' with arguments: {arguments}")
            result = await self.session.call_tool(tool_name, arguments=arguments)
            
            if result.content:
                response = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                logger.info(f"Tool '{tool_name}' executed successfully")
                return response
            else:
                logger.warning(f"Tool '{tool_name}' returned no content")
                return "Tool executed successfully (no output)"
                
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}': {e}")
            return None
    
    # Convenience methods for common operations
    async def take_screenshot(self, path: str = None) -> Optional[str]:
        """Take a screenshot."""
        args = {"path": path} if path else {}
        return await self.call_tool("get_screenshot", args)
    
    async def execute_command(self, command: str, timeout_ms: int = 30000) -> Optional[str]:
        """Execute a system command."""
        return await self.call_tool("execute_command", {
            "command": command,
            "timeout_ms": timeout_ms
        })
    
    async def read_file(self, path: str, offset: int = 0, length: int = 1000) -> Optional[str]:
        """Read file contents."""
        return await self.call_tool("read_file", {
            "path": path,
            "offset": offset,
            "length": length
        })
    
    async def write_file(self, path: str, content: str, mode: str = "rewrite") -> Optional[str]:
        """Write to a file."""
        return await self.call_tool("write_file", {
            "path": path,
            "content": content,
            "mode": mode
        })
    
    async def list_directory(self, path: str) -> Optional[str]:
        """List directory contents."""
        return await self.call_tool("list_directory", {"path": path})
    
    async def search_files(self, path: str, pattern: str) -> Optional[str]:
        """Search for files by pattern."""
        return await self.call_tool("search_files", {
            "path": path,
            "pattern": pattern
        })


# Context manager for easy usage
class MCPClientContext:
    """Context manager for MCP client."""
    
    def __init__(self, api_key: str = None):
        self.client = MCPClient(api_key)
    
    async def __aenter__(self):
        await self.client.connect()
        return self.client
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()


# Simple test function
async def test_mcp_connection():
    """Test MCP connection and basic functionality."""
    try:
        async with MCPClientContext() as client:
            # List available tools
            tools = await client.list_tools()
            print(f"✓ Connected successfully. Available tools: {tools}")
            
            # Test basic operations
            print("\n--- Testing Basic Operations ---")
            
            # 1. List current directory
            dir_result = await client.list_directory(".")
            if dir_result:
                print(f"✓ Directory listing successful")
                print(f"First few items: {dir_result[:200]}...")
            
            # 2. Take a screenshot
            screenshot_result = await client.take_screenshot("test_screenshot.png")
            if screenshot_result:
                print(f"✓ Screenshot taken: {screenshot_result}")
            
            # 3. Execute a simple command
            cmd_result = await client.execute_command("echo Hello from MCP!")
            if cmd_result:
                print(f"✓ Command executed: {cmd_result}")
            
            print("\n✓ All basic tests completed successfully!")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
