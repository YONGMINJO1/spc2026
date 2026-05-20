from flask import Flask, send_from_directory,redirect,request, jsonify
from database import MyDatabase 

app = Flask(__name__)
db = MyDatabase()

@app.route('/')
def index():
    return send_from_directory('static','index.html')

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    title = data.get('title')
    message = data.get('message')
    # print(title, message)
    sql = "INSERT INTO board (title, message) VALUES (?,?)"
    db.execute(sql,(title, message))
    db.commit()
    
    return  jsonify({'result':'success'})

@app.route('/list')
def list():
    sql = 'SELECT * FROM board'
    result = db.execute_fetch(sql)
    dict_list = [{'id':result['id'], 'title': result['title'],'message':result['message']}]

    return jsonify(dict_list)
    #return jsonify({'result':'success'})

@app.route('/delete', methods=['POST'])
def delete():
    return jsonify({'result': 'success'})

@app.route('/modify', methods=['POST'])
def modify():
    return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run(debug=True)