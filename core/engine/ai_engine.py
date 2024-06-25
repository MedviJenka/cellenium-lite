import openai
from PIL import Image
import io


# Set up your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Function to convert an image to a byte array
def image_to_byte_array(image: Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# Open an image file
image_path = 'path_to_your_image.png'
image = Image.open(image_path)

# Convert the image to a byte array
image_bytes = image_to_byte_array(image)

# Optionally, describe the image
image_description = "A description of the image goes here."

# Create a prompt for GPT-4
prompt = f"Analyze the following image: {image_description}"

# Call GPT-4 with the prompt
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=150
)

# Print the response from GPT-4
print(response.choices[0].text.strip())
