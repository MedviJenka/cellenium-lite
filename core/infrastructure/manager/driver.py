from typing import Optional
from dataclasses import dataclass
from selenium import webdriver
from core.infrastructure.manager.config import get_env
from core.infrastructure.manager.service import ServiceManager
from contextlib import closing
import socket


def find_free_port(start_port: int, end_port: int) -> int:
    for port in range(start_port, end_port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise Exception(f"No free port found in range {start_port}-{end_port}")


devtools_port = find_free_port(int(get_env('PORT')), 9999)


@dataclass
class DriverManager(ServiceManager):

    """
    This class extends the `ServiceManager` class and provides a convenient way to initialize and manage
    a Selenium web driver instance.

    headless: .............................. Testing in background with no UI

    """

    headless: Optional[bool] = True

    def __post_init__(self) -> None:
        if self.headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument(f'--remote-debugging-port={get_env("PORT")}')

        self.driver: webdriver = webdriver.Chrome(service=self.service, options=self.options)