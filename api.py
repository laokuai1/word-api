import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="我的单词本 API") # 这就是咱们的后端服务大管家

DATA_FILE = "words.json"

# 1. 还是读取数据的逻辑
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        word_dict = json.load(f)
else:
    word_dict = {}

# 2. 定义添加单词时，客户端需要传过来的数据格式
class WordItem(BaseModel):
    english: str
    chinese: str


# 3. 接口一：获取所有单词 (GET 请求)
@app.get("/words")
def get_all_words():
    """客户端访问 /words 时，返回所有的单词"""
    return word_dict


# 4. 接口二：添加新单词 (POST 请求)
@app.post("/words")
def add_word(item: WordItem):
    """客户端往 /words 发数据时，添加到单词本里"""
    word_dict[item.english] = item.chinese
    
    # 存盘
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(word_dict, f, ensure_ascii=False, indent=4)
        
    return {"message": f"成功添加：{item.english} -> {item.chinese}"}