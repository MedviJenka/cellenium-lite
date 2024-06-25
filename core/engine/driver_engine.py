import warnings
from datetime import datetime
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

    screen: Optional[str] = None

    def get_web(self, web_link: str) -> None:

        self.driver.goto(web_link)
        log.level.info(f'webdriver used: \n{self.driver} \n started: \n {web_link}')

    def get_element(self, name: str, screenshot: Optional[bool] = False) -> any:

        element_name, element_type, element_locator = self.__get_element_properties(sheet_name=self.screen, value=name)
        output = f'element name: {element_name} | elements locator: {element_locator} | element type: {element_type}'
        screenshot_path = fr'{IMAGES}/{name}.png'

        try:
            log.level.info(output)
            if screenshot:
                self.driver.locator(f'[{element_locator}={element_type}]').screenshot(path=f'{screenshot_path}')
                log.level.info(f'screen shot success: {screenshot_path}')
            return self.driver.locator(f'[{element_locator}={element_type}]')

        except Exception as e:
            raise e

    def take_screenshot(self, name: Optional[str] = None) -> None:

        now = datetime.now()
        time = now.strftime('%d%m%Y%H%M')
        image_path = fr'{IMAGES}/{time}.png'
        self.driver.screenshot(path=image_path)

        if name:
            self.driver.screenshot(path=fr'{IMAGES}/{name}.png')

    @staticmethod
    def __get_element_properties(**kwargs) -> tuple:
        element_name = get_name(**kwargs)
        element_locator = get_locator(**kwargs)
        element_type = get_type(**kwargs)
        return element_name, element_type, element_locator,
