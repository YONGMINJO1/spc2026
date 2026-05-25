from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# static 폴더 경로와 그 prefix를 결정(변경) 할 수 있음
app = Flask(__name__, static_folder="public", static_url_path="")

# history = [] 이거를 대체할 DB 코드에 넣기
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


init_db()


@app.route("/")
def index():
    return send_from_directory("public", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    chat_message = data.get("chatMessage")
    # 사용자 저장
    cursor.execute("INSERT INTO (role, content) VALUES (?,?)", ("user", chat_message))
    conn.commit()

    # chatgpt 에게 물어보기...
    gpt_reply = ask_chatgpt(chat_message)
    cursor.execute(
        "INSERT INTO history (role,content) VALUES(?,?)", ("assistant", gpt_reply)
    )
    conn.commit()

    return jsonify({"reply": {gpt_reply}})


def ask_chatgpt():

    cursor.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    print("원본 쿼리문:", rows)
    rows = rows[::-1]  # 역순으로 다시 배열에 넣기
    print("역순 쿼리문:", rows)

    rows_dict = [{"role": row["role"], "content": row["content"]} for row in rows]
    print("-" * 30)
    print(rows_dict)
    # history = [
    #     {"role": role, "content": content}
    #     for role, content in rows
    # ]

    gpt_ask_message = [
        {
            "role": "system",
            "content": "당신은 친절한 챗봇입니다. 경상도 사투리를 적절하게 섞어서 답변하시오.",
        },
        *rows_dict,
    ]
    # 이거를 대체할 SQL SELECT 구문 넣기...

    print(">>>>>>>>>>")
    print("최종 GPT 에게 우리가 물어볼 전체 메시지: ", gpt_ask_message)
    print("<<<<<<<<<<")

    response = client.chat.completions.create(  # 호출하는 코드
        model="gpt-4o-mini",
        messages=gpt_ask_message,
        # messages= [
        #     {"role": "system", "content":"당신은"},
        #     *history
        # ]
    )
    print("출력확인: ", response)
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
