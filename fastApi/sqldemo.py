from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化 FastAPI 应用
app = FastAPI(title="FastAPI MySQL Example")

# 数据库配置 - 从环境变量读取
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/dbname")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话本地类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

# 定义数据模型
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(Float)
    stock = Column(Integer)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# Pydantic 模型 - 用于数据验证和序列化
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

# 依赖项 - 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API 路由

# 创建产品
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 获取所有产品
@app.get("/products/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# 获取单个产品
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 更新产品
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

# 删除产品
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}
