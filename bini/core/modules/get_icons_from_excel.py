import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as ExcelImage
from PIL import Image as PILImage
from bini.core.data.abstract_paths import SAMPLES


def extract_image_from_excel(image_name: str, output_path: str) -> str:
    # Load the workbook and the sheet
    workbook = load_workbook(filename=SAMPLES)
    sheet = workbook.active

    # Iterate through all images in the sheet
    for image in sheet._images:
        if not image_name:
            if image.anchor._from.row == 2 and image.anchor._from.col == 2:  # Assuming image is in the second row and second column
                # Save the image
                img = PILImage.open(image.path)
                img.save(output_path)
                return f"Image saved to {output_path}"

    return "Image not found"


# Usage

image_name = 'play_icon'
output_path = 'output_image_path.png'
result = extract_image_from_excel(image_name, output_path)
print(result)
