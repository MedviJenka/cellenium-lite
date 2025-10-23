import asyncio
import pytest
from typing import Generator
from core.bini.backend.ai.agents.reflection_agent.schemas import ReflectionOutputSchema
from core.bini.backend.ai.flows.bini import bini_image
from core.engine.driver_engine import DriverEngine
from settings import Logfire


log = Logfire('test-ui')

HEADLESS = True


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

    @pytest.mark.parametrize('username', ['username'])
    @pytest.mark.parametrize('password', ['123456'])
    def test_login_flow(self, username: str, password: str) -> None:
        """Elements are mapped from Google Sheets"""
        self.engine.get_element('username_field').send_keys(username)
        self.engine.get_element('password_field').send_keys(password)
        self.engine.get_element('submit').click()
        image = self.engine.get_screenshot()
        result = asyncio.run(bini_image(prompt="login button displayed?",
                                        image=image,
                                        chain_of_thought=True,
                                        schema=ReflectionOutputSchema))
        assert 'Passed' in result
