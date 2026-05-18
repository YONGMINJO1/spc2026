from flask import Flask, request, render_template, redirect, session, flash

app = Flask(__name__)

app.secret_key = "shop_secret_key"

products = [
    {"id": 1, "name": "연필", "price": 1000},
    {"id": 2, "name": "샤프", "price": 4500},
    {"id": 3, "name": "지우개", "price": 1500},
]


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return render_template(
                "login.html", error="아이디 또는 비밀번호가 틀렸습니다"
            )
    return render_template("login.html")


@app.route("/cart")
def cart():
    # 세션에서 cart 꺼내서 html에 넘거야함
    cart_ids = session.get("cart", [])
    # id로 실제 상품 정보 찾기
    cart_items = [i for i in products if str(i["id"]) in cart_ids]
    return render_template("cart.html", cart_items=cart_items)


@app.route("/cart/add", methods=["POST"])
def cart_add():
    if "user" not in session:
        return redirect("/login")

        # 1. 폼에서 product_id 받기
    product_id = request.form["product_id"]

    # 2. 세션에 cart가 없으면 빈 리스트로 초기화
    if "cart" not in session:
        session["cart"] = []

    # 3. 장바구니에 추가
    if product_id not in session["cart"]:
        session["cart"].append(product_id)
        session.modified = True
        flash('상품이 장바구니에 담겼습니다.')
    else:
        flash("이미 담겨있는 상품입니다.")

    # 4. 장바구니 페이지로 이동
    return redirect("/cart")


@app.route("/cart/delete", methods=["POST"])
def cart_delete():
    product_id = request.form["product_id"]
    session["cart"].remove(product_id)
    session.modified = True
    return redirect("/cart")


@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    session["cart"] = []
    session.modified = True
    return redirect("/cart")


if __name__ == "__main__":
    app.run(debug=True)
