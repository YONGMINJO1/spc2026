# pip install flask
# app.py - Flask 최소 애플리케이션
from flask import Flask

app = Flask(__name__)           # Flask 인스턴스 생성

@app.route('/')                 # 라우트 데코레이터로 URL과 함수 연결
def hello():
    return """
    <html>
        <title>타이틀</title>
        <style>
            p {
                color: red;
            }
        </style>
        <head>

        </head>
        
        <body>
            <h1>웰컴투 마이 홈</h1>
            <p>여기는 텍스트 본문이 들어갑니다.</p>
            <p>여기는 텍스트 본분이 들어갑니다22</p>
        </body>
    </html>"""

if __name__ == '__main__':
    app.run(debug=True)  # debug=True 이거 나중에 배포할때에 빼야함 (깃 올리기전)