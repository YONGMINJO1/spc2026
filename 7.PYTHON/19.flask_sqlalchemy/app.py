from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Srtring(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    # 여기 밑에는 Flask나 SQLAlchemy외는 무관한.. 파이썬 클래스를 출력할때, 그 출력 포맷을 내가 정의하는 커스텀 클래스 출력 포맷 정의
    def __repr__(self):
        return f'<User {self.id},{self.name},{self.age}'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'splite:///example.db'
app.comfig['SQLALCHEMY_TRACK_MODIFICATION'] =False

# 우리의 db와 flask 앱 연결
db.init_app(app)

@app.route('/add', methods=["POST"])
def add_user():
    name = request.form.get('name')
    age = request.form.get('age')
    if not name or not age:
        flash('이름과 나이를 모두 입력해야 합니다.')
        return redirect(url_for('index'))

    new_user = User(name=name,age=age)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('delete_user/<int:id>')
def delete_user(id):
    user = db.session.delete(user)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'사용자(id: {id}가 삭제되었습니다.)')
    
    return redirect(url_for('index'))