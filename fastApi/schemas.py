from pydantic import BaseModel
from typing import Optional

# 基础模型（共享属性）
class ItemBase(BaseModel):
    name: str
    price: float
    is_available: Optional[bool] = True
    description: Optional[str] = None

# 创建商品时的模型（不需要 id，由数据库自动生成）
class ItemCreate(ItemBase):
    pass

# 更新商品时的模型（所有字段可选）
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    description: Optional[str] = None

# 数据库模型对应的响应模型（包含 id）
class Item(ItemBase):
    id: int

    # 配置：允许从 ORM 模型实例创建 Pydantic 模型
    class Config:
        orm_mode = True
