from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"name": "Alice", "age": 27, "phone": "010-1234-5678"},
    {"name": "bob", "age": 41, "phone": "010-9876-1234"},
    {"name": "mark", "age": 33, "phone": "010-5555-8888"},
    {"name": "David", "age": 33, "phone": "010-5555-8888"},
]

@app.route('/search/')
def search():

    query = request.args.get('q')
    page = request.args.get('page',default=1,type=int)

    user_input = f"Your query is {query} and page= {page}"

    return jsonify({"message": user_input})

@app.route('/user/<username>/post')
def show_user_posts(username):
    page = request.args.get('page', default=1 , type=int)

    result = f"User is {username} and page is {page}"
    return jsonify({"message": result})


if __name__ == "__main__":
    app.run(debug=True)
