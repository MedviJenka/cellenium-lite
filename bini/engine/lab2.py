import base64
import requests
from PIL import Image
from bini.infrastructure.data import PROMPT_1
from core.manager.reader import read_json
from dataclasses import dataclass


@dataclass
class Bini:

    """
    questions:
        1. do we need a local model?
        2. do we need to train a model? (because at this moment image recognition is working)

    :TODO:
        1. setup openai azure ............................................... DONE
        2. fine tune local module
        3. fine tune cloud module (GPU: 8GB RAM | CPU: 16GB RAM)
        4. make agents

        IMPORTANT:
            evaluation: never send and get the data from the user, always make a gateway to a prompt.

    """
    endpoint: str = 'https://openaigpt4audc.openai.azure.com'
    model: str = 'bini-ai'
    api_key: str = read_json('GPT_API', 'key')
    version: str = '2024-02-15-preview'

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('ascii')  # or utf-8

    @staticmethod
    def __get_image_dimensions(image: str) -> list[int]:
        with Image.open(image) as img:
            width, height = img.size
        return [width, height]

    def base64_image(self, image_path: str) -> None:
        return self.__encode_image(image_path)

    def image(self, image: str, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        # Payload for the request
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": PROMPT_1
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self.base64_image(image)}"
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
            "max_tokens": 800
        }

        endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

        # Send request
        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        # Handle the response as needed (e.g., print or process)
        data = response.json()
        print(data['choices'][0]['message']['content'])
        return data


bini = Bini()
if __name__ == '__main__':
    bini.image(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png', prompt='describe me what you see')
