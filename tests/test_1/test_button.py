from time import sleep
from playwright_refactoring.engine.driver_engine import DriverEngine


class TestTitle:

    engine = DriverEngine(screen='Google', headless=False)

    def test_web(self) -> None:
        self.engine.get_web("https://www.google.com")
        title = self.engine.driver.title()
        assert title == 'Google'
        self.engine.driver.locator('name').click('btnK')
    sleep(4)
