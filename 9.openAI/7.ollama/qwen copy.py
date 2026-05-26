# pip install requests
# ollama pull qwen2.5:1.5

import requests

MODEL_NAME = "qwen2.5:1.5b"

reponse = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": MODEL_NAME,
        "prompt": "안녕하세요, 당신을 소개해주세요.",
        "stream":False
    }
)

data = reponse.json()
final_reply = data ['response']
print(final_reply)