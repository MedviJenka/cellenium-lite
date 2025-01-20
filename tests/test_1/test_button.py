import pytest
from bini.engine.utils import BiniUtils
from infrastructure.engine.driver_engine import DriverEngine

bini = BiniUtils()


@pytest.fixture
def engine() -> DriverEngine:
    return DriverEngine(screen='Google', headless=False)


class TestGoogle:

    def test_web(self, engine: engine) -> None:
        engine.get_web("https://www.google.com")
        title = engine.driver.title
        engine.get_element('search').send_keys('cats')
        engine.get_element('button').click()
        engine.teardown()
        assert title == 'Google'

    def test_cats(self, engine) -> None:
        engine.get_web("https://www.google.com")
        engine.get_element('search').send_keys('cats')
        engine.get_element('button').click()
        screenshot = engine.get_screenshot()
        result = bini.run(image_path=screenshot, prompt='what do you see in this image?')
        assert 'Passed' and 'Cats' in result
