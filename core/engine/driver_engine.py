import warnings
from typing import Optional
from dataclasses import dataclass
from core.modules.logger import Logger
from core.engine.api_engine import get_name, get_locator, get_type
from core.manager.driver import DriverManager


warnings.filterwarnings('ignore')
log = Logger()


@dataclass
class DriverEngine(DriverManager):

    screen: Optional[str] = None

    def get_web(self, web_link: str) -> None:

        self.driver.goto(web_link)
        log.level.info(f'webdriver used: \n{self.driver} \n started: \n {web_link}')

    def get_element(self, name: str) -> any:

        element_name, element_type, element_locator = self.__get_element_properties(sheet_name=self.screen, value=name)
        output = f'element name: {element_name} | elements locator: {element_locator} | element type: {element_type}'

        try:
            log.level.info(output)
            return self.driver.locator(f'[{element_locator}={element_type}]')

        except Exception as e:
            raise e

    def get_screenshot(self, path: str) -> None:
        self.driver.screenshot(path=f'{path}.png')

    @staticmethod
    def __get_element_properties(**kwargs) -> tuple:
        element_name = get_name(**kwargs)
        element_locator = get_locator(**kwargs)
        element_type = get_type(**kwargs)
        return element_name, element_type, element_locator,
