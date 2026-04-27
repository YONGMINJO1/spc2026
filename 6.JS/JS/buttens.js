        // 각자의 버튼이 눌릴때마다 위에 div의 값을 가져다가 +1 또는 -1
        function increase () {
            //console.log("+1 클릭");
            const result = document.getElementById('result');
            let value = parseInt(result.textContent);
            console.log(result.textContent);
            result.textContent = value + 1;
        }

        function decrease () {
            document.getElementById("result").textContent -= 1
        }

        const button1 = document.getElementById('incButton');
        const button2 = document.getElementById('decButton');

        button1.addEventListener('click', () =>  {
            document.getElementById('result').textContent = parseInt(result.textContent) + 1;
        });

        button2.addEventListener('click',  () => {
            document.getElementById("result").textContent -= 1
        });