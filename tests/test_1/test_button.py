from core.engine.driver_engine import DriverEngine


class TestTitle:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='Google', headless=True)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'

    def test_bini(self) -> None:
        self.test_web()
        self.engine.get_element(name='search').fill('cats')
        self.engine.get_element(name='search', prompt='what do you see in this picture?')
        self.engine.take_screenshot(prompt='what do you see in this picture?')


class TestSTLogin:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='ST', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://stngqa.ai-logix.net/ui/login")
        self.engine.get_element('login').click()


class TestCodeGen:

    def setup_method(self) -> None:
        self.engine = DriverEngine(screen='ST', headless=False)

    def test(self) -> None:
        self.engine.codegen('https://www.google.com')
