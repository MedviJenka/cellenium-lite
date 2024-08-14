import base64
import requests
from dataclasses import dataclass


@dataclass
class Functionality:

    api_key: str
    endpoint: str

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
