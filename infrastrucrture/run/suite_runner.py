import os
import openpyxl
from typing import Optional
from dataclasses import dataclass
from infrastrucrture.core.executor import Executor
from infrastrucrture.core.logger import Logger
from infrastrucrture.data.contants import TEST_SUITE, REPORTS, TESTS
from infrastrucrture.run.cloud_runner import SuiteRunnerAPI

log = Logger()


@dataclass
class SuiteRunner(Executor):

    """"
    :param: report ........................ generate allure report bool
    :param: workbook ...................... excel screen sheet name
    :param: multiprocessing ............... parallel run
    :param: n ............................. number of parallel tests

    """

    report: bool = False
    workbook: openpyxl.Workbook = openpyxl.load_workbook(TEST_SUITE)
    multiprocessing: Optional[int] = 0
    run_with_google_sheets: Optional[bool] = False

    def execute(self) -> None:

        if self.run_with_google_sheets:
            api = SuiteRunnerAPI()
            api.execute()

        log.level.debug(f'allure report files in: {REPORTS}')

        # gets each sheet title
        for each_sheet_name in [sheet.title for sheet in self.workbook]:

            sheet = self.workbook[each_sheet_name]

            # for each title iterates through all tests
            for row in sheet.iter_rows(min_row=2, min_col=1, values_only=True):
                test_name, action = row[:2]  # was row[0], row[1]

                # runs each test that is marked with 'run'
                if action == 'RUN':
                    path = fr'{os.path.join(TESTS, sheet.title, test_name)} --alluredir={REPORTS}'

                    os.system(fr'py -m pytest {path}')
                    log.level.debug(f'items tested: {test_name}')

        if self.report:
            os.system(fr'allure serve {REPORTS}')
