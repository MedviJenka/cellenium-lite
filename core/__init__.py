from PIL import Image


get_token = {
    'id': 'chatcmpl-9egGXXX2llMaeYGzTvO2wjsCEHLEz',
    'object': 'chat.completion',
    'created': 1719482617,
    'model': 'gpt-4o-2024-05-13',
    'choices': [
        {
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': 'Yes, "Efrat Lang" is displayed on the right side of the screen.\n\nPassed'
            },
            'logprobs': None,
            'finish_reason': 'stop'
        }
    ],
    'usage': {
        'prompt_tokens': 896,
        'completion_tokens': 19,
        'total_tokens': 915
    },
    'system_fingerprint':
        'fp_4008e3b719'
}
print(type(get_token['usage']['total_tokens']))


def get_image_dimensions(image_path: str) -> (int, int):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height






def calculate_image_token_cost(width: int, height: int, detail: str, price_per_1000_tokens: float) -> float:
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


# Example usage
price_per_1000_tokens = 0.02

cost1 = calculate_image_token_cost(1024, 1024, "high", price_per_1000_tokens)
print(f"The cost for a 1024x1024 image in high detail is ${cost1:.4f}")

cost2 = calculate_image_token_cost(2048, 4096, "high", price_per_1000_tokens)
print(f"The cost for a 2048x4096 image in high detail is ${cost2:.4f}")

cost3 = calculate_image_token_cost(4096, 8192, "low", price_per_1000_tokens)
print(f"The cost for a 4096x8192 image in low detail is ${cost3:.4f}")
