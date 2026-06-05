# pip install anthropic
import os
import time

import anthropic

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

models = ['claude-haiku-4-5', 'claude-sonnet-4-6', 'claude-opus-4-7', 'claude-opus-4-8']

prompt = "인공지능과 LLM의 동작 원리를 초등학생도 쉽게 이해할 수 있도록 설명해"

for model in models:
    start = time.time()
    msg = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role":"user", "content": prompt}]
    )
    elasped = time.time() - start
    text = msg.content[0].text
    print(f"[{model}] {elasped:.1f}초, 출력 {msg.usage.output_tokens} 토큰")
    print(f"{text}")

# def ask(question):
#     print("질문 ", question)

#     messages.append({"role":"user", "content": question})

#     message = client.messages.create(
#         # haiku (빠름), sonnet
#         model="claude-haiku-4-5",
#         max_tokens=300,
#         temperature=0,
#         messages=messages
#         # messages=[{
#         #     "role":"user","content":question
#         # }]
#     )
#     return message.content[0].text

# print("[챗봇} ",ask("내 이름은 홍길동이야"))
# print("[챗봇} ",ask("내가 누구라고?"))