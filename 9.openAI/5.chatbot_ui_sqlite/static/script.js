document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value;
        // console.log(chatMessage); 실무적으로 X

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatMessage }),
        });

        const data = await response.json();
        console.log(response);

        // .then((response) => response.json())
        // .then(
        //     (data) => console.log(data), // Promise <Pending>
        // );

        const chatbotReply = document.createElement('p');
        chatbotReply.innerText = data.reply;
        resultDiv.appendChild(chatbotReply);
    });

    // TODO - 위에 리팩토링해서 적절하게 분리.. fetch 하는거 분리하고 응답 받아서 .DOM 그리는것 나누기
});
