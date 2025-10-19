import gspread
from settings import Logfire, Config
from functools import lru_cache
from dataclasses import dataclass
from google.oauth2.service_account import Credentials


log = Logfire(name='google-sheet-api')


@dataclass
class GoogleAPIAuth:

    sheet_id: str = Config.GOOGLE_SHEET_ID

    def __post_init__(self) -> None:
        service_account = Credentials.from_service_account_file(filename=Config.GOOGLE_CREDENTIALS, scopes=Config.GOOGLE_SCOPES)
        self.client = gspread.authorize(service_account)

    def __hash__(self) -> hash:
        return hash((self.sheet_id, tuple(Config.GOOGLE_SCOPES)))

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

    log.fire.log_info(sheet)
    log.fire.log_info(all_rows)
    log.fire.log_info(headers)

    for row in all_rows[1:]:
        row_dict = dict(zip(headers, row))
        log.fire.log_info(row_dict)
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
