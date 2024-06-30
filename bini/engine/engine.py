import base64
import requests
from PIL import Image
from time import time
from dataclasses import dataclass
from requests import Response
from bini.infrastructure.exceptions import BiniResponseError
from bini.infrastructure.logger import Logger


@dataclass
class Bini:

    model: str
    api_key: str
    max_tokens: int
    system_prompt: str

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
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self.base64_image(image_path)}",
                                'details': 'high',
                            }
                        }
                    ]
                }
            ],
            "max_tokens": self.max_tokens
        }

        start_time = time()
        outcome = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        end_time = time()
        self.log_performance(start_time=start_time, end_time=end_time, endpoint=outcome)
        response = outcome.json()['choices'][0]['message']['content']
        price = self.calculate_token_cost(image=image_path, price_per_1000_tokens=0.003, detail='high')

        try:
            return response

        except Exception as e:
            raise BiniResponseError(outcome=outcome, response=response, exception=e)

        finally:
            print(f'PRICE PER IMAGE: {price}$')
            print(response)

    def calculate_token_cost(self, image: str, detail: str, price_per_1000_tokens: float) -> float:

        width = self.__get_image_dimensions(image)[0]
        height = self.__get_image_dimensions(image)[1]

        if detail == "low":
            token_cost = 85

        elif detail == "high":
            # Scale to fit within 2048 x 2048 while maintaining aspect ratio
            if width > 2048 or height > 2048:
                aspect_ratio = width / height
                if aspect_ratio > 1:
                    width = 2048
                    height = int(2048 / aspect_ratio)
                else:
                    height = 2048
                    width = int(2048 * aspect_ratio)

            # Scale such that the shortest side is 768px long
            if width < height:
                scale_factor = 768 / width
            else:
                scale_factor = 768 / height

            width = int(width * scale_factor)
            height = int(height * scale_factor)

            # Calculate the number of 512px squares
            num_squares = (width // 512) * (height // 512)

            # Calculate the total token cost
            token_cost = 170 * num_squares + 85

        else:
            raise ValueError("Invalid detail level. Choose 'low' or 'high'.")

        # Calculate the cost in dollars
        cost_in_dollars = (token_cost / 1000) * price_per_1000_tokens
        return cost_in_dollars

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def __get_image_dimensions(image: str) -> list[int]:
        with Image.open(image) as img:
            width, height = img.size
        return [width, height]
