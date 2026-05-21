from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Song, Comment, Like, Hashtag, Notification, song_hashtag
from utils import search_youtube_videos, parse_hashtags, create_notification

def create_app():
    """Flask 애플리케이션 팩토리 함수입니다."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # DB 및 로그인 매니저 초기화
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # 앱 최초 실행 시 SQLite 데이터베이스 파일 및 테이블 생성
    with app.app_context():
        db.create_all()
        create_default_admin()  # 기본 관리자 생성 헬퍼 호출
        
    return app

def create_default_admin():
    """기본 관리자 계정이 없는 경우 수동 생성합니다."""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        new_admin = User(username='admin', email='admin@music.app', is_admin=True)
        new_admin.set_password('admin123')
        db.session.add(new_admin)
        db.session.commit()

app = create_app()

@app.before_request
def load_unread_notifications_count():
    """실시간이 아닌 페이지 로드 시 알림을 조회하는 전역 훅입니다."""
    g.unread_count = 0
    g.notifications = []
    if current_user.is_authenticated:
        # 읽지 않은 알림 개수 계산
        g.unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        # 최근 5개의 알림 목록 조회
        g.notifications = Notification.query.filter_by(user_id=current_user.id)\
                                              .order_by(Notification.created_at.desc()).limit(5).all()

# --- 1~2단계 완료 후 공통 메인 뷰 ---
@app.route('/')
def index():
    """메인 페이지 뷰입니다. 최신 등록 곡 및 좋아요 순 인기 곡을 조회합니다."""
    # 최신 등록 곡 6개
    recent_songs = Song.query.order_by(Song.created_at.desc()).limit(6).all()
    
    # 좋아요 개수 정렬 인기 곡 (서브쿼리 및 조인 활용)
    popular_songs = db.session.query(Song)\
        .outerjoin(Like)\
        .group_by(Song.id)\
        .order_by(db.func.count(Like.id).desc(), Song.created_at.desc())\
        .limit(6).all()
        
    # 해시태그 목록 조회
    all_hashtags = Hashtag.query.limit(20).all()
    
    return render_template('index.html', recent_songs=recent_songs, popular_songs=popular_songs, all_hashtags=all_hashtags)

# --- 3단계: 회원가입 ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입 요청을 처리하는 컨트롤러입니다."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        return handle_register_post()
    return render_template('register.html')

def handle_register_post():
    """회원가입의 POST 데이터 처리를 분할한 헬퍼 함수입니다."""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        flash('이미 존재하는 사용자명 또는 이메일입니다.', 'danger')
        return redirect(url_for('register'))
        
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('회원가입이 완료되었습니다. 로그인 해주세요!', 'success')
    return redirect(url_for('login'))

# --- 4단계: 로그인/로그아웃 ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """로그인 요청을 처리하는 컨트롤러입니다."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        return handle_login_post()
    return render_template('login.html')

def handle_login_post():
    """로그인의 POST 데이터 처리를 분할한 헬퍼 함수입니다."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        flash(f'{username}님, 환영합니다!', 'success')
        return redirect(url_for('index'))
        
    flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'danger')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    """로그아웃 세션을 해제하고 메인으로 보냅니다."""
    logout_user()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('index'))

# --- 5단계: 유튜브 검색 연동 ---
@app.route('/api/search')
@login_required
def search_song():
    """유튜브 API를 타서 비동기 검색 결과를 JSON으로 응답합니다."""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = search_youtube_videos(query)
    return jsonify(results)

@app.route('/song/add', methods=['POST'])
@login_required
def add_song():
    """유튜브 검색 결과를 기반으로 새 노래를 등록하고 해시태그를 연결합니다."""
    title = request.form.get('title')
    artist = request.form.get('artist')
    video_id = request.form.get('youtube_video_id')
    thumbnail = request.form.get('thumbnail_url')
    hashtag_input = request.form.get('hashtags', '')
    
    # 중복 곡 등록 체크
    song = Song.query.filter_by(youtube_video_id=video_id).first()
    if not song:
        song = Song(title=title, artist=artist, youtube_video_id=video_id, thumbnail_url=thumbnail, user_id=current_user.id)
        db.session.add(song)
        db.session.commit()
        
    # 해시태그 추가 헬퍼 호출
    process_song_hashtags(song, hashtag_input)
    flash(f'"{title}" 곡이 성공적으로 등록되었습니다!', 'success')
    return redirect(url_for('song_detail', song_id=song.id))

def process_song_hashtags(song, hashtag_input):
    """노래에 해시태그 문자열을 파싱하여 연결 처리합니다."""
    tags = parse_hashtags(hashtag_input)
    for tag_name in tags:
        tag = Hashtag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Hashtag(name=tag_name)
            db.session.add(tag)
        if tag not in song.hashtags:
            song.hashtags.append(tag)
    db.session.commit()

# --- 6~8단계: 상세조회, 좋아요, 댓글, 해시태그 ---
@app.route('/song/<int:song_id>')
def song_detail(song_id):
    """노래 상세 조회 화면을 구성합니다."""
    song = Song.query.get_or_404(song_id)
    # 조회수 증가 (단순 조회 시 1 증가)
    song.view_count += 1
    db.session.commit()
    
    # 내가 이 곡을 좋아요 했는지 여부 확인
    is_liked = False
    if current_user.is_authenticated:
        is_liked = Like.query.filter_by(user_id=current_user.id, song_id=song.id).first() is not None
        
    return render_template('song_detail.html', song=song, is_liked=is_liked)

@app.route('/song/<int:song_id>/like', methods=['POST'])
@login_required
def toggle_like(song_id):
    """비동기 AJAX 좋아요 상태 토글 및 알림 생성 라우터입니다."""
    song = Song.query.get_or_404(song_id)
    like_obj = Like.query.filter_by(user_id=current_user.id, song_id=song.id).first()
    
    if like_obj:
        db.session.delete(like_obj)
        action = 'unliked'
    else:
        new_like = Like(user_id=current_user.id, song_id=song.id)
        db.session.add(new_like)
        action = 'liked'
        # 알림 생성 (노래 업로더에게 전달)
        msg = f"{current_user.username}님이 당신이 올린 노래 '{song.title}'을 좋아합니다."
        create_notification(song.user_id, current_user.id, msg, url_for('song_detail', song_id=song.id))
        
    db.session.commit()
    likes_count = Like.query.filter_by(song_id=song.id).count()
    return jsonify({'status': 'success', 'action': action, 'likes_count': likes_count})

@app.route('/song/<int:song_id>/comment', methods=['POST'])
@login_required
def add_comment(song_id):
    """댓글 작성 및 알림 발송 라우터입니다."""
    song = Song.query.get_or_404(song_id)
    content = request.form.get('content')
    
    if content:
        comment = Comment(content=content, user_id=current_user.id, song_id=song.id)
        db.session.add(comment)
        # 알림 생성 (노래 업로더에게 전달)
        msg = f"{current_user.username}님이 '{song.title}'에 댓글을 남겼습니다: \"{content[:15]}...\""
        create_notification(song.user_id, current_user.id, msg, url_for('song_detail', song_id=song.id))
        db.session.commit()
        flash('댓글이 등록되었습니다.', 'success')
        
    return redirect(url_for('song_detail', song_id=song.id))

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """댓글 작성자 또는 관리자만 가능한 댓글 삭제 라우터입니다."""
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id == current_user.id or current_user.is_admin:
        song_id = comment.song_id
        db.session.delete(comment)
        db.session.commit()
        flash('댓글이 삭제되었습니다.', 'success')
        return redirect(url_for('song_detail', song_id=song_id))
        
    flash('권한이 없습니다.', 'danger')
    return redirect(url_for('index'))

@app.route('/hashtag/<string:tag_name>')
def hashtag_songs(tag_name):
    """특정 해시태그를 포함한 곡 모아보기 목록입니다."""
    tag = Hashtag.query.filter_by(name=tag_name).first_or_404()
    # 지연 로딩 dynamic 형태를 활용하여 곡 쿼리
    songs = tag.songs.all()
    return render_template('index.html', recent_songs=songs, popular_songs=[], all_hashtags=[tag], active_tag=tag_name)

# --- 9단계: 알림 페이지 ---
@app.route('/notifications')
@login_required
def notifications_list():
    """모든 알림 목록 조회 및 자동 읽음 처리 화면입니다."""
    notis = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    
    # 일괄 읽음 처리
    for noti in notis:
        noti.is_read = True
    db.session.commit()
    
    return render_template('profile.html', notifications=notis, active_tab='notifications')

# --- 10단계: 프로필 페이지 ---
@app.route('/profile')
@login_required
def profile():
    """마이페이지 대시보드 뷰입니다."""
    my_songs = Song.query.filter_by(user_id=current_user.id).order_by(Song.created_at.desc()).all()
    # 내가 좋아요 한 노래들 조회
    liked_songs = Song.query.join(Like).filter(Like.user_id == current_user.id).all()
    my_comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()
    
    return render_template('profile.html', my_songs=my_songs, liked_songs=liked_songs, my_comments=my_comments, active_tab='dashboard')

@app.route('/profile/update-password', methods=['POST'])
@login_required
def update_password():
    """프로필 내 회원 비밀번호 수정 처리 라우터입니다."""
    old_pw = request.form.get('old_password')
    new_pw = request.form.get('new_password')
    
    if current_user.check_password(old_pw):
        current_user.set_password(new_pw)
        db.session.commit()
        flash('비밀번호가 안전하게 변경되었습니다.', 'success')
    else:
        flash('현재 비밀번호가 일치하지 않습니다.', 'danger')
        
    return redirect(url_for('profile'))

# --- 11단계: 관리자 기능 ---
@app.route('/admin')
@login_required
def admin_dashboard():
    """관리자용 대시보드 메인 뷰입니다."""
    if not current_user.is_admin:
        flash('관리자 권한이 필요합니다.', 'danger')
        return redirect(url_for('index'))
        
    users = User.query.all()
    songs = Song.query.all()
    return render_template('admin.html', users=users, songs=songs)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """관리자 권한 회원 삭제 라우터입니다."""
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(user_id)
    if user.username == 'admin':
        flash('기본 관리자 계정은 삭제할 수 없습니다.', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.username} 회원을 성공적으로 강제 탈퇴시켰습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/song/<int:song_id>/delete', methods=['POST'])
@login_required
def admin_delete_song(song_id):
    """관리자 권한 노래 삭제 라우터입니다."""
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    flash(f'"{song.title}" 곡이 삭제되었습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
