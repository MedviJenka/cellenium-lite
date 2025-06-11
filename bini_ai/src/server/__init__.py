"""
Cellenium-Lite Server Package
AI-powered visual testing and desktop automation server components
"""

from .mcp_client import MCPClient, MCPClientContext
from .web_server import app
from .cli import cli

__version__ = "1.0.0"
__all__ = ["MCPClient", "MCPClientContext", "app", "cli"]
