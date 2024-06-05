import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH = abstract_dir.split('infrastructure')[0][:-1]
TESTS = fr'{GLOBAL_PATH}\tests'
LOGS = fr'{GLOBAL_PATH}\logs\data.log'
TEST_SUITE = fr'{TESTS}\_data\test_suite.xlsx'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# CONFIG = fr'{GLOBAL_PATH}\config.ini'


# ---------------- [ ADD CREDENTIALS PATH FROM GOOGLE GCP ] ---------------------

GOOGLE_SHEET_JSON = "/app/environment/_json/credentials.json"

# ---------------- [ IMPORTANT: add this file to git ignore ] -------------------


class Authorization:

    TENANT_ID = ""
    TOKEN = ""
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": TOKEN
    }
