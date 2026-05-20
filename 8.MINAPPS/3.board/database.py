import sqlite3

class MyDatabase():
    def __init__(self):
        self.db = sqlite3.connect('board.sqlite', check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def execute(self,query, args={}):
        self.cursor.execute(query,args)

    def execute_fetch(self,query, args={}):
        self.cursor.execute(query,args)
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.db.commit()

# def init_db():
#     print("초기화 추가")
#     return

# print("여기는 이 파일이 불릴때")

if __name__ == "__main__":
    print("여기는 DB테스트")
    # 미니 유닛 테스트
    db = MyDatabase()
    db.execute("CREATE TABLE board (id INTEGER PRIMARY KEY, title VARCHAR(50),message VARCHAR(200))")
    db.execute("INSERT INTO board(title, message) VALUES(?,?)",("title","message"))
    db.commit()
    result = db.execute_fetch("SELECT * FROM board")
    print(result)
    db.execute("DELETE FROM board")
    db.commit()