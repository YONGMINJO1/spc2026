from flask import Flask
from flask import jsonify


app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 27, 'phone': '010-1234-5678'},
    {'name': 'bob', 'age': 41, 'phone': '010-9876-1234'},
    {'name': 'mark', 'age': 33, 'phone': '010-5555-8888'}
]

# 파이썬 리스트 폼, 각각의 리스트에는 딕셔너리

@app.route('/')
def main():
    return jsonify(users) 

if __name__ == '__main__':
    app.run(debug=True)