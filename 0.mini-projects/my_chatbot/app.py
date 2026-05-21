from flask import Flask, render_template, jsonify, request
from openai import OpenAI
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]

    client = OpenAI(
        api_key="sk-test-1234"
    )  # env 파일을 사용해서 실제 API-KEY  사용하기!

    completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": message}]
    )
    reply = completion.choices[0].message.content
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
