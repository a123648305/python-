import os
from fastapi.responses import FileResponse
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
