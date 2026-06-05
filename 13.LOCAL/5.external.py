# 외부에 ollama 서버가 있는 경우.. 나의 req를 api에 요청하듯이 하면 도미

import requests

OLLAMA_HOST = "https://123.123.123:11434"
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"

payload = {
    "model": "exaone3.5:2.4d",
    "prompt": "파이썬으로 구현하는 헬로우 월드 코드를 보여줘",
    "stream": False
}

response = requests.post(OLLAMA_ENDPOINT, json=payload)
data = response.json()

print("모델 응답: ",data.get("response"))
