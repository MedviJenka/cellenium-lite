import requests
from typing import Optional
from dataclasses import dataclass, field
from bini.core.agents.prompt_agent import SetAgent
from bini.engine.azure_config import EnvironmentConfig
from bini.infrastructure.prompts import Prompts
from bini.engine.functionality import Functionality
from bini.infrastructure.exceptions import PromptException


config = EnvironmentConfig(api_key='OPENAI_API_KEY',
                           azure_endpoint='AZURE_OPENAI_ENDPOINT',
                           openai_api_version='OPENAI_API_VERSION',
                           deployment_name='MODEL')


@dataclass
class Bini(Functionality):

    model: str
    api_key: str
    version: str
    agent: SetAgent = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the Bini class with the correct endpoint."""
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"
        self.agent = SetAgent(config=config)

    @property
    def prompt_agent(self) -> str:
        """Enhances given prompt in more professional manner"""
        return self.agent.enhance_given_prompt(self.prompt)

    def image_agent(self) -> str:
        """
        If sample image provided insert it in the request else, use just one image.
        """
        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.image_path)}"}},
            {"type": "text", "text": self.prompt_agent}
        ]

        if self.sample_image:
            user_content.insert(__index=1, __object={"type": "sample_image", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(self.sample_image)}"}})

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_agent}]},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1,
        }

        return self._make_request(payload)

    def run(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str:
        """Runs the appropriate agents based on the call_agents flag."""
        try:
            self.params = (image_path, prompt, sample_image)
            return self.image_agent()

        except FileNotFoundError as e:
            raise e
        except requests.RequestException as e:
            raise e

    def image_compare(self, image_path: str, compare_to: str, prompt: Optional[str] = '') -> str:
        """Processes an image with a given prompt using the image visualization agent."""
        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_compare_agent}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(compare_to)}"}},
                    {"type": "text", "text": prompt}
                ]}
            ],
            "temperature": 0.1,
        }
        try:
            return self._make_request(payload)
        except Exception as e:
            raise PromptException(exception=e)
