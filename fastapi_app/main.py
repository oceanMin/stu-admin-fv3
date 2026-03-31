# main.py
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from settings import TORTOISE_ORM
from routers.student import student_router
from routers.user import user_router

# 创建 FastAPI 应用
app = FastAPI(
    title="学生管理系统API",
    description="基于 FastAPI + Tortoise-ORM 的学生管理系统",
    version="1.0.0"
)
# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议指定具体域名
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 统一设置API前缀
API_PREFIX = "/api/v1"

# 注册路由
app.include_router(student_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)

# 注册 Tortoise-ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,
    add_exception_handlers=True,
    generate_schemas=False,  # 表已存在，设为 False
)

# 根路径
@app.get("/")
async def root():
    return {
        "message": "学生管理系统API",
        "docs": "/docs",
        "api_prefix": API_PREFIX,
        "endpoints": {
            "students": f"{API_PREFIX}/student/selectAll"
        }
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=9090,
        reload=True  # 开发模式，代码修改自动重启
    )