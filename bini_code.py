import openai
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from bini.core.modules.environment import get_dotenv_data


def setup_webdriver():
    """Initialize and return a Selenium Chrome WebDriver."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def take_screenshot_and_test(api_key, url, screenshot_path='screenshot.png'):
    """
    Takes a screenshot of the given webpage and interacts with OpenAI API using provided API key.

    Args:
        api_key (str): Your OpenAI API key.
        url (str): URL to open and test.
        screenshot_path (str): Path to save the screenshot.
    """
    openai.api_key = api_key
    driver = setup_webdriver()

    try:
        # Open the webpage
        driver.get(url)
        time.sleep(2)  # Allow time for the page to load

        # Take a screenshot
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")

        # Test: Check if title contains the word 'Google'
        assert 'Google' in driver.title, "Title does not contain 'Google'"
        print("Test Passed: 'Google' found in the title.")

        # Example API request to OpenAI (for demonstration)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Explain the significance of Selenium WebDriver.",
            max_tokens=50
        )
        print("OpenAI Response:", response.choices[0].text.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


# Usage Example
if __name__ == "__main__":
    api_key = get_dotenv_data(key='API_KEY')  # Replace with your actual API key
    take_screenshot_and_test(api_key, "https://www.google.com")
