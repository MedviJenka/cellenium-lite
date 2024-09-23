==================
     Bini AI
==================


`version: 1.0.1`


Overview
========


Bini class (`Bini`) is a PyBREnv service that processes images using azure openai (Chat GPT)
and allows the user to ask any question regards the image sent.
For example, it can count the number of icons displayed or  if the user is displayed. It also can understand
any metadata information provided such as dates, time, users, whatever you wish.

`Bini` class manages interactions with the Bini OpenAI deployment for processing images and generating responses based on image content.
Bini utilizes Azure OpenAI to process images and respond to user queries about the image content. This includes identifying icons, recognizing users, and interpreting metadata.


Modules
-------
At this moment you have to install the libraries manually till the infra team will fix it.
In your local environment install the next:
One of the AI packages updates a package named 'marshmallow' to the latest version and it leads to Applitools service error, which depends on a lower version.
.. code-block::

     pip install crewai==0.41.1 crewai[tools] langchain langchain-openai python-dotenv marshmallow==2.21.0


Configuration
-------------
Navigate to qasharedinfra/infra/common/services/bini_ai
and paste the .env file that has been sent in email / presentation chat, remove the prefix before the dot to leave it as: .env

* `.env` file is private for data security
* You can get the API key from azure openai `openaigpt4audc`, or alternative deployment

.. code-block::

    AZURE_OPENAI_API = <OpenAI API key>
    ENDPOINT = https://openaigpt4audc.openai.azure.com
    MODEL = bini
    VERSION = 2024-02-15-preview


Create Bini Utils Example
-----------------
Navigate to qasharedinfra/<your product utils> and create bini_utils.py (or any readable name)

* important: do not change .env key names.

.. code-block::

    from qasharedinfra.infra.common.services.bini_ai.engine.engine import Bini
    from qasharedinfra.infra.common.services.bini_ai.core.modules.environment import get_dotenv_data

    class OVOCBiniUtils(Bini):


       """
       A utility class for interacting with the OpenAI API using Azure's infrastructure.


       This class extends the `Bini` class and initialises the necessary attributes such as
       the model, API key, API version, and endpoint by retrieving these values from environment
       variables.


       Attributes:
           model (str): The model to be used with the OpenAI API, retrieved from environment variables.
           api_key (str): The API key for authenticating requests to the OpenAI API, retrieved from environment variables.
           version (str): The version of the OpenAI API to be used, retrieved from environment variables.
           endpoint (str): The Azure endpoint for the OpenAI API, retrieved from environment variables.


       """


       def __init__(self) -> None:
           self.model: str = get_dotenv_data('MODEL')
           self.api_key: str = get_dotenv_data('OPENAI_API_KEY')
           self.version: str = get_dotenv_data('OPENAI_API_VERSION')
           self.endpoint: str = get_dotenv_data('AZURE_OPENAI_ENDPOINT')
           super().__init__(endpoint=self.endpoint, model=self.model, version=self.version)

Congrats!
---------

From this stage you can test with Bini. Navigate to your tasting dir and call Bini  instance.

* Bini should be called as global twice: Once under imports and the second time in init_globals for reusability

* Keep the Try & Except block as it is.


.. code-block::

    import pytest
    from qasharedinfra.infra.common.services.bini_ai.infrastructure.exceptions import BiniPromptException
    from qasharedinfra.infra.ovoc.general.bini_utils import OVOCBiniUtils
    from qasharedinfra.infra.smarttap.selenium.utils.recording_profile_slnm_utils import SmartTap
    from qasharedinfra.infra.smarttap.selenium.st_selenium_utils import *
    from testing.smarttap.interactions_page.core.images import CallIcons

    global bini


    st: SmartTap = env.devices['Device_1']


    @pytest.fixture(scope='module', autouse=True)
    def init_globals() -> None:

       global bini

       st.logger_.info('\n******** Module (Script) Setup ********')
       bini = OVOCBiniUtils()
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


    class TestPlayerIcons:

       """
       Tests if player icons are correctly displayed on the device screen.


       """

       def set_test_icons(self, sample_icon: CallIcons) -> None:


           try:
               sleep(5)
               response = bini.run(image_path=take_screenshot(device=st,  element_name='play_icons_column'),
                                   sample_image=sample_icon,
                                   prompt='test prompt)?')

               assert 'Passed' in response
               assert 'Something you want to validate' in response

           except BiniPromptException as e:
               raise f'bini exception: {e}'


           except WebDriverException as e:
               raise f'base selenium exception: {e}'


           except Exception as e:
               raise e


Pro Tip
-------
For better clarity, when testing a specific field, take a screenshot of the
individual element rather than the entire screen. It will ease on Bini to understand the image thus, generate better results.


And that is it! Happy and enjoyable usage!
Best regards,
Evgeny Petrusenko, Bini Dev.


Future Plans
~~~~~~~~~~~~
* Integrate with Selenium Screenshot functionality
* Adding agents usage for more precise output.


Change Log
~~~~~~~~~~
- v1.0.0 ................. Initial Alpha Release
- v1.0.1 ................. Agents and name refactoring
