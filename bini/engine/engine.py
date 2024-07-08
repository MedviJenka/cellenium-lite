import base64
import requests
from typing import Optional
from dataclasses import dataclass
from bini.infrastructure.data import Agents


@dataclass
class Bini(Agents):

    endpoint: str
    model: str
    api_key: str
    version: str
    temperature: float

    def __post_init__(self) -> None:
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

    @staticmethod
    def _encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            image = base64.b64encode(image_file.read())
            return image.decode('ascii')

    @property
    def _headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def _payload(self, agent: str, function: str) -> dict:
        return {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": agent}]},
                {"role": "user", "content": [{"type": "text", "text": function}]},
            ],
            "temperature": self.temperature,
        }

    def base64_image(self, image_path: str) -> str:
        return self._encode_image(image_path)

    def image_agent(self, image_path: str, prompt: str) -> str:
        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": self.image_visualization_agent}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.base64_image(image_path)}"}},
                    {"type": "text", "text": prompt}
                ]}
            ],
            "temperature": self.temperature,
        }

        return self._make_request(payload)

    def main_agent(self, image_path: str, prompt: str) -> str:
        function_output = self.image_agent(image_path=image_path, prompt=prompt)
        payload = self._payload(agent=self.validation_agent, function=function_output)
        return self._make_request(payload)

    def conclusion(self, image_path: str, prompt: str) -> str:
        function_output = self.main_agent(image_path=image_path, prompt=prompt)
        payload = self._payload(agent=self.conclusion_agent, function=function_output)
        return self._make_request(payload)

    def run(self, image_path: str, prompt: str, call_agents: Optional[bool] = False) -> str:
        if call_agents:
            return self.conclusion(image_path=image_path, prompt=prompt)
        return self.image_agent(image_path=image_path, prompt=prompt)

    def _make_request(self, payload: dict) -> str:
        try:
            response = requests.post(url=self.endpoint, headers=self._headers, json=payload)
            response.raise_for_status()
            data = response.json()
            output = data['choices'][0]['message']['content']
            print(f'Tokens: {data["usage"]["total_tokens"]}')
            print(output)
            return output
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
