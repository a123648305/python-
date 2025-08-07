from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

# 商品模型（对应数据库中的 items 表）
class Item(Base):
    __tablename__ = "items"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键
    name = Column(String(50), index=True)  # 商品名称
    price = Column(Float)  # 商品价格
    is_available = Column(Boolean, default=True)  # 是否可用
    description = Column(String(200), nullable=True)  # 商品描述（可为空）
