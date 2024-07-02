import base64
import requests
from PIL import Image
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

    endpoint: str
    model: str
    api_key: str
    version: str
    system_prompt: str

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

    def cached_api_key(self) -> str:
        return self.api_key

    def image(self, image_path: str, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.cached_api_key(),
        }

        # Payload for the request
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
        output = data['choices'][0]['message']['content']
        print(output)
        return output
