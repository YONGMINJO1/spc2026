from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    model="black-forest-labs/FLUX.1-dev",
    token=os.getenv("HUGGUNGFACEHUB_API_TOKEN")
)

def generate_image(prompt, output_path="output.png"):
    image_bytes = client.text_to_image(
        prompt=prompt,
        guidance_scale=7.5,
        negative_prompt="low quality, blurry"
    )

    # if isinstance(image_bytes,Image.Image)