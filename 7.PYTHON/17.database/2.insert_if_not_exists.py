import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서라는 객체를 통해서.. 실제 데이터 입출력을 함..
cur = conn.cursor()


cur.execute('SELECT COUNT(*) FROM users')
count = cur.fetchone()[0]
print(count)

if count == 0:
    cur.execute("""
                INSERT INTO users (name,age) VALUES (?, ?)
                """,('Alice',30))
else:
    print("이미 테이블에 데이터가 있습니다.")
conn.commit()

conn.close()