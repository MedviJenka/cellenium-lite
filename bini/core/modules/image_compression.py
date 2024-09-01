import io
import base64
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
