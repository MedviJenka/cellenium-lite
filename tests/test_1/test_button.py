from bini.engine.utils import BiniUtils
from core.infrastructure.engine.driver_engine import DriverEngine


bini = BiniUtils()


class TestGoogle:

    engine = DriverEngine(screen='Google', headless=True)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title
        self.engine.get_element('search').send_keys('cats')
        self.engine.get_element('button').click()
        self.engine.teardown()
        assert title == 'Google'

    def test_cats(self) -> None:
        self.engine.get_web("https://www.google.com")
        self.engine.get_element('search').send_keys('cats')
        self.engine.get_element('button').click()
        screenshot = self.engine.get_screenshot()
        result = bini.run(image_path=screenshot, prompt='what do you see in this image?')
        assert 'Passed' and 'Cats' in result
