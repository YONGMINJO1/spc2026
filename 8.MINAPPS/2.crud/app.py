from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session,flash

from datetime import timedelta

import sqlite3

app=Flask(__name__)
app.secret_key = 'Hello1234' # 실무적으로는 이런 민감한 credential을 커밋하지 않음
app.permanent_session_lifetime = timedelta (minutes=5)

DATABASE = 'user.sqlite3' # 나의 파일명

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # 나의 결과를  dict 포맷으로 관리
                                    # row[0] => row['id'] 이런식으로 접근 가능
    return conn

def init_db():
    with app.app_context(): # flask app 초기화 완료 후
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        username TEXT NOT NULL,
                                        password TEXT NOT NULL,
                                        email TEXT 
                    )
                    """)
        
        # 기본 계정 정보
        cur.execute('SELECT COUNT(*) AS count FROM users')
        count = cur.fetchone()['count'] 
        if count == 0:
            cur.execute("INSERT INTO users (username, password, email) VALUES (?,?,?)", ("user1","password1","user1@example.com"))
            cur.execute("INSERT INTO users (username, password, email) VALUES (?,?,?)", ("user2","password2","user2@example.com"))

        # 부팅시 계정 정보 출력
        cur.execute("SELECT * FROM users ")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=["POST"])
def profile_edit():
    return "나중에 구현"

@app.route('/profile', methods=["GET","POST"])
def profile():
    # 1.DB에서 나의 정보를 조회한다.
    # 2. 그래서 아래에 넘겨준다.
    # 3. 해당 정보에 수정기능을 넣는다.
    if 'user' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
    
    username = session['user']

    conn = get_db_connection()
    cur = conn.cursor()

    # 수정
    if request.method == "POST":

        new_password = request.form.get('password')
        new_email = request.form.get("email")

        cur.execute(
            """
            UPDATE users
            SET password=?,email=?
            WHERE username=?
            """,(new_password,new_email,username)
            )
            
        conn.commit()

        flash("회원정보가 수정되었습니다.")


    cur.execute("SELECT * FROM users WHERE username=?",(username,))

    user_data = cur.fetchone()
    conn.close()

    return render_template('profile.html',user=user_data)

@app.route('/signin', methods=["GET","POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        conn = get_db_connection()
        cur = conn.cursor()

        # 회원가입
        cur.execute("INSERT INTO users (username, password, email) VALUES (?,?,?)",(username, password, email))

        conn.commit()
        conn.close()

        flash("회원가입이 완료되었습니다.")

    return render_template('signin.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()
        # cur.execute("사용자 조회하는 쿼리")
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username, password))
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            session['user'] = username
            flash("로그인에 성공했습니다.")
            return redirect(url_for("home"))
        else:
            flash("로그인에 실패했습니다.")
            return redirect(url_for("login"))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("성공적으로 로그아웃이 되었습니다.")
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)