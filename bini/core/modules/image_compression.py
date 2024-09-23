import io
import base64
from PIL import Image

from bini.infrastructure.constants import WIDTH, HEIGHT


class ImageCompression:

    @staticmethod
    def __resize_image(image_path: str) -> bytes:

        """
        Resizes an image to fit within the specified max_size while maintaining the aspect ratio.
        Applies high-quality compression settings.

        """

        with Image.open(image_path) as img:
            # High-quality downscaling filter
            img.thumbnail(size=(WIDTH, HEIGHT), resample=Image.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format=img.format, quality=100, optimize=True, progressive=True)
            return buffer.getvalue()

    def __encode_image(self, image_path: str) -> str:
        """Encodes resized image file to a base64 string."""
        resized_image = self.__resize_image(image_path)
        return base64.b64encode(resized_image).decode('ascii')

    def get_image(self, image_path: str) -> str:
        """Returns the base64 encoded string of the image."""
        return self.__encode_image(image_path)
