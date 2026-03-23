from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Student

# 创建 APIRouter 实例
student_router = APIRouter()
# 创建 Pydantic 模型
Student_Pydantic = pydantic_model_creator(Student, name="Student")

@student_router.get("/student/selectAll")
async def select_all():
    """学生信息表"""
    stu_list = await Student.all()
    print(stu_list)
    return stu_list


@student_router.get("/student/select/{student_id}")
async def select_one(student_id: int):
    """
    根据ID获取学生
    - **student_id**: 学生ID，必须为正整数
    """
    student = await Student.get_or_none(id=student_id)
    return student