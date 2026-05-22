from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='public', static_url_path='')

# history = []
conn = sqlite3.connect("chatgpt.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CAREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOONCREMENT
                    role TEXT NOT NULL,
                    content TEXT NOT NULL),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    }
        """)
    conn.commit()

@app.route('/')
def index():
    return send_from_directory('public','index.html')

@app.route('/api/chat', methods= ['POST'])
def chat():
    data = request.get_json()
    chat_message =data.get('chatMessage')
    # 사용자 저장
    cursor.execute("INSERT INTO (role, content) VALUES (?,?)",
                ("user",chat_message))
    conn.commit()

    # chatgpt 에게 물어보기...
    gpt_reply = ask_chatgpt(chat_message)
    cursor.execute("INSERT INTO history (role,content) VALUES(?,?)",
                ("assistant",gpt_reply))
    conn.commit()

    return jsonify({"reply": {gpt_reply}})

def ask_chatgpt():

    cursor.execute("SELECT role, content FROM history")
    rows = cursor.fetchall()

    history = [
        {"role": role, "content": content}
        for role, content in rows
    ]

    response = client.chat.completions.create( #호출하는 코드
            model="gpt-4o-mini",
            messages= [
                {"role": "system", "content":"당신은"},
                *history
            ]
    )
    print("출력확인: ", response)
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)