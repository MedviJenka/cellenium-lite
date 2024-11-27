from typing import Optional
from dataclasses import dataclass
from selenium import webdriver
from core.infrastructure.manager.service import ServiceManager


@dataclass
class DriverManager(ServiceManager):

    """
    This class extends the `ServiceManager` class and provides a convenient way to initialize and manage
    a Selenium web driver instance.


    :params: driver (webdriver) .................... The Selenium web driver instance.
    :args:
        service (Service) ....................... The service object to use for managing the driver.
                                                     It should be an instance of
                                                     a class that extends the `Service` class from

        headless: .............................. Testing in background with no UI

    """

    headless: Optional[bool] = False

    def __post_init__(self) -> None:
        if self.headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--no-sandbox')

        self.driver: webdriver = webdriver.Chrome(service=self.service, options=self.options)
