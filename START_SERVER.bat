@echo off
echo 🤖 Starting Cellenium-Lite Server...
echo.

cd /d "C:\Users\medvi\OneDrive\Desktop\cellenium-lite"

echo 📦 Installing dependencies...
python -m pip install uvicorn fastapi click aiofiles mcp python-dotenv pydantic --quiet

echo.
echo 🌐 Starting web server...
echo 🔗 Open your browser to: http://localhost:8000
echo 📖 API docs available at: http://localhost:8000/docs
echo ⏹️  Press Ctrl+C to stop the server
echo.

python run_server.py

pause
