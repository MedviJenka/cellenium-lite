import base64
import requests
from dataclasses import dataclass
from bini.core.agnents.create_agents import GenerateAgents


@dataclass
class Bini(GenerateAgents):

    """
    questions:
        1. do we need a local model?
        2. do we need to train a model? (because at this moment image recognition is working)

    :TODO TASKS:
        1. setup openai azure ............................................... DONE
        2. create agents .................................................... WIP

    :IMPORTANT:
        evaluation: never send and get the data from the user, always make a gateway to a prompt.

    :TODO BUGS:
        1. at this moment there is a token limitation, after 3 tests need to wait for new generation

    """

    endpoint: str
    model: str
    api_key: str
    version: str

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with (open(image_path, "rb") as image_file):
            image = base64.b64encode(image_file.read())
            return image.decode('ascii')  # or utf-8

    def base64_image(self, image_path: str) -> None:
        return self.__encode_image(image_path)

    def image(self, image_path: str, prompt: str) -> str:
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
                            "text": self.execute()
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
                            "text": f'{prompt}'
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 4096
        }

        endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']

            print(f'tokens: {data['usage']['total_tokens']}')
            print(output)
            print(data)
            return output

        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
