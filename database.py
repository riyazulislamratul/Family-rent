import sqlite3

db = sqlite3.connect("database.db")

db.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

db.execute("""
CREATE TABLE records (
    id INTEGER PRIMARY KEY,
    name TEXT,
    amount INTEGER,
    date TEXT
)
""")

db.close()