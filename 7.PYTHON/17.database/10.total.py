import sqlite3

def connect_db():
    return sqlite3.connect('example.db')

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL)
                """)
    conn.commit()
    conn.close()


def insert_user(name,age):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                    INSERT INTO users (name,age) VALUES (?, ?)
                    """,(name,age))
    conn.commit()
    conn.close()

def get_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall() # 모두
    conn.close()
    return rows

def get_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE name=?',(name ,))
    user = cur.fetchall() # 모두
    conn.close()
    return user

def update_user(name, new_age):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE users SET age=? WHERE name=?',(new_age,name))
    conn.close()