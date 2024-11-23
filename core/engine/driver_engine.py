import uuid
import warnings
from typing import Optional
from dataclasses import dataclass
from core.data.constants import IMAGES
from core.modules.logger import Logger
from core.engine.api_engine import get_name, get_locator, get_type
from core.manager.driver import DriverManager


warnings.filterwarnings('ignore')
log = Logger()


@dataclass
class DriverEngine(DriverManager):

    headless: bool = False
    screen: Optional[str] = None

    def __post_init__(self):
        super().__init__(headless=self.headless)

    def get_web(self, url: str) -> None:
        self.driver.goto(url)

    def get_element(self, name: str) -> any:

        element_name, element_type, element_locator = self.__get_element_properties(sheet_name=self.screen, value=name)
        output = f'element name: {element_name} | elements locator: {element_locator} | element type: {element_type}'
        screenshot_path = fr'{IMAGES}/{name}.png'

        try:
            log.level.info(output)
            log.level.info(f'screen shot success: {screenshot_path}')
            self.take_screenshot(name=name)
            return self.driver.locator(f'[{element_locator}={element_type}]')

        except Exception as e:
            raise e

    def get_dynamic_element(self, name: str):

        element_name, element_type, element_locator = self.__get_element_properties(sheet_name=self.screen, value=name)
        dynamic_selector = f"[{element_locator}*='{element_type}']"
        log.level.info(f"Using dynamic selector: {dynamic_selector}")
        element = self.driver.locator(dynamic_selector)

        if element.count() == 0:
            raise Exception(f"Dynamic element with locator {dynamic_selector} not found")
        else:
            log.level.info(f"Dynamic element found: {element.nth(0).inner_text()}")
            return element.nth(0)

    def take_screenshot(self, name: Optional[str] = None) -> str:

        image = fr'{IMAGES}\{name}.png'
        self.driver.screenshot(path=image)
        if name is not None:
            image = fr'{IMAGES}\{name}.png'
        else:
            image = fr'{IMAGES}\{self.__random_id}.png'
        self.driver.screenshot(path=image)
        return image

    @property
    def __random_id(self) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def __get_element_properties(**kwargs) -> tuple:
        element_name = get_name(**kwargs)
        element_locator = get_locator(**kwargs)
        element_type = get_type(**kwargs)
        return element_name, element_type, element_locator,
