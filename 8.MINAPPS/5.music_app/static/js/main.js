// DOM 로드 완료 후 초기 바인딩 실행
document.addEventListener('DOMContentLoaded', () => {
    initSearch();
    initLikeButtons();
});

// 1. 유튜브 검색 관련 기능 초기화
function initSearch() {
    const searchBtn = document.getElementById('btn-youtube-search');
    const searchInput = document.getElementById('youtube-search-input');
    
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => performSearch(searchInput.value));
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch(searchInput.value);
            }
        });
    }
}

// 2. 비동기 유튜브 검색 실행 및 처리
function performSearch(query) {
    if (!query.strip().trim()) {
        alert('검색어를 입력해 주세요!');
        return;
    }
    
    const resultsContainer = document.getElementById('youtube-search-results');
    resultsContainer.innerHTML = `
        <div class="text-center my-4">
            <div class="spinner-border text-info" role="status"></div>
            <p class="mt-2 text-muted">유튜브 음악을 찾는 중...</p>
        </div>`;
        
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => renderSearchResults(data))
        .catch(err => {
            console.error('검색 실패:', err);
            resultsContainer.innerHTML = '<p class="text-danger text-center">검색 중 오류가 발생했습니다.</p>';
        });
}

// String 객체 헬퍼 정의
String.prototype.strip = function() {
    return this.replace(/^\s+|\s+$/g, "");
};

// 3. 유튜브 검색 결과 렌더링
function renderSearchResults(videos) {
    const container = document.getElementById('youtube-search-results');
    container.innerHTML = '';
    
    if (videos.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">검색 결과가 없습니다.</p>';
        return;
    }
    
    videos.forEach(video => {
        const card = createVideoResultCard(video);
        container.appendChild(card);
    });
}

// 4. 검색 결과 동적 카드 엘리먼트 생성
function createVideoResultCard(video) {
    const div = document.createElement('div');
    div.className = 'd-flex align-items-center mb-3 p-2 border border-secondary rounded bg-dark position-relative';
    div.style.cursor = 'pointer';
    div.innerHTML = `
        <img src="${video.thumbnail_url}" class="rounded me-3" style="width: 80px; height: 60px; object-fit: cover;">
        <div class="flex-grow-1 overflow-hidden" style="padding-right: 80px;">
            <h6 class="text-white text-truncate mb-1">${video.title}</h6>
            <small class="text-muted">${video.artist}</small>
        </div>
        <button class="btn btn-sm btn-outline-info position-absolute end-0 me-3">선택</button>
    `;
    div.addEventListener('click', () => selectVideoForRegister(video));
    return div;
}

// 5. 노래 카드 클릭 시 등록 양식에 매핑
function selectVideoForRegister(video) {
    document.getElementById('reg-title').value = video.title;
    document.getElementById('reg-artist').value = video.artist;
    document.getElementById('reg-video-id').value = video.youtube_video_id;
    document.getElementById('reg-thumbnail').value = video.thumbnail_url;
    
    // 등록 상세 폼 영역 활성화
    document.getElementById('register-details-form').classList.remove('d-none');
    
    // 결과창에 선택 표시 반영
    const container = document.getElementById('youtube-search-results');
    container.innerHTML = `
        <div class="alert alert-success d-flex align-items-center" role="alert">
            <i class="bi bi-check-circle-fill me-2 fs-5"></i>
            <div>선택된 곡: <strong>${video.title}</strong></div>
        </div>
    `;
}

// 6. 비동기 좋아요 버튼 토글 이벤트 초기화
function initLikeButtons() {
    const likeBtn = document.getElementById('btn-like-toggle');
    if (likeBtn) {
        likeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const songId = likeBtn.getAttribute('data-song-id');
            toggleLike(songId, likeBtn);
        });
    }
}

// 7. 비동기 좋아요 요청 발송 및 UI 전환
function toggleLike(songId, button) {
    fetch(`/song/${songId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            updateLikeUI(button, data.action, data.likes_count);
        }
    })
    .catch(err => console.error('좋아요 토글 실패:', err));
}

// 8. 좋아요 UI 상태 업데이트 및 하트 진동 애니메이션 부여
function updateLikeUI(button, action, likesCount) {
    const icon = button.querySelector('i');
    const textSpan = button.querySelector('.likes-count');
    
    // 하트 펄스 애니메이션 일시 부여
    button.classList.add('heart-pulse');
    setTimeout(() => button.classList.remove('heart-pulse'), 300);
    
    if (action === 'liked') {
        icon.className = 'bi bi-heart-fill me-2';
        button.className = 'btn btn-pink d-flex align-items-center';
    } else {
        icon.className = 'bi bi-heart me-2';
        button.className = 'btn btn-outline-light d-flex align-items-center';
    }
    
    if (textSpan) {
        textSpan.textContent = likesCount;
    }
}
