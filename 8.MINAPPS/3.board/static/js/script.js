// console.log('나 불럿니?');
document.addEventListener('DOMContentLoaded', async ()=>{
    const res = await fetch('/list')
    const data = res.json();
    console.log(data)
    const result = document.getElementById('card-list')

    data.forEach (post => {
        makeCard(post.id, post.title,post.message)
    })
})

function makeCard(id, title,message){
    const card = document.createElement('div');
    card.innerHTML= `
        <div>
            <div>
            
            <div>
        </div>
    `
}

document.getElementById('input-sumit').addEventListener('click', ()=>{
    const title = document.getElementById('input-title').values;
    const message = document.getElementById('input-text').values;

    fetch('/create', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({title},{message})
    })
})