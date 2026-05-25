document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');
    const chatContainer = document.getElementById('chat-container');

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
