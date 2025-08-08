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

* ```fastapi 单部署~~~
  - 1. 保存依赖
    - `pip freeze > requirements.txt`
  - 2. 部署到 Docker
    - `docker build -t fastapi-demo .`
  - 3. 运行 Docker
    - `docker run -p 8000:8000 fastapi-demo`

  ```

* 一键 docker-compose 部署(fastApi + mysql)

  - 1. 配置 docker-compose.yml 文件
  - 2. 启动

  ```bash
  docker-compose up -d
  ```

* 配置 MySQL 允许远程连接
  默认情况下，MySQL 可能只允许本地连接，需要配置允许远程访问：
* 进入容器：

```bash
docker exec -it mysql-container bash
```

- 登录 MySQL：

```bash
mysql -u root -p

+ 输入你设置的 root 密码
+ 执行授权命令：
#sql-- 允许root用户从任何主机连接
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;

#如果你想限制特定 IP 访问，可以将 % 替换为具体 IP 地址
+ 退出 MySQL 和容器：
exit  # 退出MySQL
exit  # 退出容器
```
