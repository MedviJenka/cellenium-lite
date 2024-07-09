import base64
import requests
from typing import Optional
from dataclasses import dataclass, field

from bini.core.modules.exceptions import PromptException
from bini.infrastructure.prompts import Agents


@dataclass
class Functionality:

    api_key: str
    temperature: float
    endpoint: str

    @staticmethod
    def _encode_image(image_path: str) -> str:

        """Encodes an image file to a base64 string."""

        with open(image_path, "rb") as image_file:
            image = base64.b64encode(image_file.read())
            return image.decode('ascii')

    def get_image(self, image_path: str) -> str:

        """Returns the base64 encoded string of the image."""

        return self._encode_image(image_path)

    @property
    def _headers(self) -> dict:

        """Returns the headers for the API request."""

        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def _payload(self, agent: str, function: callable) -> dict:

        """Creates the payload for the API request."""

        return {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": agent}]},
                {"role": "user", "content": [{"type": "text", "text": function}]},
            ],
            "temperature": self.temperature,
        }

    def _make_request(self, payload: dict) -> str:

        """Makes the API request and returns the output."""

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


@dataclass
class Bini(Agents, Functionality):

    model: str
    api_key: str
    version: str
    temperature: float
    image_path: str = field(init=False)
    prompt: str = field(init=False)

    def __post_init__(self) -> None:

        """Initializes the Bini class with the correct endpoint."""

        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

    def _set_image_and_prompt(self, image_path: str, prompt: str) -> None:
        """Sets the image path and prompt for the instance."""
        self.image_path = image_path
        self.prompt = prompt

    def image_agent(self) -> str:

        """Processes an image with a given prompt using the image visualization agent."""

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": self.image_visualization_agent}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.image_path)}"}},
                    {"type": "text", "text": self.prompt}
                ]}
            ],
            "temperature": self.temperature,
        }

        return self._make_request(payload)

    def image_validation_agent(self) -> str:

        """Processes the output of the image agent using the validation agent."""

        function_output = self.image_agent()
        payload = self._payload(agent=self.validation_agent, function=function_output)
        return self._make_request(payload)

    def final_validation_agent(self) -> str:

        """Processes the output of the main agent using the conclusion agent."""

        function_output = self.image_validation_agent()
        payload = self._payload(agent=self.conclusion_agent, function=function_output)
        return self._make_request(payload)

    def run(self, image_path: str, prompt: str, call_agents: Optional[bool] = False) -> str:

        """Runs the appropriate agents based on the call_agents flag."""

        self._set_image_and_prompt(image_path=image_path, prompt=prompt)
        if call_agents:
            return self.final_validation_agent()
        else:
            return self.image_agent()

    def image_compare(self, image_path: str, compare_to: str, prompt: Optional[str] = '') -> str:

        """Processes an image with a given prompt using the image visualization agent."""

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": self.image_compare_agent}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(compare_to)}"}},
                    {"type": "text", "text": prompt}
                ]}
            ],
            "temperature": self.temperature,
        }

        try:
            return self._make_request(payload)
        except Exception as e:
            raise PromptException(exception=e)

    def run_with_sample(self, image_path: str, sample: str, prompt: str) -> str:

        """Processes an image with a given prompt using the image visualization agent."""

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": self.image_compare_agent}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(sample)}"}},
                    {"type": "text", "text": prompt},
                ]}
            ],
            "temperature": self.temperature,
        }

        return self._make_request(payload)
