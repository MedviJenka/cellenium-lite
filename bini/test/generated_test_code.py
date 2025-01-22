
import pytest
from qasharedinfra.infra.common.services.bini_ai.infrastructure.exceptions import BiniPromptException
from qasharedinfra.infra.smarttap.selenium.st_selenium_utils import *
from qasharedinfra.infra.smarttap.selenium.utils.azure_table_data.table_query import TablesQuery
from qasharedinfra.infra.smarttap.selenium.utils.bini_utils import IRBiniUtils
from testing.smarttap.interactions_page._core.base_model import BaseModel
from testing.smarttap.version.constants import AZURE_STORAGE_DATA


HEADLESS = True
st = env.devices['Device_1']
logger = env.logger


@pytest.fixture(scope='module', autouse=True)
def init_globals() -> None:
    st.logger_.info('******** Module (Script) Setup ********')
    bini = IRBiniUtils()
    st.test_prerequisites(selenium=True, headless=HEADLESS)
    st.ui.utils.st_selenium_go_to_screen_in_current_window(st.selenium, st.st_screens.help_center)

    yield bini

    logger.info('******** Module (Script) TearDown ********')
    st.selenium.finalize()


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown() -> None:
    st.logger_.info('******** Test Setup ********')

    yield 

    st.logger_.info('******** Test TearDown ********')


@pytest.fixture
def setup() -> None:
    driver = st.selenium


class TestSystemVersion(BaseModel):
    
    def test_otzeau(self, setup) -> None:
        setup.get_mapped_element('button').click(None)
        setup.get_mapped_element('input').inject_text(None)
        setup.get_mapped_element('input').inject_text(None)