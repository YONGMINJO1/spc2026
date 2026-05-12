from flask import Flask
from flask import jsonify

app = Flask(__name__)

users = [
    {"name": "Alice", "age": 27, "phone": "010-1234-5678"},
    {"name": "bob", "age": 41, "phone": "010-9876-1234"},
    {"name": "mark", "age": 33, "phone": "010-5555-8888"},
]

# 파이썬 리스트 폼, 각각의 리스트에는 딕셔너리


@app.route("/")
def main():
    return jsonify(
        users
    )  # 우리의 백엔드 list/dict 구조를 웹이 좋아하는 JSON 포멧으로 변환해서 보내줌


@app.route("/user/<name>")
def get_user_by_name(name):
    print("사용자입력값: ", name)
    user = None
    for u in users:
        if u["name"].lower() == name.lower():
            user = u

    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "사용자를 찾지 못했습니다."})


if __name__ == "__main__":
    app.run(debug=True)
