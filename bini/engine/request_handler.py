import requests
from time import sleep
from dataclasses import dataclass
from bini.core.modules.image_compression import ImageCompression


@dataclass
class APIRequestHandler(ImageCompression):

    api_key: str
    endpoint: str
    session: requests.Session

    @property
    def _headers(self) -> dict:
        """Returns the headers for the API request."""
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def get_response_json(self, payload: dict) -> dict:
        """Makes the API request and returns the output."""
        response = self.session.post(url=self.endpoint, headers=self._headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data

    def get_tokens(self, payload: dict) -> None:
        """returns amount of tokens used in current session"""
        data = self.get_response_json(payload=payload)
        tokens = data["usage"]["total_tokens"]
        print(tokens)

    def make_request(self, payload: dict) -> str:
        """Makes the API request and returns the output."""
        try:
            data = self.get_response_json(payload=payload)
            output = data['choices'][0]['message']['content']
            self.get_tokens(payload=payload)
            return output
        except requests.RequestException as e:
            print(f"Request error: {e}")
            sleep(3)
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
