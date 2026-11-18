import sqlite3
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="我的专属单词本")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

DB_FILE = os.getenv("DB_FILE", "words.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 1. 建老表
    cursor.execute("CREATE TABLE IF NOT EXISTS words (english TEXT PRIMARY KEY, chinese TEXT NOT NULL)")
    # 2. 建分类表
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    # 3. 建关联表（就是这个 words_v2 刚才找不到）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words_v2 (
            english TEXT PRIMARY KEY, chinese TEXT NOT NULL, category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    # 4. 灌入初始数据（如果没数据的话）
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO categories (id, name) VALUES (1, '水果'), (2, '动物'), (3, '科技')")
        cursor.execute("INSERT INTO words_v2 (english, chinese, category_id) VALUES ('apple', '苹果', 1), ('banana', '香蕉', 1), ('cat', '猫', 2), ('computer', '电脑', 3)")
    conn.commit()
    conn.close()

# 👇 启动时立刻建表
init_db()

class WordItem(BaseModel):
    english: str
    chinese: str

@app.get("/words")
def get_all_words():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT english, chinese FROM words")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

@app.post("/words")
def add_word(item: WordItem):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO words (english, chinese) VALUES (?, ?)", (item.english, item.chinese))
    conn.commit()
    conn.close()
    return {"message": f"成功写入：{item.english} -> {item.chinese}"}

@app.get("/words/{category_name}")
def get_words_by_category(category_name: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT words_v2.english, words_v2.chinese, categories.name 
        FROM words_v2
        INNER JOIN categories ON words_v2.category_id = categories.id
        WHERE categories.name = ?
    """, (category_name,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return {"message": f"没有找到分类为【{category_name}】的单词"}
    
    result = [{"english": row[0], "chinese": row[1], "category": row[2]} for row in rows]
    return {"category": category_name, "words": result}