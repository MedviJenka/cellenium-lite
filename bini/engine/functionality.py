import base64
import requests
from dataclasses import dataclass, field


@dataclass
class Functionality:

    api_key: str
    temperature: float
    endpoint: str
    image_path: str = field(init=False)
    sample_image: str = field(default='', init=False)
    prompt: str = field(init=False)

    @property
    def params(self) -> tuple:
        return self.image_path, self.prompt, self.sample_image

    @params.setter
    def params(self, values: tuple[str, str, str]) -> None:
        """Sets the image path and prompt for the instance."""
        self.image_path, self.prompt, self.sample_image = values

    @staticmethod
    def _encode_image(image_path: str) -> str:
        """Encodes an image file to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('ascii')

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

    def _payload(self, agent: str, function: str) -> dict:
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
