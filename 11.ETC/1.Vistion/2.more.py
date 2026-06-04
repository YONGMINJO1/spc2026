
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {
#             'role':'user' 
#             'content' : [
#                 {"type":"text", "text":"이 이미지를 한국어로 설명해줘"},
#                 {"type":"image_url","image_url":}
#             ]
#         }
#     ]
# )

question = [

]

