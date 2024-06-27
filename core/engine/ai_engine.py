import base64
import requests
from PIL import Image
from openai import OpenAI
from dataclasses import dataclass
from core.manager.reader import read_json


@dataclass
class Bini:

    """
    Bini Advantages:

        1. Advanced Image Recognition:

        2. GPT engines can leverage deep learning models for advanced image recognition and analysis.
        They can understand complex visual patterns and elements within the UI, such as icons, buttons, and layout arrangements.
        Contextual Understanding:

        3. GPT engines can interpret the context and intent behind visual elements, providing a more comprehensive assessment of UI design and functionality.
        This is useful for evaluating the overall user experience and ensuring that the UI elements align with user expectations.
        Natural Language Interface:

        4. Tests can be specified and adjusted using natural language, making it easier for non-technical stakeholders to contribute to the testing process.
        This can improve collaboration and communication within development teams.
        Handling Variability:

        5. GPT engines can adapt to variations in UI design and content more effectively than traditional automated scripts.
        They can handle dynamic and responsive layouts, which is particularly useful for testing across different devices and screen sizes.
        Cognitive and Perceptual Testing:

        6. GPT engines can evaluate aesthetic aspects of the UI, such as color schemes, font readability, and overall visual appeal.
        They can also simulate human-like perceptions, providing insights into how users might interact with and perceive the UI.

    What Token is:
        In the context of using OpenAI's GPT models for chat interactions, a "token" refers to a unit of text or
        language that the model processes during its computations. Tokens can vary in length depending on the model's
        configuration and the specific task at hand.
        Here's a breakdown of what a token typically represents:

        Basic Unit of Text: A token can represent a word, punctuation mark, or part of a word. For instance,
        in the sentence "Hello, how are you?", tokens could be "Hello", ",", "how", "are", "you", and "?".

        Model Input: When you provide input to a GPT model for chat completion, each piece of text
        (such as a word or part of a sentence) is broken down into tokens.
        These tokens are then processed sequentially by the model to generate a response.

        Max Tokens Parameter: In OpenAI's API and similar interfaces,
        you often set a parameter called max_tokens when making requests.
        This parameter specifies the maximum number of tokens the model should generate in its response.
        It helps control the length of the generated text and can influence the depth of detail in the model's responses.

        Tokenization Process: Tokenization is the process of breaking down text into these units (tokens)
        for computational processing. This step is crucial for natural language processing tasks, as it allows the
        model to understand and manipulate text effectively.

        In summary, tokens in the context of using GPT models for chat refer to the fundamental units of text that the
        model processes and generates as part of its natural language understanding and generation capabilities. Each
        token corresponds to a specific part of the input or output text sequence.

    :param: api_key ................... api secret key generated from openai website, and copied to json file outside
                                        the project directory for security reasons
            max_tokens ................ maximum tokens that can be used pare image
            model ..................... type of gpt module user wants to use

    """

    api_key: str = read_json(env_key='GPT_API')
    max_tokens: int = 400
    model: str = "gpt-4o"

    @staticmethod
    def __encode_image(image_path: str) -> base64:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def base64_image(self, image_path: str) -> None:
        return self.__encode_image(image_path)

    def image(self, image_path: str, prompt: str) -> any:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content":
                        "Your name is Bini and you're a professional UI/UX manager and a QA engineer."
                        "from now on you will give me a very detailed and well written response of the image that "
                        "will be uploaded to you. after each session you will return Passed or Fail"
                        "*IMPORTANT!!*"
                        "* calendar dates will be always presented in day/month/year format"
                        "* always return 'Passed' if you determined and located what was written in the prompt"
                        "* always return 'Fail' if you could not find, indentify or determine something"},
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
        price = self.calculate_token_cost(image=image_path, price_per_1000_tokens=0.003, detail='high')
        print(f'PRICE PARE IMAGE: {price}$')
        print(response)

        return response

    def generate_image(self, screenshot: str) -> any:

        client = OpenAI(api_key=self.api_key)
        response = client.images.edit(model="dall-e-2",
                                      image=open(screenshot, "rb"),
                                      mask=open(screenshot, "rb"),
                                      prompt="mark the difference between 2 images that u compared before",
                                      n=1,
                                      size="1024x1024")
        image_url = response.data[0].url
        return image_url

    @staticmethod
    def __get_image_dimensions(image: str) -> (int, int):
        with Image.open(image) as img:
            width, height = img.size
        return [width, height]

    def calculate_token_cost(self, image: str, detail: str, price_per_1000_tokens: float) -> float:

        width = self.__get_image_dimensions(image)[0]
        height = self.__get_image_dimensions(image)[1]

        if detail == "low":
            token_cost = 85

        elif detail == "high":
            # Scale to fit within 2048 x 2048 while maintaining aspect ratio
            if width > 2048 or height > 2048:
                aspect_ratio = width / height
                if aspect_ratio > 1:
                    width = 2048
                    height = int(2048 / aspect_ratio)
                else:
                    height = 2048
                    width = int(2048 * aspect_ratio)

            # Scale such that the shortest side is 768px long
            if width < height:
                scale_factor = 768 / width
            else:
                scale_factor = 768 / height

            width = int(width * scale_factor)
            height = int(height * scale_factor)

            # Calculate the number of 512px squares
            num_squares = (width // 512) * (height // 512)

            # Calculate the total token cost
            token_cost = 170 * num_squares + 85

        else:
            raise ValueError("Invalid detail level. Choose 'low' or 'high'.")

        # Calculate the cost in dollars
        cost_in_dollars = (token_cost / 1000) * price_per_1000_tokens
        return cost_in_dollars

    # def compare_images(self,
    #                    prompt: str,
    #                    figma_image: str,
    #                    screenshot: str,
    #                    ignore: Optional[str] = None,
    #                    skip_if_failed: Optional[bool] = False
    #                    ) -> str:
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {self.api_key}"
    #     }
    #
    #     payload = {
    #         "model": self.model,
    #         "messages": [
    #             {
    #                 "role": "system",
    #                 "content":
    #                     "Your name is Bini and you're a professional UI/UX manager and a QA engineer."
    #                     "from now on you will give me a very detailed and well written response of the image that "
    #                     "will be uploaded to you. after each session you will return Passed or Fail"
    #                     "*IMPORTANT!!*"
    #                     "* your main goal is to compare between 2 images and sport differences and similarities"
    #                     "* calendar dates will be always presented in day/month/year format"
    #                     "* always type 'Passed' if you determined what was written in the prompt"
    #                     "* always type 'Fail' if you could not find, indentify or determine something"
    #             },
    #             {
    #                 "role": "user",
    #                 "content": [
    #                     {
    #                         "type": "text",
    #                         "text": prompt
    #                     },
    #                     {
    #                         "type": "image_url",
    #                         "image_url": {
    #                             "url": f"data:image/jpeg;base64,{self.base64_image(figma_image)}",
    #                             'details': 'high',
    #                         }
    #                     },
    #                     {
    #                         "type": "image_url",
    #                         "image_url": {
    #                             "url": f"data:image/jpeg;base64,{self.base64_image(screenshot)}",
    #                             'details': 'high',
    #                         }
    #                     },
    #                     {
    #                         "type": "image_url",
    #                         "image_url": {
    #                             "url": f"data:image/jpeg;base64, {self.generate_image(screenshot)}",
    #                             'details': 'high',
    #                         }
    #                     },
    #                 ]
    #             }
    #         ],
    #         "max_tokens": self.max_tokens
    #     }
    #
    #     outcome = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #     response = outcome.json()['choices'][0]['message']['content']
    #     print(response)
    #     return response
