import io
import base64
import requests
from dataclasses import dataclass
from PIL import Image


class ImageCompression:

    """Image resizing and high-quality compression logic."""

    @staticmethod
    def __resize_image(image_path: str, max_size: tuple[int, int] = (2048, 2048)) -> bytes:
        """
        Resizes an image to fit within the specified max_size while maintaining the aspect ratio.
        Applies high-quality compression settings.
        """
        with Image.open(image_path) as img:

            # High-quality downscaling filter
            img.thumbnail(max_size, Image.LANCZOS)
            buffer = io.BytesIO()

            # Preserve format and ensure high-quality JPEG compression
            img_format = img.format if img.format in 'PNG' else 'JPEG'
            if img_format == 'JPEG':
                img.save(buffer, format=img_format, quality=100, optimize=True, progressive=True)
            else:
                img.save(buffer, format=img_format, quality=100, optimize=True, progressive=True)

            return buffer.getvalue()

    def __encode_image(self, image_path: str) -> str:
        """Encodes a resized image file to a base64 string."""
        resized_image = self.__resize_image(image_path)
        return base64.b64encode(resized_image).decode('ascii')

    def get_image(self, image_path: str) -> str:
        """Returns the base64 encoded string of the image."""
        return self.__encode_image(image_path)


@dataclass
class APIRequestHandler(ImageCompression):

    api_key: str
    endpoint: str

    @property
    def _headers(self) -> dict:
        """Returns the headers for the API request."""
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def get_response_json(self, payload: dict) -> dict:
        """Makes the API request and returns the output."""
        response = requests.post(url=self.endpoint, headers=self._headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data

    def get_tokens(self, payload: dict) -> None:
        data = self.get_response_json(payload=payload)
        tokens = data["usage"]["total_tokens"]
        print(f'Tokens Used: {tokens}')

    def make_request(self, payload: dict) -> str:

        """Makes the API request and returns the output."""

        try:

            data = self.get_response_json(payload=payload)
            output = data['choices'][0]['message']['content']
            self.get_tokens(payload=payload)

            if requests.RequestException:
                from time import sleep
                sleep(3)
                pass

            return output

        except Exception as e:
            raise e
