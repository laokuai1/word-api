import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="我的单词本 API (SQLite 版)")

#DB_FILE = "words.db"
import os
# 如果环境变量里有 TEST_DB，就用测试库；否则用正式库
DB_FILE = os.getenv("DB_FILE", "words.db")

# 1. 初始化数据库：建表
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            english TEXT PRIMARY KEY,
            chinese TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 启动时建表
init_db()

class WordItem(BaseModel):
    english: str
    chinese: str

# 2. 查数据
@app.get("/words")
def get_all_words():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT english, chinese FROM words")
    rows = cursor.fetchall()
    conn.close()
    
    # 把 [('apple', '苹果')] 转换成 {"apple": "苹果"} 给前端
    return {row[0]: row[1] for row in rows}

# 3. 写数据
@app.post("/words")
def add_word(item: WordItem):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO words (english, chinese) VALUES (?, ?)",
        (item.english, item.chinese)
    )
    conn.commit()
    conn.close()
    
    return {"message": f"成功写入数据库：{item.english} -> {item.chinese}"}