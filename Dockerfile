FROM python:3.12-slim

WORKDIR /app

# 1. 拷贝依赖清单，并用清华源安装
COPY requirements.txt .
# 加了 --only-binary=:all: 意思是：如果对方只有源码包，直接报错，绝不卡死！
# 顺便把 pip 升级到最新版，加快解析速度
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt --only-binary=:all: -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 拷贝你的核心代码
COPY api.py ./

# 3. 告诉 Docker 我们的服务跑在 8000 端口
EXPOSE 8000

# 4. 启动命令（注意这里一定要写 --host 0.0.0.0）
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]