-- sqlite3 board.sqlite < init-database.sql

DROP TABLE IF EXISTS board

CREATE TABLE board (
    id INTEGER PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    message VARCHAR(200)
    )