## 项目介绍

- 结构介绍
  本项目使用 FastAPI 框架，FastAPI 是一个现代、高性能的 Python Web 框架，专为构建 API 设计，自 2018 年推出以来迅速成为开发者的热门选择。它结合了快速开发、自动文档生成、类型提示和异步支持等特性，非常适合构建 RESTful API、微服务和高性能后端服务。

- 安装

  - 1. 安装 FastAPI

  ```
    pip install fastapi uvicorn
  ```

  - 2.启动服务

  ```
    py app.py
  ```

- 访问
  - 1. 访问 FastAPI 文档
    - 直接访问 `http://localhost:8000/docs`
  - 2. 访问 ReDoc
    - 直接访问 `http://localhost:8000/redoc`
  - 3. 访问 API
    - 直接访问 `http://localhost:8000/items`


+ 部署
  - 1. 保存依赖
    - `pip freeze > requirements.txt`
  - 2. 部署到 Docker
    - `docker build -t fastapi-demo .`
  - 3. 运行 Docker
    - `docker run -p 8000:8000 fastapi-demo`