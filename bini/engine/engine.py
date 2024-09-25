import requests
from typing import Optional
from bini.core.agents.prompt_agent import SetAgent
from bini.engine.factory import BiniFactory
from bini.engine.request_handler import APIRequestHandler
from bini.infrastructure.prompts import Prompts


class Bini(BiniFactory, APIRequestHandler):

    """
    A class to manage interactions with the Bini OpenAI deployment.
    :param: model The model name for the OpenAI deployment.
    :param: api_key (str): The API key for accessing the OpenAI service.
    :param: version (str): The version of the OpenAI API to use.
    :param: endpoint (str): final azure openai endpoint

    """

    def __init__(self, model: str, version: str, endpoint: str) -> None:
        self.session = requests.Session()
        self.__set_agent = SetAgent()
        BiniFactory.__init__(self, model=model, version=version, endpoint=endpoint)

    def prompt_agent(self, prompt: str) -> str:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.enhance_prompt(prompt)

    def result_agent(self, result: str) -> str:
        """Enhances given prompt in more professional manner"""
        return self.__set_agent.validate_result(result)

    def run_image_processing(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str:

        """
        Sends a request to the image visualization engine.
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

        return self.make_request(payload)

    def run(self, image_path: str or callable, prompt: str, sample_image: Optional[str] = '') -> str or list:

        """
        Runs Bini module using image path and sample image as an optional reference
        """

        try:
            result = self.run_image_processing(image_path=image_path, sample_image=sample_image, prompt=prompt)
            return self.__set_agent.validate_result(result)

        except FileNotFoundError as e:
            raise f'File: {image_path} cannot be found, exception: {e}'

        except requests.RequestException as e:
            raise f'Failed to send rest request, status code: {e}'
