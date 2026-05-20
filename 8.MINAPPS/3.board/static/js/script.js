// console.log('나 불럿니?');
document.addEventListener('DOMContentLoaded', async () => {
    const res = await fetch('/list');
    const data = await res.json();
    console.log(data);
    const result = document.getElementById('card-list');

    data.forEach((post) => {
        makeCard(post.id, post.title, post.message);
    });
});

function makeCard(id, title, message) {
    const card = document.createElement('div');
    card.className = 'col-6';
    card.innerHTML = `
    <div class="card m-2">
        <div class="card-body">
            <p>${title}</p>
            <p>${message}</p>
            <button class="modify-btn btn btn-warning">수정</button>
            <button class="delete-btn btn btn-danger">삭제</button>
        </div>
    </div>
    `;

    const modifyBtn = card.querySelector('.modify-btn');

    modifyBtn.addEventListener('click', async () => {
        // 버튼 눌림 확인
        //console.log('수정할 id', id);

        card.innerHTML = `
            <div class="card m-2">
                <div class="card-body">
                    <input value="${title}" id="modify-title-${id}" class="form-control mb-2"/>
                    <input value="${message}" id="modify-message-${id}" class="form-control mb-2"/>
                    <button class="save-btn btn btn-primary">저장</button>
                </div>
            </div>
            `;
        const saveBtn = card.querySelector('.save-btn');

        saveBtn.addEventListener('click', async () => {
            const newTitle = document.getElementById(
                `modify-title-${id}`,
            ).value;
            const newMessage = document.getElementById(
                `modify-message-${id}`,
            ).value;

            await fetch('/modify', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id: id,
                    title: newTitle,
                    message: newMessage,
                }),
            });
            location.reload();

            // 수정 내용 확인용
            //console.log('수정할 id', id, newTitle, newMessage);
        });
    });

    const deleteBtn = card.querySelector('.delete-btn');

    deleteBtn.addEventListener('click', async () => {
        // 버튼 눌림 확인
        //console.log('삭제할 id', id);
        await fetch('/delete', {
            method: 'DELETE',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ id: id }),
        });
        location.reload();
    });
    document.getElementById('card-list').appendChild(card);
}

document.getElementById('input-submit').addEventListener('click', async () => {
    const title = document.getElementById('input-title').value;
    const message = document.getElementById('input-text').value;

    await fetch('/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, message }),
    });
    location.reload();
});
