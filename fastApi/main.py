import os
from fastapi import FastAPI, HTTPException,status,Depends
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from typing import Generic, TypeVar, Optional

# # 导入SQl模块
from database import get_db,Session
from models import TableItem

# 初始化 FastAPI 应用
app = FastAPI(title="物品管理 API", version="1.0")

# 定义通用数据类型
T = TypeVar('T')

# 统一响应模型
class TypeResponse(BaseModel, Generic[T]):
    code: int = status.HTTP_200_OK  # 状态码（默认 200）
    message: str = "success"        # 消息（默认成功）
    data: Optional[T] = None        # 数据（泛型，支持任意类型）


# 定义数据模型（用于请求验证和响应格式化）
class Item(BaseModel):
    name: str
    price: float
    id: Optional[int] = 0  # 可选字段

# 模拟数据库
fake_db: List[Item] = [
    {
        "id": 1,
        "name": "物品 1",
        "price": 10.99
    }
]




@app.get("/", response_class=HTMLResponse)
async def root():
    # 检查文件是否存在
    filePath = './static/index.html'
    if not os.path.exists(filePath):
        return HTMLResponse(content="<h1>HTML 文件不存在</h1>", status_code=404)
    
    # 读取 HTML 文件内容
    with open(filePath, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 返回 HTML 内容
    return HTMLResponse(content=html_content)

# 路由：获取所有物品
@app.get("/list", response_model=TypeResponse[List[Item]],status_code=200)
async def read_items(page: int = 1, limit: int = 100, db:Session = Depends(get_db)):
    products = db.query(TableItem).offset(page).limit(limit).all()
    return TypeResponse(data=products)

# 路由：创建新物品
@app.post("/add_item", status_code=201)
async def create_item(data: Item,db:Session = Depends(get_db)):
    body = data.model_dump() # 将数据转为字典
    db_product = TableItem(**body)  
    db.add(db_product)  # 添加数据到数据库会话（此时还未真正写入数据库）
    db.commit()      # 提交数据库会话，将数据真正写入到数据库中
    db.refresh(db_product)  # 刷新实例以获取数据库生成的 ID

    return TypeResponse(message="物品创建成功")


    # res = next((u for u in fake_db if u["id"] == body["id"]), None)
    # if res:
    #     return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品已存在")
    # else:
    #     fake_db.append(body)
    #     return TypeResponse(message="物品创建成功")
     
# 路由：根据索引获取单个物品
@app.get("/query",response_model=TypeResponse[Item])
async def read_item(id: int,db:Session = Depends(get_db)):
    item = db.query(TableItem).filter(TableItem.id == id).first()
    # item = next((u for u in fake_db if u["id"] == id), None)
    if item:
        return TypeResponse(data=item)
    else:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品不存在")
    
# 更新物品
@app.post("/update/{item_id}",response_model=TypeResponse)
async def update_item(item_id: int, data: Item,db:Session = Depends(get_db)):

    item = db.query(TableItem).filter(TableItem.id == item_id).first()
    #item = next((u for u in fake_db if u["id"] == item_id), None)
    print(item,data)
    if item:
        # item.update(data)

        for key, value in data.model_dump().items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return TypeResponse(message="物品更新成功")
    else:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品不存在")
    
# 删除物品
@app.delete("/delete/{item_id}",response_model=TypeResponse)
async def delete_item(item_id: int,db:Session = Depends(get_db)):
    item = db.query(TableItem).filter(TableItem.id == item_id).first()
    if item:
        # fake_db.remove(item)
        db.delete(item)
        db.commit()
        return TypeResponse(message="删除成功")
    else:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品不存在")

# 路由：下载文件
@app.get("/download/{file_name}", response_class=FileResponse)
async def download(file_name: str):
    file_path = f"static/{file_name}"
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)

# 运行服务器（需安装 uvicorn：pip install uvicorn）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
