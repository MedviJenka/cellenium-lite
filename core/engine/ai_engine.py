import base64
import requests
from dataclasses import dataclass
from core.manager.reader import read_json


@dataclass
class Binny:

    api_key = read_json(env_key='GPT_API')
    image_path: str
    max_tokens: int = 300

    def __encode_image(self) -> base64:
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @property
    def base64_image(self) -> None:
        return self.__encode_image()

    def execute(self, prompt: str) -> None:
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
                    "url": f"data:image/jpeg;base64,{self.base64_image}"
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


def test_user_is_displayed() -> None:
    bini = Binny(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png")
    response = bini.execute(prompt='is Efrat Lang displayed? and do you see any abnormalities?')
    assert 'Yes' in response


def test_count_rows() -> None:
    bini = Binny(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_1.png")
    response = bini.execute(prompt='count all the rows that starts with blue play button')
    assert '10' in response
