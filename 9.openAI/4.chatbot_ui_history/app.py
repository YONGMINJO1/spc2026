from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='public', static_url_path='')

history = []

@app.route('/')
def index():
    return send_from_directory('public','index.html')

@app.route('/api/chat', methods= ['POST'])
def chat():
    data = request.get_json()
    chat_message =data.get('chatMessage')
    #return jsonify({"reply": f'당신의 메시지는 : {chat_message}'})
    history.append({"role":"user", "content":chat_message})
    
    history.append({"role":"assistant", "content":chat_message})

    # chatgpt 에게 물어보기...

    gpt_reply = ask_chatgpt(chat_message)
    return jsonify({"reply": f'당신의 메시지는 : {gpt_reply}'})

def ask_chatgpt(chat_message):

    gpt_ask_message = [
        {'route'}
    ] 

    response = client.chat.completions.create( #호출하는 코드
            model="gpt-4o",
            messages= [
                {"role": "system", "content":"당신은"},
                *history
            ]
    )
    print("출력확인: ", response)
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)