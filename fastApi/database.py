from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库配置
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# 数据库连接 URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"数据库连接 URL: {SQLALCHEMY_DATABASE_URL}")

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建会话本地类（每次请求创建一个会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类（所有模型继承此类）
Base = declarative_base()



# 创建数据库表
Base.metadata.create_all(bind=engine)


# 依赖项：获取数据库会话（每个请求一个会话）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # 请求结束后关闭会话