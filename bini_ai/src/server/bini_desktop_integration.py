import asyncio
import tempfile
import os
from typing import Optional, Union
from bini_ai.src.server.enhanced_server import DesktopCommanderClient
from bini_ai.src.utils.bini_utils import BiniUtils


class BiniDesktopIntegration:
    """Integration layer between Bini AI testing and Desktop Commander."""
    
    def __init__(self, chain_of_thought: bool = True, to_json: bool = False):
        self.bini_utils = BiniUtils(chain_of_thought=chain_of_thought, to_json=to_json)
        self.desktop_client = DesktopCommanderClient()
        self.connected = False
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.desktop_client.connect()
        self.connected = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.connected:
            await self.desktop_client.disconnect()
            self.connected = False
    
    async def validate_screen_with_ai(
        self, 
        prompt: str, 
        screenshot_path: Optional[str] = None,
        sample_image: Union[str, list] = ''
    ) -> str:
        """
        Capture screenshot and validate using AI vision.
        
        Args:
            prompt: Validation prompt for the AI
            screenshot_path: Optional path to save screenshot
            sample_image: Reference image(s) for comparison
            
        Returns:
            AI validation result (Passed/Failed with reasoning)
        """
        if not self.connected:
            raise RuntimeError("Desktop client not connected. Use as async context manager.")
        
        # Take screenshot
        if screenshot_path is None:
            # Create temporary file for screenshot
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                screenshot_path = tmp_file.name
        
        screenshot_result = await self.desktop_client.take_screenshot(screenshot_path)
        
        if screenshot_result is None:
            return "Failed: Could not capture screenshot"
        
        try:
            # Use Bini AI to analyze the screenshot
            result = self.bini_utils.run(
                prompt=prompt,
                image_path=screenshot_path,
                sample_image=sample_image
            )
            return result
            
        except Exception as e:
            return f"Failed: Error in AI analysis - {str(e)}"
        
        finally:
            # Clean up temporary screenshot if we created it
            if screenshot_path.startswith(tempfile.gettempdir()):
                try:
                    os.unlink(screenshot_path)
                except:
                    pass
    
    async def automate_and_validate(
        self,
        automation_commands: list,
        validation_prompt: str,
        sample_image: Union[str, list] = ''
    ) -> dict:
        """
        Execute automation commands and then validate the result.
        
        Args:
            automation_commands: List of commands to execute
            validation_prompt: Prompt for AI validation
            sample_image: Reference image(s) for comparison
            
        Returns:
            Dictionary with automation results and validation
        """
        results = {
            'automation_results': [],
            'validation_result': None,
            'success': False
        }
        
        try:
            # Execute automation commands
            for i, command in enumerate(automation_commands):
                print(f"Executing command {i+1}/{len(automation_commands)}: {command}")
                result = await self.desktop_client.execute_command(command)
                results['automation_results'].append({
                    'command': command,
                    'result': result,
                    'success': result is not None
                })
                
                # Small delay between commands
                await asyncio.sleep(1)
            
            # Validate the final state
            validation_result = await self.validate_screen_with_ai(
                prompt=validation_prompt,
                sample_image=sample_image
            )
            
            results['validation_result'] = validation_result
            results['success'] = 'Passed' in validation_result
            
        except Exception as e:
            results['error'] = str(e)
            results['success'] = False
        
        return results
    
    async def validate_file_content(
        self,
        file_path: str,
        validation_prompt: str,
        expected_content: str = None
    ) -> str:
        """
        Read file content and validate using AI.
        
        Args:
            file_path: Path to file to validate
            validation_prompt: Prompt for AI validation
            expected_content: Expected content for comparison
            
        Returns:
            AI validation result
        """
        try:
            # Read file content
            file_content = await self.desktop_client.read_file(file_path)
            
            if file_content is None:
                return "Failed: Could not read file"
            
            # Create enhanced prompt with file content
            enhanced_prompt = f"""
            {validation_prompt}
            
            File content to validate:
            {file_content}
            
            Expected content (if provided):
            {expected_content or 'No expected content provided'}
            """
            
            # Use text analysis (you might need to implement this in BiniUtils)
            # For now, we'll use a simple validation approach
            if expected_content and expected_content in file_content:
                return "Passed: File contains expected content"
            elif expected_content:
                return "Failed: File does not contain expected content"
            else:
                return f"Passed: File read successfully. Content length: {len(file_content)} characters"
                
        except Exception as e:
            return f"Failed: Error reading/validating file - {str(e)}"


# Example usage function
async def example_web_test():
    """Example web application test using the integration."""
    
    async with BiniDesktopIntegration(chain_of_thought=True) as bini_desktop:
        
        # Test scenario: Open a web browser and validate Google homepage
        automation_commands = [
            "start chrome",
            "timeout 3",  # Wait for browser to start
        ]
        
        # Execute automation and validate
        result = await bini_desktop.automate_and_validate(
            automation_commands=automation_commands,
            validation_prompt="Verify that Google homepage is loaded and the search box is visible",
            sample_image=""  # Could provide reference image here
        )
        
        print("Test Results:")
        print(f"Success: {result['success']}")
        print(f"Validation: {result['validation_result']}")
        
        return result


async def example_file_test():
    """Example file validation test."""
    
    async with BiniDesktopIntegration() as bini_desktop:
        
        # Test file content
        result = await bini_desktop.validate_file_content(
            file_path="README.md",
            validation_prompt="Check if this is a valid README file with project information",
            expected_content="cellenium-lite"
        )
        
        print(f"File validation result: {result}")
        return result


if __name__ == "__main__":
    # Run example tests
    print("Running web test example...")
    asyncio.run(example_web_test())
    
    print("\nRunning file test example...")
    asyncio.run(example_file_test())
