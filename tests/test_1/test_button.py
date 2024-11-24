from bini.engine.utils import BiniUtils
from core.engine.driver_engine import DriverEngine


bini = BiniUtils()


class TestTitle:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='Google', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'
        self.engine.get_element(name='lucky').click()

    def test_bini(self) -> None:
        self.test_web()
        self.engine.get_element(name='search').fill('cats')
        self.engine.get_element(name='search').click()
        image = self.engine.take_screenshot()
        result = bini.run(prompt='what do you see in this picture?', image_path=image)
        assert 'Passed' in result


class TestSTLogin:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='ST', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://stngqa.ai-logix.net/ui/login")
        self.engine.get_element('login').click()
