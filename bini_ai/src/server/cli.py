import asyncio
import click
import json
import os
from datetime import datetime
from .mcp_client import MCPClientContext
from ..utils.bini_utils import BiniUtils


# Initialize Bini Utils
bini_utils = BiniUtils(chain_of_thought=True, to_json=False)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🤖 Cellenium-Lite - AI-powered visual testing and desktop automation"""
    pass


@cli.command()
def test_connection():
    """Test MCP server connection."""
    click.echo("🔗 Testing MCP connection...")
    
    async def _test():
        try:
            async with MCPClientContext() as client:
                tools = await client.list_tools()
                click.echo(f"✅ Connected successfully!")
                click.echo(f"📋 Available tools ({len(tools)}): {', '.join(tools)}")
                return True
        except Exception as e:
            click.echo(f"❌ Connection failed: {e}")
            return False
    
    success = asyncio.run(_test())
    exit(0 if success else 1)


@cli.command()
@click.option('--filename', '-f', help='Screenshot filename')
def screenshot(filename):
    """Take a screenshot."""
    if not filename:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    click.echo(f"📸 Taking screenshot: {filename}")
    
    async def _screenshot():
        try:
            async with MCPClientContext() as client:
                result = await client.take_screenshot(filename)
                click.echo(f"✅ Screenshot saved: {filename}")
                click.echo(f"📄 Result: {result}")
        except Exception as e:
            click.echo(f"❌ Screenshot failed: {e}")
    
    asyncio.run(_screenshot())


@cli.command()
@click.argument('command')
@click.option('--timeout', '-t', default=30000, help='Timeout in milliseconds')
def execute(command, timeout):
    """Execute a system command."""
    click.echo(f"⚡ Executing: {command}")
    
    async def _execute():
        try:
            async with MCPClientContext() as client:
                result = await client.execute_command(command, timeout)
                click.echo(f"✅ Command executed successfully")
                click.echo(f"📄 Output:\n{result}")
        except Exception as e:
            click.echo(f"❌ Command failed: {e}")
    
    asyncio.run(_execute())


@cli.command()
@click.argument('path')
@click.option('--offset', '-o', default=0, help='Start reading from line offset')
@click.option('--length', '-l', default=1000, help='Number of lines to read')
def read_file(path, offset, length):
    """Read file contents."""
    click.echo(f"📖 Reading file: {path}")
    
    async def _read():
        try:
            async with MCPClientContext() as client:
                content = await client.read_file(path, offset, length)
                click.echo(f"✅ File read successfully")
                click.echo(f"📄 Content:\n{content}")
        except Exception as e:
            click.echo(f"❌ File read failed: {e}")
    
    asyncio.run(_read())


@cli.command()
@click.argument('path')
@click.argument('content')
@click.option('--mode', '-m', default='rewrite', type=click.Choice(['rewrite', 'append']), help='Write mode')
def write_file(path, content, mode):
    """Write content to a file."""
    click.echo(f"✏️  Writing to file: {path} (mode: {mode})")
    
    async def _write():
        try:
            async with MCPClientContext() as client:
                result = await client.write_file(path, content, mode)
                click.echo(f"✅ File written successfully")
                click.echo(f"📄 Result: {result}")
        except Exception as e:
            click.echo(f"❌ File write failed: {e}")
    
    asyncio.run(_write())


@cli.command()
@click.argument('path')
def list_dir(path):
    """List directory contents."""
    click.echo(f"📁 Listing directory: {path}")
    
    async def _list():
        try:
            async with MCPClientContext() as client:
                result = await client.list_directory(path)
                click.echo(f"✅ Directory listed successfully")
                click.echo(f"📄 Contents:\n{result}")
        except Exception as e:
            click.echo(f"❌ Directory listing failed: {e}")
    
    asyncio.run(_list())


@cli.command()
@click.argument('prompt')
@click.option('--image', '-i', help='Image path to validate')
@click.option('--sample', '-s', help='Sample image for comparison')
@click.option('--screenshot/--no-screenshot', default=True, help='Take screenshot if no image provided')
def validate(prompt, image, sample, screenshot):
    """Validate screen or image using AI."""
    click.echo(f"🤖 AI Validation: {prompt}")
    
    async def _validate():
        try:
            image_path = image
            
            # Take screenshot if needed
            if screenshot and not image_path:
                async with MCPClientContext() as client:
                    screenshot_filename = f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    await client.take_screenshot(screenshot_filename)
                    image_path = screenshot_filename
                    click.echo(f"📸 Screenshot taken: {screenshot_filename}")
            
            if not image_path:
                click.echo("❌ No image provided and screenshot disabled")
                return
            
            # Run AI validation
            click.echo("🧠 Running AI analysis...")
            result = bini_utils.run(
                prompt=prompt,
                image_path=image_path,
                sample_image=sample or ''
            )
            
            # Display results
            if "Passed" in result:
                click.echo("✅ VALIDATION PASSED")
            else:
                click.echo("❌ VALIDATION FAILED")
            
            click.echo(f"📄 AI Response:\n{result}")
            
        except Exception as e:
            click.echo(f"❌ Validation failed: {e}")
    
    asyncio.run(_validate())


@cli.command()
@click.argument('commands', nargs=-1, required=True)
@click.option('--validate-prompt', '-v', required=True, help='Validation prompt for final state')
@click.option('--sample', '-s', help='Sample image for comparison')
def automate(commands, validate_prompt, sample):
    """Run automation commands and validate the result."""
    click.echo(f"🤖 Running automation workflow...")
    click.echo(f"📋 Commands: {list(commands)}")
    click.echo(f"🎯 Validation: {validate_prompt}")
    
    async def _automate():
        try:
            async with MCPClientContext() as client:
                # Execute commands
                for i, command in enumerate(commands):
                    click.echo(f"⚡ [{i+1}/{len(commands)}] Executing: {command}")
                    result = await client.execute_command(command)
                    if result:
                        click.echo(f"✅ Command completed")
                    else:
                        click.echo(f"⚠️  Command may have failed")
                    
                    # Delay between commands
                    await asyncio.sleep(1)
                
                # Take final screenshot
                final_screenshot = f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                await client.take_screenshot(final_screenshot)
                click.echo(f"📸 Final screenshot: {final_screenshot}")
                
                # Validate result
                click.echo("🧠 Running final validation...")
                validation_result = bini_utils.run(
                    prompt=validate_prompt,
                    image_path=final_screenshot,
                    sample_image=sample or ''
                )
                
                # Display results
                if "Passed" in validation_result:
                    click.echo("✅ AUTOMATION SUCCESSFUL")
                else:
                    click.echo("❌ AUTOMATION FAILED VALIDATION")
                
                click.echo(f"📄 Validation Result:\n{validation_result}")
                
        except Exception as e:
            click.echo(f"❌ Automation failed: {e}")
    
    asyncio.run(_automate())


@cli.command()
@click.option('--config-file', '-c', help='JSON configuration file')
def run_test_suite(config_file):
    """Run a test suite from configuration file."""
    if not config_file or not os.path.exists(config_file):
        click.echo("❌ Configuration file not found")
        return
    
    click.echo(f"📋 Running test suite: {config_file}")
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        tests = config.get('tests', [])
        click.echo(f"🧪 Found {len(tests)} test(s)")
        
        async def _run_suite():
            results = []
            
            for i, test in enumerate(tests):
                click.echo(f"\n🧪 Running test {i+1}/{len(tests)}: {test.get('name', 'Unnamed')}")
                
                try:
                    test_type = test.get('type')
                    
                    if test_type == 'automation':
                        async with MCPClientContext() as client:
                            # Execute commands
                            for cmd in test.get('commands', []):
                                await client.execute_command(cmd)
                                await asyncio.sleep(1)
                            
                            # Take screenshot and validate
                            screenshot = f"test_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            await client.take_screenshot(screenshot)
                            
                            validation_result = bini_utils.run(
                                prompt=test.get('validation_prompt', ''),
                                image_path=screenshot,
                                sample_image=test.get('sample_image', '')
                            )
                            
                            test_result = {
                                'name': test.get('name'),
                                'passed': 'Passed' in validation_result,
                                'result': validation_result
                            }
                            results.append(test_result)
                            
                            status = "✅ PASSED" if test_result['passed'] else "❌ FAILED"
                            click.echo(f"{status}: {test.get('name')}")
                    
                    elif test_type == 'validation':
                        validation_result = bini_utils.run(
                            prompt=test.get('prompt', ''),
                            image_path=test.get('image_path', ''),
                            sample_image=test.get('sample_image', '')
                        )
                        
                        test_result = {
                            'name': test.get('name'),
                            'passed': 'Passed' in validation_result,
                            'result': validation_result
                        }
                        results.append(test_result)
                        
                        status = "✅ PASSED" if test_result['passed'] else "❌ FAILED"
                        click.echo(f"{status}: {test.get('name')}")
                        
                except Exception as e:
                    click.echo(f"❌ Test failed: {e}")
                    results.append({
                        'name': test.get('name'),
                        'passed': False,
                        'error': str(e)
                    })
            
            # Summary
            passed = sum(1 for r in results if r['passed'])
            total = len(results)
            click.echo(f"\n📊 Test Summary: {passed}/{total} passed")
            
            # Save results
            results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'summary': {'passed': passed, 'total': total},
                    'results': results
                }, f, indent=2)
            
            click.echo(f"📄 Results saved to: {results_file}")
        
        asyncio.run(_run_suite())
        
    except Exception as e:
        click.echo(f"❌ Test suite failed: {e}")


@cli.command()
def create_sample_config():
    """Create a sample test configuration file."""
    sample_config = {
        "name": "Sample Test Suite",
        "description": "Example test configuration for Cellenium-Lite",
        "tests": [
            {
                "name": "Calculator Test",
                "type": "automation",
                "commands": [
                    "calc",
                    "timeout 3"
                ],
                "validation_prompt": "Verify that Windows Calculator is open and displaying the number pad",
                "sample_image": ""
            },
            {
                "name": "Notepad Test",
                "type": "automation",
                "commands": [
                    "notepad",
                    "timeout 2"
                ],
                "validation_prompt": "Confirm that Notepad application is open and ready for text input",
                "sample_image": ""
            },
            {
                "name": "Desktop Validation",
                "type": "validation",
                "prompt": "Verify that the desktop is visible and functional",
                "image_path": "",
                "sample_image": ""
            }
        ]
    }
    
    filename = "sample_test_config.json"
    with open(filename, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    click.echo(f"✅ Sample configuration created: {filename}")
    click.echo("📝 Edit this file to customize your tests")
    click.echo(f"🚀 Run with: cellenium run-test-suite -c {filename}")


@cli.command()
def interactive():
    """Start interactive mode."""
    click.echo("🎮 Interactive Mode - Cellenium-Lite")
    click.echo("Type 'help' for commands or 'quit' to exit")
    
    async def _interactive():
        async with MCPClientContext() as client:
            click.echo("✅ Connected to MCP server")
            
            while True:
                try:
                    command = click.prompt("\ncellenium", type=str).strip()
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    elif command.lower() == 'help':
                        click.echo("""
Available commands:
  screenshot [filename]     - Take a screenshot
  execute <command>         - Execute system command
  validate "<prompt>"       - AI validation with screenshot
  tools                     - List available tools
  help                      - Show this help
  quit                      - Exit interactive mode
                        """)
                    elif command.lower() == 'tools':
                        tools = await client.list_tools()
                        click.echo(f"Available tools: {', '.join(tools)}")
                    elif command.startswith('screenshot'):
                        parts = command.split(' ', 1)
                        filename = parts[1] if len(parts) > 1 else f"interactive_{datetime.now().strftime('%H%M%S')}.png"
                        result = await client.take_screenshot(filename)
                        click.echo(f"📸 Screenshot: {filename}")
                    elif command.startswith('execute '):
                        cmd = command[8:]  # Remove 'execute '
                        result = await client.execute_command(cmd)
                        click.echo(f"Output: {result}")
                    elif command.startswith('validate '):
                        prompt = command[9:].strip('"\'')  # Remove 'validate ' and quotes
                        screenshot_file = f"interactive_validation_{datetime.now().strftime('%H%M%S')}.png"
                        await client.take_screenshot(screenshot_file)
                        result = bini_utils.run(prompt=prompt, image_path=screenshot_file)
                        status = "✅ PASSED" if "Passed" in result else "❌ FAILED"
                        click.echo(f"{status}")
                        click.echo(f"Result: {result}")
                    else:
                        click.echo("Unknown command. Type 'help' for available commands.")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"Error: {e}")
            
            click.echo("👋 Goodbye!")
    
    try:
        asyncio.run(_interactive())
    except KeyboardInterrupt:
        click.echo("\n👋 Goodbye!")


if __name__ == '__main__':
    cli()
