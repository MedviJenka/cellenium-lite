from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import os
import tempfile
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .mcp_client import MCPClientContext
from ..utils.bini_utils import BiniUtils


# Pydantic models for API requests
class ScreenshotRequest(BaseModel):
    filename: Optional[str] = None


class CommandRequest(BaseModel):
    command: str
    timeout_ms: int = 30000


class FileReadRequest(BaseModel):
    path: str
    offset: int = 0
    length: int = 1000


class FileWriteRequest(BaseModel):
    path: str
    content: str
    mode: str = "rewrite"


class ValidationRequest(BaseModel):
    prompt: str
    image_path: Optional[str] = None
    sample_image: Optional[str] = None
    take_screenshot: bool = False


class AutomationRequest(BaseModel):
    commands: List[str]
    validation_prompt: str
    sample_image: Optional[str] = None


# FastAPI app
app = FastAPI(
    title="Cellenium-Lite Server",
    description="AI-powered visual testing and desktop automation server",
    version="1.0.0"
)

# Store for active sessions and results
active_sessions: Dict[str, Any] = {}
test_results: Dict[str, Any] = {}

# Initialize Bini Utils
bini_utils = BiniUtils(chain_of_thought=True, to_json=False)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic web interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cellenium-Lite Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #fff; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
            .get { background-color: #61affe; }
            .post { background-color: #49cc90; }
            .delete { background-color: #f93e3e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Cellenium-Lite Server</h1>
            <p>AI-powered visual testing and desktop automation server</p>
            
            <h2>Available Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/health</strong>
                <p>Check server health and MCP connection status</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/tools</strong>
                <p>List available MCP tools</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/screenshot</strong>
                <p>Take a screenshot of the desktop</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/execute</strong>
                <p>Execute a system command</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/validate</strong>
                <p>Validate screen or image using AI</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span> <strong>/automate</strong>
                <p>Run automation workflow with validation</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span> <strong>/results/{session_id}</strong>
                <p>Get test results for a session</p>
            </div>
            
            <h2>Quick Test</h2>
            <p>Try: <a href="/health">/health</a> | <a href="/tools">/tools</a> | <a href="/docs">/docs</a></p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        async with MCPClientContext() as client:
            tools = await client.list_tools()
            return {
                "status": "healthy",
                "mcp_connected": True,
                "available_tools": len(tools),
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "mcp_connected": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/tools")
async def list_tools():
    """List available MCP tools."""
    try:
        async with MCPClientContext() as client:
            tools = await client.list_tools()
            return {"tools": tools, "count": len(tools)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tools: {str(e)}")


@app.post("/screenshot")
async def take_screenshot(request: ScreenshotRequest):
    """Take a screenshot."""
    try:
        async with MCPClientContext() as client:
            filename = request.filename or f"screenshot_{uuid.uuid4().hex[:8]}.png"
            result = await client.take_screenshot(filename)
            
            return {
                "success": True,
                "filename": filename,
                "message": result,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot failed: {str(e)}")


@app.post("/execute")
async def execute_command(request: CommandRequest):
    """Execute a system command."""
    try:
        async with MCPClientContext() as client:
            result = await client.execute_command(request.command, request.timeout_ms)
            
            return {
                "success": True,
                "command": request.command,
                "output": result,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Command execution failed: {str(e)}")


@app.post("/files/read")
async def read_file(request: FileReadRequest):
    """Read file contents."""
    try:
        async with MCPClientContext() as client:
            content = await client.read_file(request.path, request.offset, request.length)
            
            return {
                "success": True,
                "path": request.path,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File read failed: {str(e)}")


@app.post("/files/write")
async def write_file(request: FileWriteRequest):
    """Write to a file."""
    try:
        async with MCPClientContext() as client:
            result = await client.write_file(request.path, request.content, request.mode)
            
            return {
                "success": True,
                "path": request.path,
                "mode": request.mode,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File write failed: {str(e)}")


@app.post("/validate")
async def validate_screen(request: ValidationRequest):
    """Validate screen or image using AI."""
    session_id = str(uuid.uuid4())
    
    try:
        image_path = request.image_path
        
        # Take screenshot if requested
        if request.take_screenshot or not image_path:
            async with MCPClientContext() as client:
                screenshot_filename = f"validation_{session_id}.png"
                await client.take_screenshot(screenshot_filename)
                image_path = screenshot_filename
        
        # Run AI validation
        validation_result = bini_utils.run(
            prompt=request.prompt,
            image_path=image_path,
            sample_image=request.sample_image or ''
        )
        
        # Store results
        result_data = {
            "session_id": session_id,
            "prompt": request.prompt,
            "image_path": image_path,
            "sample_image": request.sample_image,
            "validation_result": validation_result,
            "success": "Passed" in validation_result,
            "timestamp": datetime.now().isoformat()
        }
        
        test_results[session_id] = result_data
        
        return result_data
        
    except Exception as e:
        error_result = {
            "session_id": session_id,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        test_results[session_id] = error_result
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.post("/automate")
async def run_automation(request: AutomationRequest):
    """Run automation workflow with validation."""
    session_id = str(uuid.uuid4())
    
    try:
        async with MCPClientContext() as client:
            automation_results = []
            
            # Execute commands
            for i, command in enumerate(request.commands):
                print(f"Executing command {i+1}/{len(request.commands)}: {command}")
                cmd_result = await client.execute_command(command)
                automation_results.append({
                    "command": command,
                    "result": cmd_result,
                    "success": cmd_result is not None
                })
                
                # Small delay between commands
                await asyncio.sleep(1)
            
            # Take final screenshot for validation
            final_screenshot = f"automation_{session_id}_final.png"
            await client.take_screenshot(final_screenshot)
            
            # Run AI validation
            validation_result = bini_utils.run(
                prompt=request.validation_prompt,
                image_path=final_screenshot,
                sample_image=request.sample_image or ''
            )
            
            # Compile results
            result_data = {
                "session_id": session_id,
                "automation_results": automation_results,
                "validation_prompt": request.validation_prompt,
                "validation_result": validation_result,
                "final_screenshot": final_screenshot,
                "success": "Passed" in validation_result,
                "timestamp": datetime.now().isoformat()
            }
            
            test_results[session_id] = result_data
            return result_data
            
    except Exception as e:
        error_result = {
            "session_id": session_id,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        test_results[session_id] = error_result
        raise HTTPException(status_code=500, detail=f"Automation failed: {str(e)}")


@app.get("/results/{session_id}")
async def get_results(session_id: str):
    """Get test results for a session."""
    if session_id not in test_results:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return test_results[session_id]


@app.get("/results")
async def list_all_results():
    """List all test results."""
    return {
        "sessions": list(test_results.keys()),
        "total_sessions": len(test_results),
        "results": test_results
    }


@app.delete("/results/{session_id}")
async def delete_results(session_id: str):
    """Delete results for a session."""
    if session_id not in test_results:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del test_results[session_id]
    return {"message": f"Results for session {session_id} deleted"}


# Background task for cleanup
@app.on_event("startup")
async def startup_event():
    """Startup tasks."""
    print("🚀 Cellenium-Lite Server starting up...")
    
    # Test MCP connection
    try:
        async with MCPClientContext() as client:
            tools = await client.list_tools()
            print(f"✓ MCP connection successful. Available tools: {len(tools)}")
    except Exception as e:
        print(f"⚠️  MCP connection failed: {e}")
    
    print("✓ Server ready!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
