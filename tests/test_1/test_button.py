import pytest
from typing import AsyncGenerator
from settings import Logfire
from bini_ai import BiniUtils
from core.engine.driver_engine import DriverEngine


bini = BiniUtils()

log = Logfire(name='test-button')


@pytest.fixture
def engine() -> DriverEngine:
    return DriverEngine(screen='Google', headless=False)


@pytest.fixture(scope='module')
async def lifespan(engine) -> AsyncGenerator:
    log.fire.info('Starting test module setup')
    yield
    engine.teardown()
    log.fire.info('Test module teardown complete')


class TestGoogle:

    def test_web(self, engine) -> None:
        engine.get_web("https://www.google.com")
        title = engine.driver.title
        engine.get_element('search').send_keys('cats')
        engine.get_element('button').click()
        assert title == 'Google'

    def test_cats(self, engine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element('search').send_keys('cats')
        engine.get_element('button').click()
        screenshot = engine.get_screenshot()
        result = bini.run(image_path=screenshot, prompt='what do you see in this image?')
        assert 'Passed' and 'Cats' in result, log.fire.error('cats were not found in page')
