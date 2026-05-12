from flask import Flask

app = Flask(__name__)

@app.route("/user")

@app.route("/user/<username>") # <변수> 가변인자
def show_user_user(username="익명"):
    return f"<h1>사용자: {username}</h1>"

@app.route("/admin")
def show_user_admin():
    return "사용자: 홍길동"

@app.route("/product")
@app.route("/product/<int:id>") # id: 숫자로 지정
def show_user_product(id=0):
    return f"상품코드: {id}, 사과"


if __name__ == '__main__':
    app.run()