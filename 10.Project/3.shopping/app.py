import os
from dotenv import load_dotenv

from flask import Flask, send_from_directory, jsonify, request
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="public")

reviews = (
    []
)  # 사용자들의 댓글을 저장할 변수 (평점과 후기가 함께 들어간다. {'rating':값,'comment':값})


# ---------------
# API 서버 라우팅
# ---------------
@app.route("/api/reviews", methods=["POST"])  # POST로 받기
def add_review():
    # reviews에 저장하기
    data = request.get_json()

    rating = data["rating"]
    comment = data["comment"]

    reviews.append({"rating": rating, "comment": comment})
    return jsonify({"message": "저장완료"})


@app.route("/api/reviews", methods=["GET"])  # GET로 받기
def get_review():
    # reviews를 가져와서 변환하기
    return jsonify(reviews)


@app.route("/api/ai-summary", methods=["GET"])  # GET로 받기
def get_ai_summary():
    # reviews를 가져와서..
    # 여기서 프롬프트 및 API 호출 코드 작성
    # 리뷰 문자열 정리
    # 리뷰가 없을 경우
    if len(reviews) == 0:
        return jsonify(
            {"message": "아직 등록된 리뷰가 없습니다.", "average_rating": "N/A"}
        )

    review_text = "\n".join(
        [f"- 평점 {r['rating']}점: {r['comment']}" for r in reviews]
    )

    # 평균 별점 계산
    avg_rating = round(sum(int(r["rating"]) for r in reviews) / len(reviews), 1)

    prompt = f"""
아래는 쇼핑몰 상품 리뷰입니다.

리뷰들을 읽고 전체적인 고객 반응을 자연스럽게 요약해주세요.

규칙:
- 리뷰를 하나씩 나열하지 말 것
- 억지로 장단점을 분리하지 말 것
- "정보가 부족합니다", "파악하기 어렵습니다" 같은 표현 금지
- 실제 쇼핑몰에서 보여주는 리뷰 요약처럼 자연스럽게 작성
- 2~3문장 정도로 간결하게 작성
- 말투는 부드럽고 자연스럽게

리뷰:
{review_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 쇼핑몰 리뷰 요약 전무가 입니다."},
            {"role": "user", "content": prompt},
        ],
    )
    summary = response.choices[0].message.content

    return jsonify({"message": summary, "average_rating": avg_rating})


# ---------------
# 웹 서버 라우팅
# ---------------
@app.route("/")
def index():
    return send_from_directory("public", "index.html")


if __name__ == "__main__":
    app.run(debug=True)
