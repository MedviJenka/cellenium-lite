from core.engine.driver_engine import DriverEngine


class TestTitle:

    engine = DriverEngine(screen='Google', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'
        self.engine.get_element('search').fill('cats')
