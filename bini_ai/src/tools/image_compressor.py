import base64
from typing import Optional
from langchain_core.messages import HumanMessage
from bini_ai.src.utils.azure_llm import AzureLLMConfig


class CompressAndUploadImage(AzureLLMConfig):

    @staticmethod
    def __encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image

    def upload_image(self, image_path: str, prompt: str, sample_image: Optional[str or list] = '') -> str:
        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.__encode_image(image_path)}"}}
        ])

        if sample_image:
            if isinstance(sample_image, list):
                for each_image in sample_image:
                    message.content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{self.__encode_image(each_image)}"}
                    })
            else:
                message.content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{self.__encode_image(sample_image)}"}
                })

        response = self.langchain_llm.invoke([message])

        return str(response)
