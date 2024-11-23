from bini.engine.utils import BiniUtils
from core.engine.driver_engine import DriverEngine


class TestTitle:

    bini = BiniUtils()

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='Google', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'

    def test_bini(self) -> None:
        self.test_web()
        self.engine.get_element(name='search').fill('cats')
        image = self.engine.take_screenshot()
        result = self.bini.run(prompt='what do you see in this picture?', image_path=image)
        assert 'Passed' in result


class TestSTLogin:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='ST', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://stngqa.ai-logix.net/ui/login")
        self.engine.get_element('login').click()
