import os

# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH = abstract_dir.split('core')[0][:-1]
TESTS = fr'{GLOBAL_PATH}\tests'
CONFIG_PATH = fr'{GLOBAL_PATH}\core\static\utils\config.ini'
TEST_LIST = fr'{GLOBAL_PATH}\core\utils\data\test_list.json'
SCREENSHOTS = fr'{GLOBAL_PATH}\core\utils\data\screenshots\reports'
JENKINS = fr'{GLOBAL_PATH}\jenkins\jenkins.war'
LOGS = fr'{TESTS}\_data\logs\logs.log'
REPORTS = fr'{TESTS}\_reports'
PAGE_BASE = fr'{TESTS}\_data\page_base.xlsx'
TEST_SUITE = fr'{TESTS}\_data\test_suite.xlsx'
PLAYER_DATA = fr'{GLOBAL_PATH}\app\player\data.json'
IMAGE_COMPARE_DATA = fr'{GLOBAL_PATH}\core\tools\image_compare\data.json'
COOKIES = fr'{GLOBAL_PATH}\core\infrastructure\constants\data\cookies.json'
GOOGLE_SHEET_JSON = r'C:\Users\evgenyp\Downloads\cellenium-screen-e7288379b0b7.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class Authorization:

    """
    :TODO: check in wireshark both postman and python requests and see the differences

    """

    TENANT_ID = ""
    TOKEN = ""
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": TOKEN
    }
