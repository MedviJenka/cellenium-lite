from typing import Generator
import pytest
from infrastructure.engine.driver_engine import DriverEngine
from settings import Logfire

log = Logfire('test-web')


@pytest.fixture(scope='module')
def driver() -> Generator[DriverEngine, None, None]:
    engine = DriverEngine(screen='Heroku', headless=False)
    log.fire.info('Browser launched')
    yield engine
    engine.driver.quit()
    log.fire.info('Browser closed')


class TestLogin:

    screen = "https://the-internet.herokuapp.com/login"

    @pytest.fixture(autouse=True)
    def setup(self, driver: DriverEngine):
        self.engine = driver

    @pytest.mark.parametrize('username', ['wrong', 'tomsmith'])
    @pytest.mark.parametrize('password', ['wrong', 'SuperSecretPassword'])
    def test_login_flow(self, username: str, password: str) -> None:
        """Elements are mapped from Google Sheets"""
        self.engine.get_web(self.screen)
        self.engine.get_element('username_field').send_keys(username)
        self.engine.get_element('password_field').send_keys(password)
        self.engine.get_element('submit').click()
