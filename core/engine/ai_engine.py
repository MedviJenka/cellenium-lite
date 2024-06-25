import base64
import requests
from dataclasses import dataclass
from core.manager.reader import read_json


class Binny:

    def __init__(self,*, api_key = read_json(env_key='GPT_API'), max_tokens: int = 1000):
        self.api_key = api_key
        self.max_tokens = max_tokens

    def __encode_image(self, image_path) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def base64_image(self, image_path) -> None:
        return self.__encode_image(image_path)

    def execute(self, image_path: str, prompt: str) -> str:
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": prompt
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{self.base64_image(image_path)}"
                  }
                }
              ]
            }
          ],
          "max_tokens": self.max_tokens
        }

        outcome = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = outcome.json()['choices'][0]['message']['content']
        print(response)
        return response


bini = Binny()


def test_user_is_displayed() -> None:
    response = bini.execute(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png",
        prompt='is Efrat Lang displayed on the right of the screen? and do you see any abnormalities?')
    assert 'Yes' in response


def test_outgoing_calls_under_external_p2p() -> None:
    response = bini.execute(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_3.png",
        prompt='how many Outgoing" has the call type "External p2p')
    assert '3' or 'Three' in response


def test_count_rows() -> None:
    response = bini.execute(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_1.png",
        prompt='count all the rows that starts with blue play button, expected are 10')
    assert '10' or 'ten' in response


def test_no_rows() -> None:
    response = bini.execute(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_2.png",
                            prompt='are there any rows?, expected is no')
    assert 'No rows' in response
