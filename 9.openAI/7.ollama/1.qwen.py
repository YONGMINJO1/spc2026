# pip install requests
# ollama pull qwen2.5:1.5

import requests

MODEL_NAME = "qwen2.5:1.5b"

def ask_qwen(question):

    reponse = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": question,
            "stream":False
        }
    )

    data = reponse.json()
    final_reply = data ['response']
    
    #print(final_reply)
    
while True:
    user_input = input("나: ")
    if user_input == "exit":
        print("종료합니다.")
        break

    print("응답: " )