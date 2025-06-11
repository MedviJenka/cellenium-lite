#!/usr/bin/env python3
"""
Simple runner for Cellenium-Lite server
"""

import os
import sys
from pathlib import Path

# Change to the project directory
project_dir = Path(__file__).parent
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

print("🤖 Cellenium-Lite Server")
print("=" * 30)

def run_server():
    """Run the server in web mode."""
    try:
        print("📦 Installing required packages...")
        os.system("python -m pip install uvicorn fastapi click aiofiles mcp python-dotenv pydantic")
        
        print("\n🌐 Starting web server...")
        print("🔗 Server will be available at: http://localhost:8000")
        print("📖 API docs will be at: http://localhost:8000/docs")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Import and run the server
        import uvicorn
        from bini_ai.src.server.web_server import app
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTrying alternative method...")
        
        # Alternative: run the original server
        try:
            from bini_ai.src.server.server import main
            sys.argv = ["server.py", "web"]
            main()
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")

if __name__ == "__main__":
    run_server()
