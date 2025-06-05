import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
API_KEY = os.getenv("STABILITY_API_KEY")


def generate_stability_image(prompt: str) -> Image.Image:
    headers = {
        "authorization": f"Bearer {API_KEY}",
        "accept": "image/*"
    }

    # Stability expects 'files' even if empty, and 'data' for prompt etc.
    response = requests.post(
        API_URL,
        headers=headers,
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )
    if response.status_code == 200:
        # Load the image from bytes into PIL Image object
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(f"Stability API error: {response.json()}")
