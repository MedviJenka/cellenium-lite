import base64
import requests
from PIL import Image
from core.manager.reader import read_json
from dataclasses import dataclass


@dataclass
class Bini:
    api_key: str = read_json('GPT_API', 'key')

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

    def image(self, image: str) -> str:
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
                            "text": "You are an AI assistant that helps people find information."
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
                            "text": "descibe me this image"
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        endpoint = "https://openaigpt4audc.openai.azure.com/openai/deployments/bini-ai/chat/completions?api-version=2024-02-15-preview"

        # Send request
        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        # Handle the response as needed (e.g., print or process)
        data = response.json()
        print(data['choices'][0]['message']['content'])


bini = Bini()
if __name__ == '__main__':
    bini.image(image=r'C:\Users\evgenyp\PycharmProjects\cellenium-lite\bini\core\data\images\img.png')
