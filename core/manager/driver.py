from typing import Optional
from playwright.sync_api import sync_playwright
from dataclasses import dataclass


@dataclass
class DriverManager:

    """
    This class provides a convenient way to initialize and manage
    a Playwright browser instance.

    headless: .............................. Testing in background with no UI
    """

    headless: Optional[bool] = False
    play = sync_playwright().start()
    chrome = play.chromium.launch(headless=headless)
    driver = chrome.new_page()

    def __del__(self) -> None:
        self.chrome.close()
        self.play.stop()
