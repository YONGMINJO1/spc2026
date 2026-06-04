# 텍스트를 기반으로 이미지를 생성 (GAN)

# 구버전 모댈이 dall => dall-e-2 =>?
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

prompt ="""
해가 뜨고 있는 해변, 잔잔한 파도, 지브리 스타일
"""

result = client.images.generate(
    model="gpt-image-1.5",
    prompt=prompt,
    size="1024x1024",
    quality="medium"
)

image_base64 = result.data[0].b64_json

with open("sunset_beach.png", "wb") as f:
    f.write(base64.b64decode(image_base64))

print("이미지 저장 완료")