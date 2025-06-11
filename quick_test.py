import os
import asyncio
from pathlib import Path
import sys

# Add the project to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from bini_ai.src.server.mcp_client import MCPClientContext
    print("✅ Successfully imported MCP client")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing missing packages...")
    os.system("python -m pip install mcp")
    sys.exit(1)

async def quick_test():
    """Quick test of MCP connection."""
    print("🔗 Testing MCP connection...")
    
    try:
        async with MCPClientContext() as client:
            tools = await client.list_tools()
            print(f"✅ Connected successfully!")
            print(f"📋 Available tools ({len(tools)}): {', '.join(tools[:5])}{'...' if len(tools) > 5 else ''}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(quick_test())
    if success:
        print("\n🎉 Ready to run the server!")
    else:
        print("\n⚠️  Please check your .env configuration")
