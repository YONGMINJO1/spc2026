import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서라는 객체를 통해서.. 실제 데이터 입출력을 함..
cur = conn.cursor()

cur.execute("""
            UPDATE users SET age=28 WHERE name= 'Bob'
            """)
cur.execute("""
            UPDATE users SET age=? WHERE name= '?'
            """,(33,'Bob'))



conn.commit()
conn.close()