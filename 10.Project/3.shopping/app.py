import os
from dotenv import load_dotenv

from flask import Flask, send_from_directory, jsonify, request
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app=Flask(__name__, static_folder="public")

reviews = [] # 사용자들의 댓글을 저장할 변수 (평점과 후기가 함께 들어간다. {'rating':값,'comment':값})
#---------------
# API 서버 라우팅
#---------------
@app.route('/api/reviews', methods=['POST']) # POST로 받기
def add_review():
    # reviews에 저장하기
    data = request.get_json()

    rating = data['rating']
    comment = data['comment']

    reviews.append({'rating': rating, 'comment':comment})
    return jsonify({'message':'저장완료'})

@app.route('/api/reviews', methods=['GET']) # GET로 받기
def get_review():
    # reviews를 가져와서 변환하기
    return jsonify(reviews)

@app.route('/api/ai-summary', methods=['GET']) # GET로 받기
def get_ai_summary():
    # reviews를 가져와서..
    # 여기서 프롬프트 및 API 호출 코드 작성
    prompt = f"다음 리뷰들을 요약해줘: {reviews}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    summary = response.choices[0].message.content

    return jsonify({'message':summary})


#---------------
# 웹 서버 라우팅
#---------------
@app.route('/')
def index():
    return send_from_directory('public','index.html')

if __name__ == "__main__":
    app.run(debug=True)