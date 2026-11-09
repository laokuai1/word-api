import os
import pytest
from fastapi.testclient import TestClient

os.environ["DB_FILE"] = "test_words.db"

from api import app, init_db, DB_FILE

client = TestClient(app)

# 每次跑测试前，先清理旧数据，再建空表
@pytest.fixture(autouse=True)
def setup_database():
    # 👈 核心新增：如果测试库存在，先删掉它，保证每次都是干净的白纸
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    init_db() # 建新表
    yield
    # 测试跑完后，再删一次，不留垃圾
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

# 测试 1：测试 GET 接口（初始应该是空的）
def test_get_empty_words():
    response = client.get("/words")
    assert response.status_code == 200
    assert response.json() == {}

# 测试 2：测试 POST 添加单词
def test_add_word():
    response = client.post("/words", json={"english": "test", "chinese": "测试"})
    assert response.status_code == 200
    assert "成功" in response.json()["message"]

# 测试 3：添加后再查询，看看数据对不对
def test_add_and_get():
    client.post("/words", json={"english": "apple", "chinese": "苹果"})
    response = client.get("/words")
    assert response.status_code == 200
    assert response.json() == {"apple": "苹果"}