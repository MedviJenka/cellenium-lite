import os
import gspread
from functools import lru_cache
from dataclasses import dataclass
from google.oauth2.service_account import Credentials
from core.infrastructure.core.logger import Logger
from core.infrastructure.data.constants import SCOPES
from infrastructure.manager.config_manager import linux_to_windows_path_convert, get_env


log = Logger()


@dataclass
class GoogleAPIAuth:

    sheet_id: str = '1HiBBUWKS_wheb3ANqCGVtOCpZPCFuN3KSae0hZOD0QE'
    credentials: str = None

    def __post_init__(self) -> None:

        # if no linux environment (means there is no container) detected use local windows path
        if os.getenv('CONTAINER', 'false') == 'false':
            self.credentials = linux_to_windows_path_convert('CONTAINER_CREDENTIALS')

        # else, use linux path
        elif os.getenv('CONTAINER', 'true') == 'true':
            self.credentials = get_env(key='LOCAL_CREDENTIALS')

        service_account = Credentials.from_service_account_file(filename=self.credentials, scopes=SCOPES)
        self.client = gspread.authorize(service_account)

    def __hash__(self) -> hash:
        return hash((self.sheet_id, tuple(SCOPES)))

    def get_cached_sheet(self, sheet_name: str) -> gspread.Worksheet:
        return self.get_sheet.worksheet(sheet_name)

    @property
    def get_sheet(self) -> gspread.Spreadsheet:
        return self.client.open_by_key(self.sheet_id)

    @property
    def get_all_sheets(self) -> list[str]:
        return [sheet.title for sheet in self.client.open_by_key(self.sheet_id).worksheets()]


@lru_cache(maxsize=32)  # minimize repetitive API calls
def __read_google_sheet(sheet_name: str, value: str, api: GoogleAPIAuth) -> dict:

    sheet = api.get_cached_sheet(sheet_name)
    all_rows = sheet.get_all_values()
    headers = all_rows[0]

    log.level.info(sheet)
    log.level.info(all_rows)
    log.level.info(headers)

    for row in all_rows[1:]:
        row_dict = dict(zip(headers, row))
        log.level.info(row_dict)
        if row_dict['name'] == value:
            return row_dict

    return {}


def get_row_data(sheet_name: str, value: str, api=GoogleAPIAuth()) -> dict:

    """
    Retrieve a row from a Google Sheet based on a specific value.

    :param sheet_name: Name of the sheet to search.
    :param value: The value to search for in the 'name' column.
    :param api: An instance of GoogleAPIAuth to use for accessing the sheet.
    :return: A dictionary containing the row data or an empty dict if not found.

    """

    return __read_google_sheet(sheet_name, value, api)


def get_name(sheet_name: str, value: str) -> str:
    return get_row_data(sheet_name=sheet_name, value=value)['name']


def get_locator(sheet_name: str, value: str) -> str:
    return get_row_data(sheet_name=sheet_name, value=value)['locator']


def get_type(sheet_name: str, value: str) -> str:
    return get_row_data(sheet_name=sheet_name, value=value)['type']


def get_action(sheet_name: str, value: str) -> str:
    return get_row_data(sheet_name=sheet_name, value=value)['action']


print(get_type('Google', 'button'))
