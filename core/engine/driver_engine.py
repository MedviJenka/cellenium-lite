import uuid
import warnings
from typing import Optional
from dataclasses import dataclass
from bini.infrastructure.ai_utils import IRBiniUtils
from core.data.constants import IMAGES
from core.modules.logger import Logger
from core.engine.api_engine import get_name, get_locator, get_type
from core.manager.driver import DriverManager


warnings.filterwarnings('ignore')
log = Logger()


@dataclass
class DriverEngine(DriverManager):

    screen: Optional[str] = None

    def get_web(self, url: str) -> None:
        self.driver.goto(url)

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

    def take_screenshot(self, name: Optional[str] = None, prompt: Optional[str] = None) -> None:

        bini = IRBiniUtils()
        image = fr'{IMAGES}\{name}.png'

        if prompt:
            print(f'image path: {image}')
            self.driver.screenshot(path=image)
            bini.run(image_path=image, prompt=prompt)
            if name is not None:
                image = fr'{IMAGES}\{name}.png'
            else:
                image = fr'{IMAGES}\{self.__random_id}.png'
        self.driver.screenshot(path=image)

    @property
    def __random_id(self) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def __get_element_properties(**kwargs) -> tuple:
        element_name = get_name(**kwargs)
        element_locator = get_locator(**kwargs)
        element_type = get_type(**kwargs)
        return element_name, element_type, element_locator,
