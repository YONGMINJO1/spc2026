const words = ['apple', 'light', 'water', 'music', 'grape'];
let answer = '';

let wrongCount = 0;
let usedLetters = [];
let currentWord = [];

function startGame() {
    answer = words[Math.floor(Math.random() * words.length)];

    currentWord = [];
    for (let i = 0; i < answer.length; i++) {
        currentWord.push('_');
    }

    wrongCount = 0;
    usedLetters = [];

    updateDisplay();
}

function updateDisplay() {
    document.getElementById('wordDisplay').textContent = currentWord.join(' ');
    document.getElementById('lives').textContent = 6 - wrongCount;
    document.getElementById('usedLetters').textContent = usedLetters.join(', ');
}

function guess() {
    const letter = document.getElementById('letterInput').value;

    if (usedLetters.includes(letter)) {
        return;
    }

    usedLetters.push(letter);

    if (answer.includes(letter)) {
        for (let i = 0; i < answer.length; i++) {
            if (answer[i] === letter) {
                currentWord[i] = letter;
            }
        }
    } else {
        wrongCount++;
    }
    if (!currentWord.includes('_')) {
        document.getElementById('message').textContent =
            `축하합니다. 단어는 ${answer} 였습니다.`;
    }
    if (wrongCount === 6) {
        document.getElementById('message').textContent =
            `게임 끝! 단어는 ${answer} 였습니다`;
    }

    document.getElementById('letterInput').value = '';
    updateDisplay();
}
document.addEventListener('DOMContentLoaded', () => {
    startGame();

    document.getElementById('guessButton').addEventListener('click', guess);
    document
        .getElementById('newGameButton')
        .addEventListener('click', startGame);
});
