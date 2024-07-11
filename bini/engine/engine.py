import requests
from typing import Optional
from dataclasses import dataclass
from bini.infrastructure.prompts import Agents
from bini.engine.functionality import Functionality
from bini.core.modules.exceptions import PromptException


@dataclass
class Bini(Agents, Functionality):

    model: str
    api_key: str
    version: str
    temperature: float

    def __post_init__(self) -> None:
        """Initializes the Bini class with the correct endpoint."""
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"

    def image_agent(self) -> str:

        """
        If sample image provided insert it in the request
        Else, use just one image.
        """

        if self.sample_image:
            payload = {
                "messages": [
                    {"role": "system", "content": [{"type": "text", "text": self.image_visualization_agent}]},
                    {"role": "user", "content": [
                        {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.image_path)}"}},
                        {"type": "sample_image","image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.sample_image)}"}},
                        {"type": "text", "text": self.prompt}
                    ]}
                ],
                "temperature": self.temperature,
            }

        else:
            payload = {
                "messages": [
                    {"role": "system", "content": [{"type": "text", "text": self.image_visualization_agent}]},
                    {"role": "user", "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.image_path)}"}},
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

    def run(self, image_path: str, prompt: str, call_agents: Optional[bool] = False, sample_image: Optional[str] = '') -> str:
        """Runs the appropriate agents based on the call_agents flag."""
        try:
            self.params = (image_path, prompt, sample_image)
            if call_agents:
                return self.final_validation_agent()
            else:
                return self.image_agent()
        except FileNotFoundError as e:
            raise e
        except requests.RequestException as e:
            raise e

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
