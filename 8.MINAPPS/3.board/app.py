from flask import Flask, send_from_directory, redirect, request, jsonify
from database import MyDatabase

app = Flask(__name__)
db = MyDatabase()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    title = data.get("title")
    message = data.get("message")
    # print(title, message)
    sql = "INSERT INTO board (title, message) VALUES (?,?)"
    db.execute(sql, (title, message))
    db.commit()

    return jsonify({"result": "success"})


@app.route("/list")
def list():
    sql = "SELECT * FROM board"
    result = db.execute_fetch(sql)
    dict_list = [
        {"id": r["id"], "title": r["title"], "message": r["message"]} for r in result
    ]

    return jsonify(dict_list)
    # return jsonify({'result':'success'})


@app.route("/delete", methods=["DELETE"])
def delete():
    data = request.get_json()
    id = data.get("id")
    sql = "DELETE FROM board WHERE id=?"
    db.execute(sql, (id,))
    db.commit()
    return jsonify({"result": "success"})


@app.route("/modify", methods=["PUT"])
def modify():
    data = request.get_json()
    id = data.get("id")
    title = data.get("title")
    message = data.get("message")
    sql = "UPDATE board SET title=?, message=? WHERE id=?"
    db.execute(sql, (title, message, id))
    db.commit()
    return jsonify({"result": "success"})


if __name__ == "__main__":
    app.run(debug=True)
