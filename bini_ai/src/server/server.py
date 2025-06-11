"""
Cellenium-Lite Server
Main entry point for the AI-powered visual testing and desktop automation server
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from bini_ai.src.server.mcp_client import MCPClientContext, test_mcp_connection
from bini_ai.src.server.web_server import app
from bini_ai.src.server.cli import cli


def main():
    """Main entry point with multiple server modes."""
    parser = argparse.ArgumentParser(
        description="Cellenium-Lite: AI-powered visual testing and desktop automation"
    )
    parser.add_argument(
        'mode',
        choices=['web', 'cli', 'test', 'interactive'],
        help='Server mode to run'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host for web server (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port for web server (default: 8000)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    print("🤖 Cellenium-Lite Server")
    print("=" * 50)
    
    if args.mode == 'web':
        print(f"🌐 Starting web server on {args.host}:{args.port}")
        import uvicorn
        uvicorn.run(
            "bini_ai.src.server.web_server:app",
            host=args.host,
            port=args.port,
            reload=args.debug,
            log_level="debug" if args.debug else "info"
        )
    
    elif args.mode == 'cli':
        print("💻 Starting CLI mode")
        cli()
    
    elif args.mode == 'test':
        print("🧪 Testing MCP connection")
        asyncio.run(test_mcp_connection())
    
    elif args.mode == 'interactive':
        print("🎮 Starting interactive mode")
        from bini_ai.src.server.cli import interactive
        interactive()


if __name__ == "__main__":
    main()
