import os
import requests
from models import db, Notification

# 유튜브 API 키 로드
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

def get_mock_videos(query):
    """유튜브 API 호출 실패 또는 키 누락 시 반환할 음악 Mock 데이터 목록입니다."""
    mock_data = [
        {
            'youtube_video_id': 'kJQP7kiw5Fk',
            'title': 'Luis Fonsi - Despacito ft. Daddy Yankee',
            'artist': 'Luis Fonsi',
            'thumbnail_url': 'https://img.youtube.com/vi/kJQP7kiw5Fk/0.jpg'
        },
        {
            'youtube_video_id': 'OPf0YbXqDm0',
            'title': 'Mark Ronson - Uptown Funk ft. Bruno Mars',
            'artist': 'Mark Ronson',
            'thumbnail_url': 'https://img.youtube.com/vi/OPf0YbXqDm0/0.jpg'
        },
        {
            'youtube_video_id': 'JGwWNGJdvx8',
            'title': 'Ed Sheeran - Shape of You [Official Video]',
            'artist': 'Ed Sheeran',
            'thumbnail_url': 'https://img.youtube.com/vi/JGwWNGJdvx8/0.jpg'
        }
    ]
    # 검색어가 포함된 항목 필터링 (대소문자 구분 없음)
    filtered = [v for v in mock_data if query.lower() in v['title'].lower() or query.lower() in v['artist'].lower()]
    return filtered if filtered else mock_data


def search_youtube_videos(query):
    """유튜브 Data API v3를 활용하여 동영상을 검색합니다.
    API 키가 없거나 예외 발생 시 Mock 데이터를 안전하게 반환합니다.
    """
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == 'YOUR_YOUTUBE_API_KEY':
        return get_mock_videos(query)
        
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 5,
        'key': YOUTUBE_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return parse_youtube_response(response.json())
        return get_mock_videos(query)
    except Exception:
        return get_mock_videos(query)


def parse_youtube_response(data):
    """유튜브 검색 API 응답 데이터를 필요한 구조로 변환합니다."""
    videos = []
    for item in data.get('items', []):
        snippet = item.get('snippet', {})
        video_id = item.get('id', {}).get('videoId')
        title = snippet.get('title', '알 수 없는 제목')
        artist = snippet.get('channelTitle', '알 수 없는 아티스트')
        thumbnail_url = snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
        
        if video_id:
            videos.append({
                'youtube_video_id': video_id,
                'title': title,
                'artist': artist,
                'thumbnail_url': thumbnail_url
            })
    return videos


def parse_hashtags(hashtag_str):
    """공백, 쉼표 등으로 분리된 해시태그 문자열을 정제된 리스트로 파싱합니다."""
    if not hashtag_str:
        return []
    # 쉼표를 공백으로 치환 후 분리
    raw_tags = hashtag_str.replace(',', ' ').split()
    tags = []
    for tag in raw_tags:
        clean_tag = tag.strip().replace('#', '')
        if clean_tag and clean_tag not in tags:
            tags.append(clean_tag)
    return tags


def create_notification(user_id, sender_id, message, redirect_url=None):
    """새로운 비동기 알림 레코드를 데이터베이스에 생성하여 저장합니다."""
    # 본인이 발생시킨 행위(예: 자신이 올린 곡에 자신의 좋아요 등)는 알림을 생성하지 않음
    if user_id == sender_id:
        return None
        
    noti = Notification(
        user_id=user_id,
        sender_id=sender_id,
        message=message,
        redirect_url=redirect_url
    )
    db.session.add(noti)
    db.session.commit()
    return noti
