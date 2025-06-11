# Quick Start Guide - Cellenium-Lite

## Prerequisites
- Python 3.11+
- Windows 10/11 (for Desktop Commander)
- Smithery API key
- Azure OpenAI API access

## Setup Instructions

### 1. Environment Configuration
```bash
# Clone and navigate to project
cd C:\Users\medvi\OneDrive\Desktop\cellenium-lite

# Create .env file with your keys
echo SMITHERY_API_KEY=your_key_here > .env
echo AZURE_OPENAI_API_KEY=your_azure_key >> .env
echo AZURE_OPENAI_ENDPOINT=your_azure_endpoint >> .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test Basic Connection
```bash
python bini_ai/src/server/enhanced_server.py
```

### 4. Run Your First Test
```python
import asyncio
from bini_ai.src.server.bini_desktop_integration import BiniDesktopIntegration

async def first_test():
    async with BiniDesktopIntegration() as bini_desktop:
        result = await bini_desktop.validate_screen_with_ai(
            "Check if the desktop is visible and functional"
        )
        print(f"Result: {result}")

asyncio.run(first_test())
```

### 5. Run Comprehensive Tests
```bash
pytest tests/test_desktop_integration.py -v -s
```

## Common Issues and Solutions

### Connection Issues
- Verify SMITHERY_API_KEY is correct
- Check internet connection
- Ensure Desktop Commander service is accessible

### Screenshot Issues
- Verify display settings
- Check file permissions
- Ensure sufficient disk space

### AI Analysis Issues
- Verify Azure OpenAI credentials
- Check prompt formatting
- Monitor API rate limits

## Example Use Cases

### Web Testing
```python
# Test Google homepage
automation_commands = ["start chrome https://google.com", "timeout 3"]
validation_prompt = "Verify Google homepage loaded with search box visible"
```

### Desktop Application Testing
```python
# Test Calculator app
automation_commands = ["calc", "timeout 2"]
validation_prompt = "Confirm Windows Calculator is open and functional"
```

### File Operations Testing
```python
# Test file creation and validation
await client.write_file("test.txt", "test content")
result = await client.validate_file_content("test.txt", "Check file content")
```

## What's Next?

1. **Explore the Examples**: Try the test cases in `tests/test_desktop_integration.py`
2. **Create Custom Tests**: Build tests specific to your applications
3. **Integrate with CI/CD**: Add to your automated testing pipeline
4. **Extend Functionality**: Add new validation prompts and automation commands

## Getting Help

- Check the logs in `bini_tests.log`
- Review error messages for debugging
- Refer to the architecture diagram for system understanding
- Consult the development roadmap for planned features
