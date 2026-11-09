import sqlite3

# 1. 连接数据库（如果文件不存在，会自动创建）
conn = sqlite3.connect("test_words.db")
cursor = conn.cursor()

# 2. 建表（就像建一个 Excel 表格）
cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        english TEXT PRIMARY KEY,
        chinese TEXT NOT NULL
    )
""")

# 3. 插入一条数据（注意后面的问号，这是防黑客注入的防弹衣）
cursor.execute("INSERT OR REPLACE INTO words (english, chinese) VALUES (?, ?)", ("apple", "苹果"))

# 4. 提交修改（不写这句，数据不会真的存进去）
conn.commit()

# 5. 查询数据
cursor.execute("SELECT english, chinese FROM words")
rows = cursor.fetchall()
print("目前数据库里的数据：", rows)

# 6. 关门
conn.close()