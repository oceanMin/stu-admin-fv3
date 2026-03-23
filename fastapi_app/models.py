from tortoise import fields,models
from pydantic import BaseModel

class Student(models.Model):
    id = fields.IntField(pk=True, description="用户ID，主键")
    no=fields.CharField(max_length=255,null=True)
    name=fields.CharField(max_length=255,null=True)
    clazz=fields.CharField(max_length=255,null=True)
    major=fields.CharField(max_length=255,null=True)
    college=fields.CharField(max_length=255,null=True)
    phone=fields.CharField(max_length=255,null=True)
    email=fields.CharField(max_length=255,null=True)
    address=fields.CharField(max_length=255,null=True)

    class Meta:
        db_name = "student"


# 添加 Pydantic 模型用于数据返回
class StudentResponse(BaseModel):
    """返回给前端的 Student 数据结构"""
    id: int
    no: str | None = None
    name: str | None = None
    clazz: str | None = None
    major: str | None = None
    college: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True  # 允许从 ORM 模型转换