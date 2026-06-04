# 텍스트를 기반으로 이미지를 생성 (GAN)

# 구버전 모댈이 dall-e => dall-e-2 => ??
# gpt-image-1.5 또는 gpt-image-2

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

prompt = """
해가 뜨고 있는 해변, 잔잔한 파도, 지브리 스타일
"""

result = client.images.generate(
    model="gpt-image-1.5",
    prompt=prompt,
    size="1024x1024",  # 1024x1024 (정사각형), 1024x1536(세로), 1536/1024 가로
    quality="medium",  # low / medium / high / auto
)

# image-2
# 4k 까지 지원함 (4096). 16:9 비율도 생성 가능...
# 지원 언어가 대폭 증가..
# 빠진 단점 하나는, 투명배경 못만듦.. 투명배경은 1.5의 기능임

image_base64 = result.data[0].b64_json

with open("sunset_beach.png", "wb") as f:
    f.write(base64.b64decode(image_base64))

print("이미지 저장 완료")
