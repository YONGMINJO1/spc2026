# pip install flask-session

from flask import Flask, session
from flask_session import Session # 서버측에 세션을 저장하기 위한 확장 클래스

app = Flask(__name__)
app.secret_key = 'your_secret_key' # 나만 아는 나의 세션 암호화 키 =-> .env 파일에서 다루는 거임 
app.config['SESSION_TYPE']= 'filesystem' # 나의 세션을 파일 / redis / memcahed / mongo 등등 다양한걸 다룸
app.config['SESSION_FILE_DIR']='././sessions'
app.config['SESSION_PERMANENT']= False
app.config['SESSION_USE_SIGNER']= True

Session(app)

@app.route('/set-session')
def set_sesstion():
    if 'username' in session:
        return f"세션에서 당신의 정보를 찾았습니다. {session['username'],session['fullname'],session['dob'],session['hobby']}"
    # return "세션 정보가 없습니다."
    session['username']='spc2026'
    session['fullname']='홍길동'
    session['dob']='2020/05/05'
    session['hobby']='유튜브하기, 쇼핑하기, 게임하기'
    
    return "첫 방문이시군요"

if __name__ == "__main__":
    app.run(debug=True)