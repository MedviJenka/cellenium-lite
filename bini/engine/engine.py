import requests
from typing import Optional
from bini.core.agents.prompt_agent import SetAgent
from bini.engine.base_model import BiniBaseModel
from bini.engine.request_handler import APIRequestHandler
from bini.infrastructure.colors import TerminalColors
from bini.infrastructure.prompts import Prompts
from infrastructure.codegen import BrowserRecorder


class Bini(BiniBaseModel, APIRequestHandler):

    """
    A class to manage interactions with the Bini OpenAI deployment.
    :param: model The model name for the OpenAI deployment.
    :param: api_key (str): The API key for accessing the OpenAI service.
    :param: version (str): The version of the OpenAI API to use.
    :param: endpoint (str): final azure openai endpoint

    """

    def __init__(self, model: str, version: str, endpoint: str, api_key: str) -> None:
        self.__set_agent = SetAgent()
        self.session = requests.Session()
        self.browser_recorder = BrowserRecorder(screen='https://irqa.ai-logix.net')
        BiniBaseModel.__init__(self, model=model, version=version, endpoint=endpoint, api_key=api_key)

    def switch_model(self, model: str, version: str) -> None:
        self.model = model
        self.version = version

    def prompt_agent(self, prompt: str) -> str:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.enhance_prompt(prompt)

    def result_agent(self, result: str) -> str:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.validate_result(result)

    def __friendly_message_output(self, output: str) -> None:

        colors = TerminalColors()
        message = output.split('Final result:')[0]
        result = output.split('Final result:')[1]

        if 'Failed' in result:
            result = f"{colors.RED}Result: {result}"
        else:
            result = f"{colors.GREEN}Result: {result}"

        final = f"""       
        {colors.CYAN}
        ✅ AI Successfully generated
        ✅ Model: {self.model}
        ✅ Version: {self.version}
        ✅ Output:
        {colors.YELLOW}
        {message}
        {result}           
        """

        print(final)

    def run_image_processing(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str:

        """
        Sends request to the image visualization engine.
        If self.sample_image is provided, it will include the sample image in the payload.
        :return: Image processing output as a string.

        """

        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
            {"type": "text", "text": self.prompt_agent(prompt=prompt)}  # self.prompt for prompt without agent
        ]

        if sample_image:
            user_content.append({"type": "sample_image", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(sample_image)}"}})

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_prompt}]},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0,
        }

        return self.make_request_with_retry(payload=payload)

    def run(self, image_path: str or callable, prompt: str, sample_image: Optional[str] = '') -> str:

        """
        Runs Bini module using image path and sample image as an optional reference
        """

        try:
            result = self.run_image_processing(image_path=image_path, sample_image=sample_image, prompt=prompt)
            self.__friendly_message_output(output=result)
            return self.__set_agent.validate_result(result)

        except FileNotFoundError as e:
            raise f'⚠ File: {image_path} cannot be found, exception: {e} ⚠'

        except requests.RequestException as e:
            raise f'⚠ Failed to send rest request, status code: {e} ⚠'

    def get_browser_recorder_list(self) -> list:
        interaction_list = self.browser_recorder.execute()
        tags = [interaction[0] for interaction in interaction_list]
        return tags

    def bini_code(self) -> None:

        """
        Generates a Python test file based on the provided interaction list.
        :param interaction_list: List of interactions [[tagname, id, path], ...].
        """
        l = self.get_browser_recorder_list()
        user_content = [
            {"type": "text", "text": self.prompt_agent(prompt='you are the perfect code generator')}
        ]

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.code_agent_prompt}]},
                {"role": "user", "content": f'{user_content}\n{l}'}
            ],
            "temperature": 0,
        }
        output = self.make_request(payload=payload)

        print(f"Test code successfully written to {output}")
