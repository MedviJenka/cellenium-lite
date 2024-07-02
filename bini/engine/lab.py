import requests
import base64
from dataclasses import dataclass
from bini.infrastructure.data import PROMPT_1
from core.manager.reader import read_json


@dataclass
class Bini:

    """
    questions:
        1. do we need a local model?
        2. do we need to train a model? (because at this moment image recognition is working)

    :TODO:
        1. setup openai azure ............................................. WIP
        2. fine tune local module
        3. fine tune cloud module (GPU: 8GB RAM | CPU: 16GB RAM)
        4. make agents

        IMPORTANT:
            evaluation: never send and get the data from the user, always make a gateway to a prompt.

    """

    api_key: str = read_json(env_key='GPT_API', json_key='key')
    endpoint: str = "https://openaiforaudc.openai.azure.com/"
    max_tokens: int = 10000
    system_prompt: str = PROMPT_1
    deployment_name: str = 'gpt-4o-automation'
    version: str = '2024-05-01-preview'

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def base64_image(self, image_path: str) -> base64:
        return self.__encode_image(image_path)

    def image(self, image: str) -> None:

        endpoint = f"{self.endpoint}/openai/deployments/{self.deployment_name}/completions?api-version={self.version}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.deployment_name,
            "messages": [
                {
                    "role": "system",
                    "content": 'hi'
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": PROMPT_1
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self.base64_image(image_path=image)}",
                                'details': 'high',
                            }
                        }
                    ]
                }
            ],
            "max_tokens": self.max_tokens,
            "extensions": {
                "name": "image-analysis",
                "parameters": {
                    "image_quality": "high"
                }
            },
        }

        try:
            outcome = requests.post(url=endpoint, headers=headers, json=payload)
            response = outcome.json()

        except requests.RequestException as e:
            raise SystemExit(f'failed to make request {e}')

        print(response)


bini = Bini()
if __name__ == '__main__':
    bini.image(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png')
