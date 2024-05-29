import warnings
from os import system
from typing import Optional
from selenium import webdriver
from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from infrastructure.core.logger import Logger
from infrastructure.core.reader import get_name, get_locator, get_type
from infrastructure.data.enums import Type
from infrastructure.manager.driver_manager import DriverManager


warnings.filterwarnings('ignore')
log = Logger()


@dataclass
class DriverEngine(DriverManager):

    screen: Optional[str] = None

    def get_web(self, web_link: str, maximize_window=True) -> None:

        self.driver.get(web_link)
        log.level.info(f'webdriver used: \n{self.driver} \n started: \n {web_link}')

        if maximize_window:
            self.driver.maximize_window()

    def get_element(self, name: str, seconds=10) -> webdriver:

        self.driver.implicitly_wait(seconds)
        element_name, element_type, element_locator = self.__get_element_properties(sheet_name=self.screen, value=name)
        output = f'element name: {element_name} | elements locator: {element_locator} | element type: {element_type}'

        try:
            if element_type in Type.__members__:
                log.level.info(output)
                return self.driver.find_element(Type[element_type].value, element_locator)

        except Exception as e:
            # self.attach_screenshot()
            raise e

    @staticmethod
    def __get_element_properties(**kwargs) -> tuple:
        element_name = get_name(**kwargs)
        element_locator = get_locator(**kwargs)
        element_type = get_type(**kwargs)
        return element_name, element_locator, element_type

    def get_dynamic_element(self, attribute: str, name: str, seconds=10) -> webdriver:

        # explanation ............ //*[contains(@<attribute>, <name>)]
        # example ................ //*[contains(@name, "btnK")]

        self.driver.implicitly_wait(seconds)
        element_locator = get_locator(self.screen, name)
        element_type = get_type(self.screen, name)
        path = f"//*[contains(@{attribute}, '{element_locator}')]"

        match element_type:

            case 'DYNAMIC':
                try:
                    return self.driver.find_elements(By.XPATH, path)[0]

                except Exception as e:
                    raise e

    def wait_for_element(self, name: str, seconds=5) -> callable:
        element_locator = get_locator(self.screen, name)
        wait = WebDriverWait(self.driver, seconds)
        return wait.until(expected_conditions.visibility_of_element_located(('', element_locator)))

    def dropdown(self, by: By, locator: str) -> webdriver:
        select = Select(self.driver.find_element(by, get_locator(self.screen, locator)))
        return select.select_by_visible_text(locator)

    def count_elements(self, name: str, tag: str, selector: Type) -> int:

        """
        :param: name ............... name is retrieved from get_element()
        :param: tag ................ div, tr, etc... type it as it is
        :param: selector ........... inherits By class
        """

        table = self.get_element(name)
        rows = len(table.find_elements(selector, f'.//{tag}'))
        print(fr'number of rows in this page is: {rows}')
        return rows

    def press_keyboard_key(self, key: str, hold=False) -> ActionChains | None:
        action = ActionChains(self.driver)
        press = action.key_down(Keys.CONTROL).send_keys(key).key_up(Keys.CONTROL)
        if hold:
            press = action.key_down(Keys.CONTROL + 'T').send_keys(key).key_up(Keys.CONTROL)
            return press.perform()
        return press.perform()

    def scroll_page(self, direction: str, px: int) -> None:

        """
        :param: px ................ pixels
        :param: up or down

        """

        # screen_height: int = self.driver.execute_script("return window.innerHeight")

        match direction:
            case "up":
                self.driver.execute_script(f"window.scrollBy(0, {-px});")

            case "down":
                self.driver.execute_script(f"window.scrollBy(0, {px});")

    def switch_to_new_tab(self, url: str) -> None:
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'T')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        return self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_main_tab(self) -> None:
        window_handles = self.driver.window_handles
        return self.driver.switch_to.window(window_handles[0])

    def handle_basic_auth(self, username: str, password: str) -> None:
        url = f"{username}:{password}@{self.driver.current_url}"
        self.driver.get(url)

    def count_rows(self, name: str, structure: str) -> int:

        """
        :param name .................. element name
        :param structure ............. div, tr, etc..
        :return:  integer
        """

        locator = get_locator(self.screen, name)
        table = self.driver.find_element(Type.XPATH, locator)
        rows = table.find_elements(By.XPATH, structure)
        return len(rows)

    def teardown(self) -> None:

        try:
            self.driver.close()
            self.driver.quit()

        except self.driver is None:
            system("taskkill /f /im chromedriver.exe")
            system("taskkill /f /im chrome.exe")
            raise Exception("driver's N/A")
