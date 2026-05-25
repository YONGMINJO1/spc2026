from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    chat_message = data.get("chatMessage")
    print("사용자 입력값: ", chat_message)

    # chatgpt 에게 물어보기...
    gpt_reply = ask_chatgpt(chat_message)

    return jsonify({"reply": gpt_reply})


def ask_chatgpt(chat_message):
    response = client.chat.completions.create(  # 호출하는 코드
        model="gpt-4o-mini",  # 웬만한 실습은 gpt-4o-mini
        messages=[
            {"role": "system", "content": "당신은 친절한 챗봇입니다."},
            {"role": "user", "content": chat_message},
        ],
    )
    print("출력확인: ", response)
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
