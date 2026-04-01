import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 加密
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-safe-123456")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 令牌过期时间

# 生成密码哈希
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 校验密码（核心修复：确保和注册用同一算法）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 创建 token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt