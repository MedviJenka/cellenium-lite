import base64
import requests
from PIL import Image
from time import time
from dataclasses import dataclass
from requests import Response
from bini.infrastructure.data import PROMPT_1
from bini.infrastructure.exceptions import BiniResponseError
from bini.infrastructure.logger import Logger


@dataclass
class Bini:

    """
    questions:
        1. do we need a local model?
        2. do we need to train a model? (because at this moment image recognition is working)

    :TODO:
        1. setup openai azure
        2. fine tune local module
        3. fine tune cloud module (GPU: 8GB RAM | CPU: 16GB RAM)
        4. make agents

        IMPORTANT:
            evaluation: never send and get the data from the user, always make a gateway to a prompt.

    """

    api_key: str
    max_tokens: int
    system_prompt: str
    endpoint: str

    def __post_init__(self):
        self.log: Logger = Logger()

    def log_performance(self, start_time: float, end_time: float, endpoint: Response) -> callable:
        duration = end_time - start_time
        self.log.level.info(f"Endpoint: {endpoint}, Duration: {duration:.2f} seconds")

    def base64_image(self, image_path: str) -> None:
        return self.__encode_image(image_path)

    def image(self, image_path: str, prompt: str) -> any:

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": self.system_prompt
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self.base64_image(image_path)}"
                            }
                        },
                        {
                          "type": "text",
                          "text": prompt
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": self.max_tokens
        }

        start_time = time()
        outcome = requests.post(url=self.endpoint, headers=headers, json=payload)
        end_time = time()
        self.log_performance(start_time=start_time, end_time=end_time, endpoint=outcome)
        response = outcome.json()

        try:
            print(response)
            return response

        except Exception as e:
            raise BiniResponseError(outcome=outcome, response=response, exception=e)

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def __get_image_dimensions(image: str) -> list[int]:
        with Image.open(image) as img:
            width, height = img.size
        return [width, height]


bini = Bini(api_key="0fb09f54b13949ebbb258a70e14e3f05", max_tokens=10000, system_prompt=PROMPT_1, endpoint="https://openaigpt4audc.openai.azure.com/openai/deployments/bini-ai/chat/completions?api-version=2024-02-15-preview")
if __name__ == '__main__':
    bini.image(r'C:/Users/evgenyp/PycharmProjects/cellenium-lite/bini/core/data/images/img.png', 'describe me what you see')
