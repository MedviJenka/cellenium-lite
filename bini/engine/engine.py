import base64
import requests
from dataclasses import dataclass
from bini.infrastructure.data import IMAGE_VISUALIZATION_PROMPT, VALIDATION_PROMPT, CONCLUSION_PROMPT


@dataclass
class Bini:

    endpoint: str
    model: str
    api_key: str
    version: str

    @staticmethod
    def __encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            image = base64.b64encode(image_file.read())
            return image.decode('ascii')  # or 'utf-8'

    def base64_image(self, image_path: str) -> str:
        return self.__encode_image(image_path)

    def image(self, image_path: str, prompt: str) -> str:

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        # Execute agents and get their results
        # agent_results = self.execute()

        # Payload for the request
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": IMAGE_VISUALIZATION_PROMPT
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
            "temperature": 0.1,
        }

        endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']

            print(f'tokens: {data["usage"]["total_tokens"]}')
            print(output)
            print(data)

            return output

        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

    def main_agent(self, image_path: str, prompt: str) -> None:

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
                            "text": VALIDATION_PROMPT
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.image(image_path=image_path, prompt=prompt)
                        }
                    ]
                },
            ],
            "temperature": 0.1,
        }

        endpoint = "https://openaigpt4audc.openai.azure.com/openai/deployments/bini/chat/completions?api-version=2024-02-15-preview"

        # Send request
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']
            return output
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

    def analyize(self, image_path: str, prompt: str):

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
                            "text": CONCLUSION_PROMPT
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.main_agent(image_path=image_path, prompt=prompt)
                        }
                    ]
                },
            ],
            "temperature": 0.1,
        }

        endpoint = "https://openaigpt4audc.openai.azure.com/openai/deployments/bini/chat/completions?api-version=2024-02-15-preview"

        # Send request
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']
            return output
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")


