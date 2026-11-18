import sqlite3
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 新增

app = FastAPI(title="我的单词本 API")

# 👈 新增：允许所有前端网页来调用你的 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许任何人访问
    allow_methods=["*"],
    allow_headers=["*"],
)

class Database:
    def __init__(self, db_file: str):
        """这就是构造函数。每次实例化这个类的时候，都会执行这里"""
        self.db_file = db_file
        
    def init_table(self):
        """初始化建表"""
        # 使用 with 语句，Python 会在结束后自动帮你关闭连接，不用手动 close 了！
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    english TEXT PRIMARY KEY,
                    chinese TEXT NOT NULL
                )
            """)

    def get_words(self) -> dict:
        """查数据"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT english, chinese FROM words")
            rows = cursor.fetchall()
            # 这里用到了字典推导式
            return {row[0]: row[1] for row in rows}

    def add_word(self, english: str, chinese: str) -> bool:
        """增数据"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO words (english, chinese) VALUES (?, ?)", 
                    (english, chinese)
                )
            return True
        except Exception as e:
            print(f"数据库报错: {e}")
            return False