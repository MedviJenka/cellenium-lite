# Cellenium-Lite Server Usage Guide

## 🚀 Quick Start

### 1. Setup
```bash
# Run the setup script
python setup_server.py

# Edit .env file with your API keys
# SMITHERY_API_KEY=your_key_here
# AZURE_OPENAI_API_KEY=your_azure_key_here
# AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
```

### 2. Test Connection
```bash
# Test MCP connection
python bini_ai/src/server/server.py test
```

### 3. Start Server
```bash
# Web server mode
python bini_ai/src/server/server.py web

# Or use startup scripts
start_server.bat         # Windows
./start_server.sh        # Linux/Mac
```

## 🌐 Web Server Usage

### Start Web Server
```bash
python bini_ai/src/server/server.py web --host 0.0.0.0 --port 8000
```

### Access Web Interface
- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "healthy",
  "mcp_connected": true,
  "available_tools": 15,
  "timestamp": "2025-06-11T15:30:00"
}
```

#### 2. Take Screenshot
```bash
curl -X POST http://localhost:8000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.png"}'
```

#### 3. Execute Command
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "echo Hello World", "timeout_ms": 5000}'
```

#### 4. AI Validation
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Verify desktop is visible",
    "take_screenshot": true
  }'
```

#### 5. Automation Workflow
```bash
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{
    "commands": ["calc", "timeout 3"],
    "validation_prompt": "Verify calculator is open"
  }'
```

## 💻 CLI Usage

### Basic Commands
```bash
# Test connection
python bini_ai/src/server/server.py cli test-connection

# Take screenshot
python bini_ai/src/server/server.py cli screenshot -f "my_screenshot.png"

# Execute command
python bini_ai/src/server/server.py cli execute "dir"

# AI validation
python bini_ai/src/server/server.py cli validate "Check if desktop is visible"

# Automation with validation
python bini_ai/src/server/server.py cli automate "calc" "timeout 3" -v "Verify calculator is open"
```

### File Operations
```bash
# Read file
python bini_ai/src/server/server.py cli read-file "README.md"

# Write file
python bini_ai/src/server/server.py cli write-file "test.txt" "Hello World"

# List directory
python bini_ai/src/server/server.py cli list-dir "."
```

### Test Suites
```bash
# Create sample configuration
python bini_ai/src/server/server.py cli create-sample-config

# Run test suite
python bini_ai/src/server/server.py cli run-test-suite -c sample_test_config.json
```

## 🎮 Interactive Mode

```bash
python bini_ai/src/server/server.py interactive
```

Interactive commands:
- `screenshot [filename]` - Take screenshot
- `execute <command>` - Run system command
- `validate "<prompt>"` - AI validation
- `tools` - List available tools
- `help` - Show help
- `quit` - Exit

## 📋 Test Configuration Format

Create JSON test configurations:

```json
{
  "name": "My Test Suite",
  "description": "Example tests",
  "tests": [
    {
      "name": "Calculator Test",
      "type": "automation",
      "commands": ["calc", "timeout 3"],
      "validation_prompt": "Verify calculator is open",
      "sample_image": ""
    },
    {
      "name": "Desktop Check",
      "type": "validation",
      "prompt": "Verify desktop is functional",
      "image_path": "",
      "sample_image": ""
    }
  ]
}
```

## 🔧 Advanced Usage

### Custom Validation Prompts
```python
# Specific UI validation
"Verify that the login button is visible and has blue background color"

# Comparative validation
"Compare current screen with baseline image for layout differences"

# Functional validation
"Confirm that all menu items are accessible and properly aligned"
```

### Automation Workflows
```python
# Web browser testing
commands = [
    "start chrome https://google.com",
    "timeout 5"
]
validation = "Verify Google homepage loaded with search functionality"

# Desktop application testing
commands = [
    "notepad",
    "timeout 2"
]
validation = "Confirm Notepad is open and ready for input"
```

### Error Handling
The server provides comprehensive error handling:
- Connection failures
- Invalid commands
- AI analysis errors
- File operation errors

Example error response:
```json
{
  "session_id": "uuid-here",
  "success": false,
  "error": "Screenshot failed: Display not accessible",
  "timestamp": "2025-06-11T15:30:00"
}
```

## 🧪 Testing Examples

### Web Application Testing
```bash
# Test Google homepage
python bini_ai/src/server/server.py cli automate \
  "start chrome https://google.com" \
  "timeout 5" \
  -v "Verify Google search page is loaded with search box visible"
```

### Desktop Application Testing
```bash
# Test Windows Calculator
python bini_ai/src/server/server.py cli automate \
  "calc" \
  "timeout 3" \
  -v "Confirm calculator application is open and number pad is visible"
```

### File System Testing
```bash
# Create and validate file
python bini_ai/src/server/server.py cli write-file "test.txt" "Hello World"
python bini_ai/src/server/server.py cli read-file "test.txt"
```

### Visual Regression Testing
```bash
# Take baseline screenshot
python bini_ai/src/server/server.py cli screenshot -f "baseline.png"

# Later, compare current state
python bini_ai/src/server/server.py cli validate \
  "Compare current desktop with baseline image for any visual changes" \
  -s "baseline.png"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Failed
```
Error: Failed to connect to MCP server
```
**Solution**: Check your SMITHERY_API_KEY in .env file

#### 2. Screenshot Failed
```
Error: Screenshot failed: Display not accessible
```
**Solution**: Ensure the display is accessible and permissions are correct

#### 3. AI Validation Failed
```
Error: Azure OpenAI API error
```
**Solution**: Verify AZURE_OPENAI_API_KEY and endpoint configuration

#### 4. Command Execution Failed
```
Error: Command execution failed
```
**Solution**: Check command syntax and system permissions

### Debug Mode
```bash
# Enable debug logging
python bini_ai/src/server/server.py web --debug

# Check logs
tail -f cellenium.log
```

### Health Diagnostics
```bash
# Check system health
curl http://localhost:8000/health

# List available tools
curl http://localhost:8000/tools
```

## 📊 Monitoring and Logging

### Log Files
- **Server logs**: `cellenium.log`
- **Test results**: `test_results_YYYYMMDD_HHMMSS.json`
- **Screenshots**: `*.png` files in working directory

### Metrics
The server tracks:
- Test execution time
- Success/failure rates
- Screenshot capture success
- AI validation accuracy

### Result Storage
Test results are stored with:
- Session ID
- Timestamp
- Success status
- Detailed results
- Error information (if any)

## 🔄 Integration Examples

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Cellenium Tests
  run: |
    python setup_server.py
    python bini_ai/src/server/server.py test
    python bini_ai/src/server/server.py cli run-test-suite -c tests/ui_tests.json
```

### Python Integration
```python
import asyncio
from bini_ai.src.server.mcp_client import MCPClientContext
from bini_ai.src.utils.bini_utils import BiniUtils

async def custom_test():
    async with MCPClientContext() as client:
        await client.take_screenshot("test.png")
        
        bini = BiniUtils()
        result = bini.run(
            prompt="Verify application loaded correctly",
            image_path="test.png"
        )
        
        print(f"Test result: {result}")

asyncio.run(custom_test())
```

### REST API Integration
```javascript
// JavaScript example
const response = await fetch('http://localhost:8000/validate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Verify login form is visible',
    take_screenshot: true
  })
});

const result = await response.json();
console.log('Validation result:', result);
```

## 🚀 Next Steps

1. **Start with basic tests**: Use simple screenshot and validation commands
2. **Build test suites**: Create JSON configurations for your specific applications
3. **Integrate with CI/CD**: Add automated testing to your deployment pipeline
4. **Customize prompts**: Develop specific validation prompts for your use cases
5. **Monitor results**: Use the web interface to track test success rates

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Architecture Diagram**: See the SVG diagram in the project
- **Development Roadmap**: Check DEVELOPMENT_ROADMAP.md
- **Sample Tests**: Look at existing test files in the tests/ directory

For more help, check the server logs or use the interactive mode for real-time testing and debugging.
