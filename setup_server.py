#!/usr/bin/env python3
"""
Setup script for Cellenium-Lite server
"""

import os
import sys
import subprocess
from pathlib import Path


def install_additional_requirements():
    """Install additional requirements for the server."""
    additional_packages = [
        "uvicorn[standard]",
        "click",
        "aiofiles"
    ]
    
    for package in additional_packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def create_env_template():
    """Create .env template if it doesn't exist."""
    env_path = Path(".env")
    
    if not env_path.exists():
        env_template = """# Cellenium-Lite Environment Variables
# Copy this file to .env and fill in your actual values

# Smithery API Key for Desktop Commander
SMITHERY_API_KEY=your_smithery_api_key_here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Optional: Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=cellenium.log
"""
        
        with open(env_path, 'w') as f:
            f.write(env_template)
        
        print(f"✅ Created .env template at {env_path}")
        print("📝 Please edit .env file with your actual API keys")
    else:
        print("✅ .env file already exists")


def create_startup_scripts():
    """Create convenient startup scripts."""
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Cellenium-Lite Server...

REM Test connection first
echo Testing MCP connection...
python bini_ai/src/server/server.py test

if %ERRORLEVEL% EQU 0 (
    echo Connection successful! Starting web server...
    python bini_ai/src/server/server.py web --host 0.0.0.0 --port 8000
) else (
    echo Connection failed! Please check your .env configuration.
    pause
)
"""
    
    with open("start_server.bat", 'w') as f:
        f.write(windows_script)
    
    # Linux/Mac shell script
    unix_script = """#!/bin/bash
echo "Starting Cellenium-Lite Server..."

# Test connection first
echo "Testing MCP connection..."
python3 bini_ai/src/server/server.py test

if [ $? -eq 0 ]; then
    echo "Connection successful! Starting web server..."
    python3 bini_ai/src/server/server.py web --host 0.0.0.0 --port 8000
else
    echo "Connection failed! Please check your .env configuration."
    read -p "Press any key to continue..."
fi
"""
    
    with open("start_server.sh", 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable
    try:
        os.chmod("start_server.sh", 0o755)
    except:
        pass  # Windows or permission issues
    
    print("✅ Created startup scripts: start_server.bat and start_server.sh")


def main():
    """Main setup function."""
    print("🚀 Setting up Cellenium-Lite Server")
    print("=" * 40)
    
    try:
        # Install additional requirements
        install_additional_requirements()
        
        # Create environment template
        create_env_template()
        
        # Create startup scripts
        create_startup_scripts()
        
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Test connection: python bini_ai/src/server/server.py test")
        print("3. Start web server: python bini_ai/src/server/server.py web")
        print("4. Or use startup scripts: start_server.bat (Windows) or ./start_server.sh (Linux/Mac)")
        print("5. Visit http://localhost:8000 for the web interface")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
