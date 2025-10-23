from typing import Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class DriverManager:

    """
    This class extends the `ServiceManager` class and provides a convenient way to initialize and manage
    a Selenium web driver instance.


    :params: Driver (webdriver) .................... The Selenium web driver instance.
    :args:
        Service (Service) ....................... The service object to use for managing the driver.
                                                     It should be an instance of
                                                     a class that extends the `Service` class from

        Headless: .............................. Testing in background with no UI

    """

    headless: Optional[bool] = False
    options = Options()
    service = Service(ChromeDriverManager().install())

    def __post_init__(self) -> None:
        if self.headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--no-sandbox')

        self.driver: webdriver = webdriver.Chrome(service=self.service, options=self.options)
