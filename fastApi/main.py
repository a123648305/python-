import os
from fastapi import FastAPI, HTTPException,status
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from typing import Generic, TypeVar, Optional

# # 导入自定义模块
# import models
# import schemas
from database import SessionLocal, engine

# 创建数据库表（首次运行时执行）
# models.Base.metadata.create_all(bind=engine)
# 依赖项：获取数据库会话（每个请求一个会话）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # 请求结束后关闭会话

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


async def download_file(FILE_PATH:str):
    # 检查文件是否存在
    if not os.path.exists(FILE_PATH):
        return {"error": "文件不存在"}
    
    # 返回文件（自动处理 MIME 类型）
    return FileResponse(
        path=f"./static/{FILE_PATH}",
        filename="custom-name.pdf",  # 下载时显示的文件名（可选）
        media_type="application/pdf"  # 指定 MIME 类型（可选，自动推断）
    )


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
async def read_items():
    return TypeResponse(data=fake_db)

# 路由：创建新物品
@app.post("/add_item", status_code=201)
async def create_item(data: Item):
    body = data.model_dump() # 将数据转为字典
    res = next((u for u in fake_db if u["id"] == body["id"]), None)
    if res:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品已存在")
    else:
        fake_db.append(body)
        return TypeResponse(message="物品创建成功")
     
# 路由：根据索引获取单个物品
@app.get("/query",response_model=TypeResponse[Item])
async def read_item(id: int):
    item = next((u for u in fake_db if u["id"] == id), None)
    if item:
        return TypeResponse(data=item)
    else:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品不存在")
    
# 更新物品
@app.post("/update/{item_id}",response_model=TypeResponse)
async def update_item(item_id: int, data: Item):
    item = next((u for u in fake_db if u["id"] == item_id), None)
    print(item,data)
    if item:
        item.update(data)
        return TypeResponse(message="物品更新成功")
    else:
        return TypeResponse(code=status.HTTP_404_NOT_FOUND,message="物品不存在")
    
# 删除物品
@app.delete("/delete/{item_id}",response_model=TypeResponse)
async def delete_item(item_id: int):
    item = next((u for u in fake_db if u["id"] == item_id), None)
    if item:
        fake_db.remove(item)
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
