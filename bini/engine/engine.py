import requests
from typing import Optional
from dataclasses import dataclass
from bini.core.agents.prompt_agent import SetAgent
from bini.engine.azure_config import AzureOpenAIEnvironmentConfig
from bini.engine.functionality import APIRequestHandler
from bini.infrastructure.prompts import Prompts


@dataclass
class Bini(APIRequestHandler):

    model: str
    version: str

    def __post_init__(self) -> None:

        self.config = AzureOpenAIEnvironmentConfig(api_key='OPENAI_API_KEY',
                                                   azure_endpoint='AZURE_OPENAI_ENDPOINT',
                                                   openai_api_version='OPENAI_API_VERSION',
                                                   deployment_name='MODEL')

        """Initializes the Bini class with the correct endpoint."""
        self.endpoint = f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?api-version={self.version}"
        self.agent = SetAgent(config=self.config)

    def enhance_prompt(self, prompt: str) -> str:
        """Enhances given prompt in more professional manner"""
        return self.agent.enhance_given_prompt(prompt)

    def enhance_result(self, prompt: str) -> str:
        """
        :TODO: enhance result with agent
        """

    def image_agent(self, image_path: str, sample_image: str, prompt: str) -> str:
        """
        If sample image provided insert it in the request else, use just one image.
        """
        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(image_path)}"}},
            {"type": "text", "text": self.enhance_prompt(prompt)}
        ]

        if sample_image:
            user_content.insert(__index=1, __object={"type": "sample_image", "image_url": {"url": f"data:image/jpeg;base64,{self.get_image(sample_image)}"}})

        payload = {
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": Prompts.image_visualization_agent}]},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1,
        }

        return self.make_request(payload)

    def run(self, image_path: str, prompt: str, sample_image: Optional[str] = '') -> str:
        """Runs the appropriate agents based on the call_agents flag."""
        try:
            result = self.image_agent(image_path=image_path, sample_image=sample_image, prompt=prompt)
            return self.enhance_prompt(result)

        except FileNotFoundError as e:
            raise e

        except requests.RequestException as e:
            raise e
