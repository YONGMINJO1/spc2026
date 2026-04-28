let interval;
let timerId;
const timeInput = document.getElementById('timeInput');
const progress = document.getElementById('progress'); // 진행률 바
const progressText = document.getElementById('progressText');
const startButton = document.getElementById('startButton');
const clearButton = document.getElementById('clearButton');

startButton.addEventListener('click', startProgress);
clearButton.addEventListener('click', clearProgress);

function startProgress() {
    duration = parseInt(timeInput.value);
    console.log('입력초: ', duration);

    let elapsed = 0; /* 초과시간 */
    timerId = setInterval(() => {
        elapsed++;

        const ratio = Math.floor((elapsed / duration) * 100);
        progress.style.width = `${ratio}%`;
        progressText.textContent = `${ratio}%`;
        //console.log('반복호출');

        if (ratio >= 100) {
            // 타이머 중지
            clearInterval(timerId);
        }
    }, 1000);
}

function clearProgress() {
    if (timerId) clearInterval(timerId);
    progress.style.width = '2px';
    timeInput.value = ' ';
    progressText.textContent = `0%`;
}
