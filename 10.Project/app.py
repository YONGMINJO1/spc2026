# 1. openai 관련 라이브러리를 다 불러온다. (dotenv, openai 등등)
# 2. 커리큘럼 페이지 ( 우리의 최종 페이지 )에서 체팅창 FE를 만든다.
# 3-1. 그 FORM을 BE에서 받아서, chatgpt API를 호출한다. (그냥 아무말이나 해도됨..)
# 3-2. 응답을 받아서 다시 프런트엔드에 반환해서, 결과를 출력한다.
# 3-3. [추가]  복습을 원하면 SSE 기반에 스트리밍 구현
# 4. 그럼 이제, 진짜 우리의 이 상황 (학년, 커리큐럼) 에 대해서 영어로 대화를 하도록 만든다.
# 5. [추가] 메모리를 통해서 대화 내용 컨텍스트를 기억하게 한다.

import os

from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = Flask(__name__)

history = []

# 각 학년별 커리큘럼 데이터

curriculums = {
    1: ["기초 인사", "간단한 문장", "동물이름"],
    2: ["학교 생활", "가족 소개", "자기소개"],
    3: [
        "취미와 운동",
        "날씨 묘사",
        "간단한 이야기",
    ],  # 나중에 내용을 바꾸거나, 목록을 추가하거나
    4: ["쇼핑과 가격", "음식 주문", "여행이야기 "],
    5: ["역사와 문화", "과학과 자연", "사회 이슈"],
    6: ["미래 계획", "진로 탐색", "세게 여행"],
}


@app.route("/")
def home():
    return render_template("home.html", grades=curriculums.keys())


@app.route("/grade/<int:grade>")
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template(
            "grade.html",
            grade=grade,
            grades=curriculums.keys(),
            curriculums=curriculums_index,
        )
    return "해당 학년은 존재하지 않습니다.", 404


@app.route("/grade/<int:grade>/curriculum/<int:curriculum_id>")
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template(
            "curriculum.html",
            grade=grade,
            grades=curriculums.keys(),
            curriculum_title=curriculum_title,
        )
    return "해당 커리큐럼은 존재하지 않습니다.", 404


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    grade = request.json.get("grade")
    curriculum_title = request.json.get("curriculum_title")

    # GPT한테 물어보기
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                너는 친절한 초등학교 영어 선생님이야.
                지금 {grade}학년 학생에게
                '{curriculum_title}' 주제로 영어를 가르치고 있어.

                반드시:
                - 쉬운 영어 사용
                - 짧은 문장 사용
                - 관련 주제로만 대화
                - 한국어 설명도 가능
                - markdown 사용 금지
                """,
            }
        ]
        + history
        + [
            {"role": "user", "content": user_message},
        ],
    )

    # AI 응답에서 텍스트 꺼내기
    ai_message = response.choices[0].message.content
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ai_message})
    history = history[-5:]  # 마지막 10개만 유지

    return jsonify({"reply": ai_message})


if __name__ == "__main__":
    app.run(debug=True)
