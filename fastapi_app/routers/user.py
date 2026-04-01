from fastapi import APIRouter
from models import User
from schemas import UserCreate
from utils.utils import get_password_hash, verify_password, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

user_router = APIRouter(prefix="/api/v1/user", tags=["用户模块"])

# 注册接口（增强异常处理）
@user_router.post("/register")
async def register(user: UserCreate):
    try:
        # 检查用户名是否已存在
        exist = await User.exists(username=user.username)
        if exist:
            return {"code": 400, "message": "用户名已存在，请更换", "data": None}
        
        # 密码加密
        hashed_pwd = get_password_hash(user.password)
        # 创建用户
        await User.create(username=user.username, password=hashed_pwd)
        
        return {"code": 200, "message": "注册成功，请登录", "data": None}
    except Exception as e:
        # 捕获所有异常，返回统一错误格式
        return {"code": 500, "message": f"注册失败：{str(e)}", "data": None}

# 登录接口（保持不变，确保格式统一）
@user_router.post("/login")
async def login(user: UserCreate):
    try:
        # 1. 查询用户
        db_user = await User.get_or_none(username=user.username)
        if not db_user:
            return {"code": 401, "message": "用户名或密码错误", "data": None}
        
        # 2. 校验密码
        if not verify_password(user.password, db_user.password):
            return {"code": 401, "message": "用户名或密码错误", "data": None}
        
        # 3. 生成token（确保create_access_token函数正常）
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": db_user.username},
            expires_delta=access_token_expires
        )
        
        # 4. 强制返回完整格式（前端需要的字段必须存在）
        return {
            "code": 200,
            "message": "登录成功",
            "token": access_token,  # 必须返回token
            "username": db_user.username,  # 必须返回用户名
            "data": None
        }
    except Exception as e:
        return {"code": 500, "message": f"登录失败：{str(e)}", "data": None}