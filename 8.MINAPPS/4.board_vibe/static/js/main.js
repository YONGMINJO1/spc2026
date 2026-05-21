document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const postForm = document.getElementById('postForm');
    const titleInput = document.getElementById('title');
    const messageInput = document.getElementById('message');
    const postsGrid = document.getElementById('postsGrid');
    const postCountBadge = document.getElementById('postCount');
    const submitBtn = document.getElementById('submitBtn');
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');

    // Global Post Count
    let totalPostsCount = 0;

    // Toast Notification System
    function showToast(message, isError = false) {
        toastMessage.textContent = message;
        if (isError) {
            toast.classList.add('error');
            toastIcon.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i>';
        } else {
            toast.classList.remove('error');
            toastIcon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        }
        
        toast.classList.remove('hidden');
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }

    // Format Date string to a sleek format (e.g., 2026.05.21 11:45)
    function formatDate(dateStr) {
        try {
            // SQLite TIMESTAMP defaults to UTC (e.g. "2026-05-21 02:40:18")
            // Parse and translate to local timezone
            let date;
            if (dateStr.includes('T')) {
                date = new Date(dateStr);
            } else {
                // SQLite default space separator instead of 'T'
                date = new Date(dateStr.replace(' ', 'T') + 'Z'); 
            }
            
            if (isNaN(date.getTime())) {
                return dateStr;
            }
            
            const yyyy = date.getFullYear();
            const mm = String(date.getMonth() + 1).padStart(2, '0');
            const dd = String(date.getDate()).padStart(2, '0');
            const hh = String(date.getHours()).padStart(2, '0');
            const min = String(date.getMinutes()).padStart(2, '0');
            
            return `${yyyy}.${mm}.${dd} ${hh}:${min}`;
        } catch (e) {
            return dateStr;
        }
    }

    // Create a Post Card Element
    function createPostCardElement(post) {
        const card = document.createElement('div');
        card.className = 'glass-card post-card';
        card.id = `post-${post.id}`;
        
        card.innerHTML = `
            <div class="post-card-body">
                <div class="post-meta">
                    <span class="post-date">
                        <i class="fa-regular fa-clock"></i> ${formatDate(post.created_at)}
                    </span>
                    <button class="btn-delete" title="바이브 삭제" data-id="${post.id}">
                        <i class="fa-regular fa-trash-can"></i>
                    </button>
                </div>
                <h4 class="post-title">${escapeHTML(post.title)}</h4>
                <p class="post-message">${escapeHTML(post.message)}</p>
            </div>
            <div class="post-card-footer">
                <div class="post-likes">
                    <button class="btn-like" data-id="${post.id}">
                        <i class="fa-regular fa-heart"></i>
                        <span class="like-count">${post.likes}</span>
                    </button>
                </div>
                <span class="post-author-badge">VIBE #${post.id}</span>
            </div>
        `;

        // Bind delete event
        const deleteBtn = card.querySelector('.btn-delete');
        deleteBtn.addEventListener('click', () => deletePost(post.id, card));

        // Bind like event
        const likeBtn = card.querySelector('.btn-like');
        likeBtn.addEventListener('click', () => likePost(post.id, likeBtn));

        return card;
    }

    // Helper to Escape HTML inputs to prevent XSS
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Fetch and render all posts
    async function fetchPosts() {
        try {
            const response = await fetch('/api/posts');
            if (!response.ok) throw new Error('바이브 목록을 가져오는데 실패했습니다.');
            
            const posts = await response.json();
            postsGrid.innerHTML = '';
            
            totalPostsCount = posts.length;
            postCountBadge.textContent = totalPostsCount;

            if (posts.length === 0) {
                renderEmptyState();
                return;
            }

            posts.forEach(post => {
                const cardElement = createPostCardElement(post);
                postsGrid.appendChild(cardElement);
            });
        } catch (error) {
            console.error(error);
            postsGrid.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-circle-exclamation" style="color: var(--neon-rose)"></i>
                    <h4>에러 발생</h4>
                    <p>${error.message}</p>
                </div>
            `;
        }
    }

    // Render Empty State UI
    function renderEmptyState() {
        postsGrid.innerHTML = `
            <div class="empty-state">
                <i class="fa-regular fa-lightbulb"></i>
                <h4>아직 등록된 바이브가 없습니다.</h4>
                <p>가장 먼저 매력적인 한마디를 남겨보세요!</p>
            </div>
        `;
    }

    // Handle Form Submission
    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = titleInput.value.trim();
        const message = messageInput.value.trim();

        // Validation Check
        if (!title) {
            showToast('제목을 입력해주세요!', true);
            titleInput.focus();
            return;
        }
        if (!message) {
            showToast('메시지를 입력해주세요!', true);
            messageInput.focus();
            return;
        }

        // Set Loading State
        submitBtn.disabled = true;
        const originalBtnContent = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span>등록 중...</span> <i class="fa-solid fa-spinner fa-spin"></i>';

        try {
            const response = await fetch('/api/posts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, message })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || '바이브 등록에 실패했습니다.');
            }

            const newPost = await response.json();
            
            // If empty state was active, clear it
            if (totalPostsCount === 0) {
                postsGrid.innerHTML = '';
            }

            // Update badge counts
            totalPostsCount += 1;
            postCountBadge.textContent = totalPostsCount;

            // Prepend new card with a nice transition
            const newCard = createPostCardElement(newPost);
            postsGrid.insertBefore(newCard, postsGrid.firstChild);

            // Clean inputs
            postForm.reset();
            showToast('성공적으로 새로운 바이브가 등록되었습니다! ✨');

        } catch (error) {
            console.error(error);
            showToast(error.message, true);
        } finally {
            // Restore button state
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnContent;
        }
    });

    // Handle Likes via API
    async function likePost(id, buttonEl) {
        const heartIcon = buttonEl.querySelector('i');
        const countSpan = buttonEl.querySelector('.like-count');
        
        // Add micro-animation effect
        heartIcon.classList.add('heart-pop');
        heartIcon.className = 'fa-solid fa-heart'; // Turn into solid heart
        
        // Remove animation class after it completes to allow triggering again
        setTimeout(() => {
            heartIcon.classList.remove('heart-pop');
        }, 400);

        try {
            const response = await fetch(`/api/posts/${id}/like`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error();
            const data = await response.json();
            
            countSpan.textContent = data.likes;
        } catch (error) {
            console.error('Failed to like post:', error);
            showToast('좋아요 등록 과정에 문제가 발생했습니다.', true);
            // Revert icon look
            heartIcon.className = 'fa-regular fa-heart';
        }
    }

    // Handle Delete via API
    async function deletePost(id, cardEl) {
        if (!confirm('이 바이브를 삭제하시겠습니까? 😢')) return;

        try {
            const response = await fetch(`/api/posts/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('바이브 삭제에 실패했습니다.');
            
            // Add exit animation class
            cardEl.classList.add('deleting');
            
            // Remove from DOM after CSS transition completes
            setTimeout(() => {
                cardEl.remove();
                totalPostsCount -= 1;
                postCountBadge.textContent = totalPostsCount;
                
                if (totalPostsCount === 0) {
                    renderEmptyState();
                }
            }, 400);

            showToast('바이브가 깔끔하게 삭제되었습니다.');
        } catch (error) {
            console.error(error);
            showToast(error.message, true);
        }
    }

    // Initialize Posts Load
    fetchPosts();
});
