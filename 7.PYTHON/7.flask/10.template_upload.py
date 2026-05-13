from flask import Flask, render_template, request

import os

app = Flask(__name__)

# 저장소 설정
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# def allowerd_file(filename):
#     ALLOWERD_EXT = 

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', metthods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    print(f"입력한 ID는 {id}, PW는 {pw}")
    # if id == u['id'] and pw == u['pw']:

    return render_template('login.html', name=id)

# @app.route('upload', methods=['POST'])
# def upload_file 