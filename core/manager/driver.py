from typing import Optional
from dataclasses import dataclass
from playwright.sync_api import sync_playwright


@dataclass
class DriverManager:

    """
    This class provides a convenient way to initialize and manage
    a Playwright browser instance.

    headless: .............................. Testing in background with no UI

    """

    headless: Optional[bool] = True
    play = sync_playwright().start()
    chrome = play.chromium.launch(headless=headless)

    def __post_init__(self) -> None:
        self.driver = self.chrome.new_page()

    def __del__(self) -> None:
        self.chrome.close()
        self.play.stop()
