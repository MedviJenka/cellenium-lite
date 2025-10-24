import asyncio
import pytest
from typing import Generator
from core.bini.backend.ai.flows.bini import bini_image
from pydantic import BaseModel, Field
from core.engine.driver_engine import DriverEngine
from settings import Logfire


log = Logfire('test-ui')

HEADLESS = True


class ReflectionOutputSchema(BaseModel):
    is_response_ok: bool
    fixed_prompt: str
    chain_of_thought: str
    final_decision: str = Field(description='passed or failed')


@pytest.fixture(scope='module')
def driver() -> Generator[DriverEngine, None, None]:
    engine = DriverEngine(screen='Heroku', headless=HEADLESS)
    log.fire.info('Browser launched')
    engine.get_web(web_link="https://the-internet.herokuapp.com/login")
    yield engine
    engine.driver.quit()
    log.fire.info('Browser closed')


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, driver: DriverEngine):
        self.engine = driver

    @pytest.mark.parametrize(
        "username,password,prompt,expected",
        [
            ("username", "123456", "is login button displayed?", "Passed"),
            ("username", "123456", "is a cat displayed", "Failed"),
        ],
    )
    def test_login_flow(self, username, password, prompt, expected):
        self.engine.get_element("username_field").send_keys(username)
        self.engine.get_element("password_field").send_keys(password)
        self.engine.get_element("submit").click()
        image = self.engine.get_screenshot()
        result = asyncio.run(bini_image(prompt=prompt, image=image, chain_of_thought=True, schema=ReflectionOutputSchema))
        final_decision = result.get("final_decision")
        assert final_decision == expected, f"For prompt='{prompt}', got {final_decision}, expected {expected}"
