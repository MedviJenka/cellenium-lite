from dataclasses import dataclass
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ServiceManager:
    chrome = ChromeDriverManager()
    options: Options = Options()
    service: Service = Service(executable_path=chrome.install())
