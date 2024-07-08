import base64
import requests
from dataclasses import dataclass
from bini.infrastructure.data import Agents


@dataclass
class Bini(Agents):

    endpoint: str
    model: str
    api_key: str
    version: str
    temperature: float

    def __post_init__(self):
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

    @staticmethod
    def __encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            image = base64.b64encode(image_file.read())
            return image.decode('ascii')

    @property
    def __headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        return headers

    def __payload(self, agent: str, function: callable or str) -> dict:

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": agent
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": function
                        }
                    ]
                },
            ],
            "temperature": self.temperature,
        }

        return payload

    def base64_image(self, image_path: str) -> str:
        return self.__encode_image(image_path)

    def image_agent(self, image_path: str, prompt: str) -> str:

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": self.image_visualization_agent
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
            "temperature": self.temperature,
        }

        try:
            response = requests.post(url=self.endpoint, headers=self.__headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']

            print(f'tokens: {data["usage"]["total_tokens"]}')
            print(output)
            print(data)

            return output

        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

    def main_agent(self, image_path: str, prompt: str) -> None:

        payload = self.__payload(agent=self.validation_agent, function=self.image_agent(image_path=image_path, prompt=prompt))

        try:
            response = requests.post(self.endpoint, headers=self.__headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']
            print(f'main agent output: {output}')
            return output

        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

    def analyze(self, image_path: str, prompt: str):

        payload = self.__payload(agent=self.conclusion_agent, function=self.main_agent(image_path=image_path, prompt=prompt))

        try:
            response = requests.post(self.endpoint, headers=self.__headers, json=payload)
            data = response.json()
            output = data['choices'][0]['message']['content']
            print(f'analyze agent output: {output}')
            return output
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
