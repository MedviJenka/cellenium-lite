import pytest
import asyncio
from bini_ai.src.server.bini_desktop_integration import BiniDesktopIntegration


class TestDesktopIntegration:
    """Test cases using Desktop Commander integration."""
    
    @pytest.mark.asyncio
    async def test_basic_screenshot_validation(self):
        """Test basic screenshot capture and AI validation."""
        async with BiniDesktopIntegration() as bini_desktop:
            result = await bini_desktop.validate_screen_with_ai(
                prompt="Verify that the desktop is visible and functional"
            )
            
            assert result is not None
            assert isinstance(result, str)
            # Should contain either "Passed" or "Failed"
            assert any(keyword in result for keyword in ["Passed", "Failed"])
    
    @pytest.mark.asyncio
    async def test_web_browser_automation(self):
        """Test web browser automation with validation."""
        automation_commands = [
            "start msedge https://www.google.com",
            "timeout 5"  # Wait for page to load
        ]
        
        async with BiniDesktopIntegration(chain_of_thought=True) as bini_desktop:
            result = await bini_desktop.automate_and_validate(
                automation_commands=automation_commands,
                validation_prompt="Confirm that Google homepage is loaded with search functionality visible"
            )
            
            assert result['success'] is not None
            assert 'validation_result' in result
            assert 'automation_results' in result
            assert len(result['automation_results']) == len(automation_commands)
    
    @pytest.mark.asyncio
    async def test_file_operations_with_validation(self):
        """Test file operations and content validation."""
        async with BiniDesktopIntegration() as bini_desktop:
            
            # Test file creation
            test_content = "This is a test file created by Bini Desktop Integration"
            write_success = await bini_desktop.desktop_client.write_file(
                "test_output.txt",
                test_content
            )
            
            assert write_success is True
            
            # Test file validation
            validation_result = await bini_desktop.validate_file_content(
                file_path="test_output.txt",
                validation_prompt="Verify this file contains test content",
                expected_content="test file"
            )
            
            assert "Passed" in validation_result
            
            # Cleanup
            await bini_desktop.desktop_client.execute_command("del test_output.txt")
    
    @pytest.mark.asyncio
    async def test_calculator_app_automation(self):
        """Test calculator application automation."""
        automation_commands = [
            "calc",  # Open calculator
            "timeout 3"
        ]
        
        async with BiniDesktopIntegration() as bini_desktop:
            result = await bini_desktop.automate_and_validate(
                automation_commands=automation_commands,
                validation_prompt="Verify that Windows Calculator application is open and displaying the number pad"
            )
            
            # Close calculator
            await bini_desktop.desktop_client.execute_command("taskkill /im Calculator.exe /f")
            
            assert 'validation_result' in result
    
    @pytest.mark.asyncio
    async def test_directory_operations(self):
        """Test directory listing and validation."""
        async with BiniDesktopIntegration() as bini_desktop:
            
            # List current directory
            dir_contents = await bini_desktop.desktop_client.list_directory(".")
            
            assert isinstance(dir_contents, list)
            assert len(dir_contents) > 0
            
            # Validate directory structure
            has_bini_dir = any("bini_ai" in item for item in dir_contents)
            assert has_bini_dir, "Should contain bini_ai directory"
    
    @pytest.mark.asyncio
    async def test_notepad_text_validation(self):
        """Test Notepad automation with text validation."""
        automation_commands = [
            "notepad",
            "timeout 2"
        ]
        
        async with BiniDesktopIntegration() as bini_desktop:
            # Open Notepad
            result = await bini_desktop.automate_and_validate(
                automation_commands=automation_commands,
                validation_prompt="Verify that Notepad application is open and ready for text input"
            )
            
            # Close Notepad without saving
            await bini_desktop.desktop_client.execute_command("taskkill /im notepad.exe /f")
            
            assert 'validation_result' in result
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling for invalid operations."""
        async with BiniDesktopIntegration() as bini_desktop:
            
            # Test invalid file read
            validation_result = await bini_desktop.validate_file_content(
                file_path="nonexistent_file.txt",
                validation_prompt="This should fail gracefully"
            )
            
            assert "Failed" in validation_result
    
    @pytest.mark.asyncio
    async def test_screenshot_comparison(self):
        """Test screenshot comparison functionality."""
        async with BiniDesktopIntegration() as bini_desktop:
            
            # Take baseline screenshot
            baseline_path = "baseline_desktop.png"
            await bini_desktop.desktop_client.take_screenshot(baseline_path)
            
            # Take another screenshot and compare
            result = await bini_desktop.validate_screen_with_ai(
                prompt="Compare current desktop state with baseline image for any significant changes",
                sample_image=baseline_path
            )
            
            assert result is not None
            assert isinstance(result, str)
            
            # Cleanup
            await bini_desktop.desktop_client.execute_command(f"del {baseline_path}")
    
    @pytest.mark.asyncio
    async def test_multi_step_workflow(self):
        """Test complex multi-step workflow."""
        async with BiniDesktopIntegration(chain_of_thought=True) as bini_desktop:
            
            workflow_steps = [
                {
                    'commands': ["mkdir test_workflow"],
                    'validation': "Verify that test_workflow directory was created"
                },
                {
                    'commands': ["echo Test content > test_workflow/test.txt"],
                    'validation': "Confirm test file was created in the workflow directory"
                },
                {
                    'commands': ["dir test_workflow"],
                    'validation': "Validate directory listing shows the test file"
                }
            ]
            
            workflow_results = []
            
            for step in workflow_steps:
                result = await bini_desktop.automate_and_validate(
                    automation_commands=step['commands'],
                    validation_prompt=step['validation']
                )
                workflow_results.append(result)
            
            # Cleanup
            await bini_desktop.desktop_client.execute_command("rmdir /s /q test_workflow")
            
            # Verify all steps succeeded
            assert all(result.get('success', False) for result in workflow_results)
    
    @pytest.mark.asyncio
    async def test_performance_timing(self):
        """Test performance and timing of operations."""
        import time
        
        async with BiniDesktopIntegration() as bini_desktop:
            
            start_time = time.time()
            
            result = await bini_desktop.validate_screen_with_ai(
                prompt="Quick desktop validation for performance testing"
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            assert result is not None
            assert execution_time < 30  # Should complete within 30 seconds
            print(f"Validation completed in {execution_time:.2f} seconds")


if __name__ == "__main__":
    # Run a simple test
    async def run_simple_test():
        async with BiniDesktopIntegration() as bini_desktop:
            result = await bini_desktop.validate_screen_with_ai(
                "Verify the desktop is functional"
            )
            print(f"Test result: {result}")
    
    asyncio.run(run_simple_test())
