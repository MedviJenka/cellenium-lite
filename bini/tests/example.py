import pytest
from qasharedinfra.infra.common.services.bini_ai.infrastructure.exceptions import BiniPromptException
from qasharedinfra.infra.mi.db.mi_data_db import MIDataDB
from qasharedinfra.infra.smarttap.selenium.utils.bini_utils import IRBiniUtils
from qasharedinfra.infra.smarttap.selenium.utils.calls_generator.generate_calls_types import make_peer_to_peer_call
from qasharedinfra.infra.smarttap.selenium.utils.calls_generator.smarttap_participants import STParticipant
from qasharedinfra.infra.smarttap.selenium.utils.recording_profile_slnm_utils import SmartTap
from qasharedinfra.infra.smarttap.selenium.st_selenium_utils import *
from testing.smarttap.interactions_page.core.images import InteractionsSamples


global bini


st: SmartTap = env.devices['Device_1']


def generate_p2p_5_min_call(caller: str, callee: str) -> None:
    """
    :TODO: make a call and ask shirel about the commented function

    """

    caller = STParticipant(st.get_user(caller),
                           audio_path=MIDataDB.Attachments.teams_ez_audio_2_speakers_5min_Speaker_01)
    callee = STParticipant(st.get_user(callee),
                           audio_path=MIDataDB.Attachments.teams_ez_audio_2_speakers_5min_Speaker_01)

    try:
        st.logger_.info('----------- Generating ST call ------------')
        make_peer_to_peer_call(caller=caller, callee=callee)

    except Exception as e:
        st.logger_.error(e)
        # raise CallGenerationException(caller=caller, callee=callee, error_message=e)


@pytest.fixture(scope='module', autouse=True)
def init_globals() -> None:

    global bini

    st.logger_.info('\n******** Module (Script) Setup ********')
    bini = IRBiniUtils()

    try:
        ...
        # generate_p2p_5_min_call(caller='st_user4', callee='st_user3')

    finally:
        ...

    st.test_prerequisites(selenium=True, headless=True)
    st.ui.utils.st_selenium_go_to_screen_in_current_window(st.selenium, st.st_screens.interactions)

    yield

    logger.info('******** Module (Script) TearDown ********')
    st.selenium.finalize()


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown() -> None:
    st.logger_.info('******** Test Setup ********')

    yield

    st.logger_.info('******** Test TearDown ********')


class TestInteractionsPageWithBini:

    """
    A test class for verifying interactions on a page using Bini.

    Methods:
        test_ui_header() -> None:
            Tests the UI header by comparing a sample image with an actual screenshot of the screen using Bini.

    """

    def test_ui_header(self) -> None:

        """
        Tests the UI header by comparing a sample image with an actual screenshot of the screen using Bini.

        This method captures a screenshot using the `take_screenshot` function, and then uses Bini to compare
        the captured screenshot with a provided sample image. It asserts that the comparison passes.

        Raises:
            BiniPromptException: If an exception occurs when running Bini with the prompt.
            WebDriverException: If a Selenium-related exception occurs.
            Exception: If a general exception occurs during the process.

        """

        global bini

        try:
            response = bini.run(image_path=take_screenshot(device=st),  # or path to an existing screenshot
                                sample_image=InteractionsSamples.SAVE_SEARCH,
                                prompt='is the sample image provided equals to actual screen?')
            assert 'Passed' in response

        except BiniPromptException as e:
            raise f'bini exception: {e}'

        except WebDriverException as e:
            raise f'base selenium exception: {e}'

        except Exception as e:
            raise f'general exception: {e}'
