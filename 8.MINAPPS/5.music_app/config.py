import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

class Config:
    """Flask 애플리케이션의 환경 설정을 관리하는 클래스입니다."""
    
    # 세션 및 보안 서명에 사용되는 비밀키
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-spc-2026')
    
    # SQLAlchemy 데이터베이스 URI 설정 (SQLite 기본값)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///music.db')
    
    # SQLAlchemy 객체 변경 추적 비활성화 (오버헤드 방지)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 유튜브 Data API v3 연동을 위한 API 키
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
