from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="public", static_url_path="")

history = []


@app.route("/")
def index():
    return send_from_directory("public", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    chat_message = data.get("chatMessage")
    print("사용자 입력값: ", chat_message)

    history.append({"role": "user", "content": chat_message})

    # chatgpt 에게 물어보기...
    gpt_reply = ask_chatgpt(chat_message)

    history.append({"role": "assistant", "content": gpt_reply})

    print(">>>>>>>>>>")
    print(history)
    print("<<<<<<<<<<")

    return jsonify({"reply": {gpt_reply}})


def ask_chatgpt(chat_message):

    gpt_ask_message = [
        {
            "role": "system",
            "content": "당신은 친절한 챗봇입니다. 경상도 사투리를 적절하게 섞어서 답하시오.",
        },
        history,
    ]

    print(">>>>>>>>>>")
    print("최종 GPT 에게 우리가 물어볼 전체 메시지: ", gpt_ask_message)
    print("<<<<<<<<<<")

    # 호출하는 코드
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=gpt_ask_message
    )
    print("출력확인: ", response)
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
