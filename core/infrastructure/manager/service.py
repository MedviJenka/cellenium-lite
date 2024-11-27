from dataclasses import dataclass
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ServiceManager:

    options: Options = Options()
    service: Service = None

    def __post_init__(self):
        self.service = Service(executable_path=ChromeDriverManager().install())
