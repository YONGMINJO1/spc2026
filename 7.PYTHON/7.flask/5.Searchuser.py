from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"name": "Alice", "age": 27, "phone": "010-1234-5678"},
    {"name": "bob", "age": 41, "phone": "010-9876-1234"},
    {"name": "mark", "age": 33, "phone": "010-5555-8888"},
    {"name": "David", "age": 33, "phone": "010-5555-8888"},
]

@app.route('/search')
def search_user():

    name = request.args.get('name')
    age = request.args.get('age')
    phone = request.args.get('phont')

    result = users

    if name:
        result = [u    for u in result    if name.lower() in u['name']]

    if age:
        result = [u    for u in result    if int(age) == u['age']]
    
    if phone:
        # result = [u    for u in result    if phone == u['phone']]
        result = [u    for u in result    if u['phone'].startswith(phone)]
    # for u in users:
    #     if name and age and phone:
    #         ???s
    #     elif name and age:
    #         ???
    #     elif name and phone:
    #         ???

        # if u['name'] == name:

    #쿼리 파라미터로 name, age, phone로 검색해서 결과를 반환

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
