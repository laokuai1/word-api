import sqlite3
import os

class WordDatabase:
    def __init__(self, db_file: str):
        """初始化数据库管理类，记住文件路径"""
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """初始化建表逻辑"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # 1. 建老表
            cursor.execute("CREATE TABLE IF NOT EXISTS words (english TEXT PRIMARY KEY, chinese TEXT NOT NULL)")
            # 2. 建分类表
            cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
            # 3. 建关联表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS words_v2 (
                    english TEXT PRIMARY KEY, chinese TEXT NOT NULL, category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
            # 4. 灌入初始数据
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO categories (id, name) VALUES (1, '水果'), (2, '动物'), (3, '科技')")
                cursor.execute("INSERT INTO words_v2 (english, chinese, category_id) VALUES ('apple', '苹果', 1), ('banana', '香蕉', 1), ('cat', '猫', 2), ('computer', '电脑', 3)")

    def get_all_words(self) -> dict:
        """查 words 表"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT english, chinese FROM words")
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}

    def add_word(self, english: str, chinese: str):
        """增 words 表"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO words (english, chinese) VALUES (?, ?)", (english, chinese))

    def get_words_by_category(self, category_name: str) -> list:
        """联表查 words_v2"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT words_v2.english, words_v2.chinese, categories.name 
                FROM words_v2
                INNER JOIN categories ON words_v2.category_id = categories.id
                WHERE categories.name = ?
            """, (category_name,))
            rows = cursor.fetchall()
            
            # 把查出来的数据整理成列表字典
            return [{"english": row[0], "chinese": row[1], "category": row[2]} for row in rows]