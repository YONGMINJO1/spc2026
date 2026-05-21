from dotenv import load_dotenv
import os

import requests

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)
user_input = "안녕하세요, 반갑습니다. 당신은 뭘해줄 수 있나요?"


response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    json={
        "model": "gpt-3.5-turbo",
        "messages": [
            # {'role':'system', 'content':'You are a helpful assistant.'},
            {"role": "system", "content": "너는 나를 잘 도와주는 경력 20년차개발자야."},
            {"role": "user", "content": user_input},
        ],
        "temperature": 1.0,
        "top_p": 0.5,
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    },
)
data = response.json()
print(data)
final_response = data["choices"][0]["message"]["content"]

print(final_response)
