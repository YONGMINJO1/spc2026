document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');
    const chatContainer = document.getElementById('chat-container');
    const chatList = document.getElementById('chat-list');
    const deleteBtn = document.getElementById('delete-btn');

    deleteBtn.addEventListener('click', async () => {
        if (!confirm('전체 채팅 내용을 삭제할까요?')) return;

        await fetch('/api/history', {
            method: 'DELETE',
        });

        resultDiv.innerHTML = '';
        chatList.innerHTML = '';
    });

    // 페이지 로드되자마자 사이드바 목록 불러오기
    async function loadChatList() {
        const response = await fetch('/api/history/title');
        const data = await response.json();

        chatList.innerHTML = '';

        const item = document.createElement('div');
        item.classList.add('chat-list-item');
        item.innerText = data.title;

        item.addEventListener('click', async () => {
            const res = await fetch('/api/history');
            const history = await res.json();

            resultDiv.innerHTML = '';
            history.forEach((msg) => {
                appendMessage(
                    msg.role === 'user' ? 'user' : 'bot',
                    msg.content,
                );
            });
        });

        chatList.appendChild(item);
    }

    loadChatList();

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value.trim();
        if (!chatMessage) return;

        appendMessage('user', chatMessage);
        chatInput.value = '';

        try {
            const replyText = await fetchChatbotReply(chatMessage);
            appendMessage('bot', replyText);
        } catch (error) {
            console.error('에러 발생:', error);
            appendMessage('bot', '죄송해요, 서버와 연결이 원활하지 않아요. 😢');
        }
    });

    async function fetchChatbotReply(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chatMessage: message }),
        });

        if (!response.ok) throw new Error('네트워크 응답에 문제가 있습니다.');

        const data = await response.json();
        return data.reply;
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        bubbleDiv.innerText = text;

        messageDiv.appendChild(bubbleDiv);
        resultDiv.appendChild(messageDiv);

        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
