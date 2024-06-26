import base64
import requests
from dataclasses import dataclass
from core.manager.reader import read_json
from core.modules.decorators import negative


@dataclass
class Bini:

    api_key: str = read_json(env_key='GPT_API')
    max_tokens: int = 300
    model: str = "gpt-4o"

    @staticmethod
    def __encode_image(image_path) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def base64_image(self, image_path) -> None:
        return self.__encode_image(image_path)

    def image(self, image_path: str, prompt: str) -> str:
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
          "model": self.model,
          "messages": [
            {
                "role": "system",
                "content": "Your name is Bini and you're a professional UI/UX manager and a QA engineer. "
                           "from now on you will give me a very detailed and well written response of the image that "
                           "will be uploaded to you. after each session you will return Passed or Fail"
                           "IMPORTANT:"
                           "always type 'Passed' if you think you were correct"
                           "if you could not find, indentify or determine something, always type 'Fail'"},
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
                    "url": f"data:image/jpeg;base64,{self.base64_image(image_path)}",
                    'details': 'high',
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

    def assist(self, prompt: str) -> str:
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
                "role": "system",
                "content": "Your name is Beany and you're a professional developer that has a keen eye for small details"},
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": prompt
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


bini = Bini()


def test_user_is_displayed() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png",
        prompt='Is Efrat Lang displayed on the right side of the screen? at the end type Passed if yes')
    assert 'Passed' in response


def test_meeting_insights() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_5.png",
        prompt='validate the dates are displayed are from 4/4/24 to 14/5/24, parse the date type as day/month/year')
    assert 'Passed' in response


def test_user_is_not_displayed() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img.png",
        prompt='Is Evgeny Petrusenko displayed on the right of the screen?')
    assert 'Fail' in response


def test_outgoing_calls_under_external_p2p() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_3.png",
        prompt='how many Outgoing" has the call type "External p2p')
    assert '3' or 'Three' in response


def test_count_rows() -> None:
    response = bini.image(
        image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_1.png",
        prompt='count all the rows that starts with blue play button on the left, expected result is 10')
    assert 'Passed' in response


def test_no_rows() -> None:
    response = bini.image(image_path=r"C:\Users\evgenyp\PycharmProjects\cellenium-lite\core\data\images\img_2.png",
                          prompt='are there any rows?, expected is: No Rows')
    assert 'Passed' in response
