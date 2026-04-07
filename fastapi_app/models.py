from tortoise import fields, models
from pydantic import BaseModel

# 创建用户模型
class User(models.Model):
    id = fields.BigIntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password = fields.CharField(max_length=256, description="加密密码")
    # 确保字段名和数据库一致：create_time / update_time
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "user"  # 强制指定表名，避免ORM自动生成user表
        table_description = "用户表"

# 创建学生模型
class Student(models.Model):
    id = fields.IntField(pk=True, generated=True, description="用户ID，主键")
    no = fields.CharField(max_length=20, description="学号") 
    name = fields.CharField(max_length=255, null=True)
    clazz = fields.CharField(max_length=255, null=True)
    major = fields.CharField(max_length=255, null=True)
    college = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=255, null=True)
    email = fields.CharField(max_length=255, null=True)
    address = fields.CharField(max_length=255, null=True)

    class Meta:
        db_name = "student"


# 添加 Pydantic 模型用于数据返回
class StudentResponse(BaseModel):
    """返回给前端的 Student 数据结构"""
    id: int | None = None
    no: str | int | None = None
    name: str | None = None
    clazz: str | None = None
    major: str | None = None
    college: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True  # 允许从 ORM 模型转换
