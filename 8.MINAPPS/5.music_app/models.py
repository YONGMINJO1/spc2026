from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy 데이터베이스 객체 초기화
db = SQLAlchemy()

# 다대다 관계 테이블 (Song <-> Hashtag)
# 노래와 해시태그 간의 다대다(N:M) 매핑을 위한 중간 테이블입니다.
song_hashtag = db.Table(
    'song_hashtag',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id', ondelete='CASCADE'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model, UserMixin):
    """사용자 정보를 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # 관리자 여부 (수동 설정 방식)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    songs = db.relationship('Song', backref='uploader', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # 사용자가 받은 알림들
    notifications = db.relationship(
        'Notification',
        foreign_keys='Notification.user_id',
        backref='recipient',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    # 사용자가 생성한(보낸) 알림들
    sent_notifications = db.relationship(
        'Notification',
        foreign_keys='Notification.sender_id',
        backref='sender',
        lazy=True
    )
    
    def set_password(self, password):
        """비밀번호를 해싱하여 저장합니다."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """입력된 비밀번호가 저장된 해시와 일치하는지 확인합니다."""
        return check_password_hash(self.password_hash, password)


class Song(db.Model):
    """유튜브 음악 정보를 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'song'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    youtube_video_id = db.Column(db.String(50), unique=True, nullable=False)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    view_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    comments = db.relationship('Comment', backref='song', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='song', lazy=True, cascade='all, delete-orphan')
    
    # 다대다 관계 설정 (Hashtag)
    hashtags = db.relationship(
        'Hashtag',
        secondary=song_hashtag,
        backref=db.backref('songs', lazy='dynamic')
    )


class Comment(db.Model):
    """노래에 작성된 댓글을 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Like(db.Model):
    """사용자가 노래에 표시한 '좋아요' 정보를 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'like'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Hashtag(db.Model):
    """노래 분류를 위한 해시태그 정보를 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'hashtag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Notification(db.Model):
    """사용자에게 전달할 알림 정보를 저장하는 데이터베이스 모델입니다."""
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 알림을 수신할 사용자 ID
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 알림 발생의 원인을 제공한 사용자 ID (예: 좋아요 누른 유저)
    message = db.Column(db.String(255), nullable=False)                         # 알림 내용 메시지
    is_read = db.Column(db.Boolean, default=False)                            # 읽음 여부
    redirect_url = db.Column(db.String(255), nullable=True)                    # 클릭 시 이동할 URL 경로
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
