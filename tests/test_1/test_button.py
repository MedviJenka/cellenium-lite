from core.engine.driver_engine import DriverEngine


class TestTitle:

    engine = DriverEngine(screen='Google')

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'
        self.engine.get_element(name='search').fill('cats')
        self.engine.get_element(name='search', screenshot=True)
        self.engine.take_screenshot(prompt='what do you see in this picture?')


class TestSTLogin:

    engine = DriverEngine(screen='ST', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://stngqa.ai-logix.net/ui/login")
        self.engine.get_element('login').click()
