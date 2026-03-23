from fastapi import APIRouter
from fastapi.params import Body, Path, Query
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime
from tortoise.expressions import Q

from models import Student,StudentResponse

# 创建 APIRouter 实例
student_router = APIRouter()
# 创建 Pydantic 模型
Student_Pydantic = pydantic_model_creator(Student, name="Student")


@student_router.get(
    "/student/selectAll",
    summary="查询所有学生信息",
    description="获取系统中所有学生的信息列表，支持分页查询",
    response_description="返回学生信息列表及分页数据",
)
async def select_all(
    page: int = Query(1, description="当前页码", ge=1),
    size: int = Query(10, description="每页显示数量", ge=1, le=100),
    search: str = Query("", description="搜索关键词"),
):
    """
    查询所有学生信息

    - **page**: 当前页码，默认为1
    - **size**: 每页显示数量，默认为10，最大100

    返回数据包含：
    - **message**: 操作结果消息
    - **status**: HTTP状态码
    - **success**: 是否成功
    - **data**: 学生信息列表
    - **pages**: 分页信息
    """
    # 计算偏移量
    offset = (page - 1) * size
     # 构建查询条件：如果有搜索关键词，模糊匹配学号或姓名
    query = Student.all()
    if search.strip():  # 去除空格，避免空字符串查询
        # 模糊查询逻辑（Tortoise ORM 语法）
        # contains: 包含关键词（不区分大小写，根据数据库配置）
        # 同时匹配学号（数字转字符串匹配）和姓名
        query = query.filter(
            # Q对象实现 或 条件：学号包含 或 姓名包含
             Q(no__icontains=search) | Q(name__icontains=search)
        )

    # 查询总数
    total = await query.count()

    # 分页查询
    stu_list = await query.offset(offset).limit(size)

    # 计算总页数
    total_pages = (total + size - 1) // size

    return {
        "message": "查询成功",
        "status": 200,
        "success": True,
        "code": 200,
        "data": stu_list,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages": {"total": total, "current": page, "size": size, "pages": total_pages},
    }


@student_router.get(
    "/student/select/{student_id}",
    summary="查询指定学生信息",
    description="根据ID查询指定学生的信息",
    response_description="返回学生信息",
)
async def select_one(student_id: int = Path(..., description="学生ID")):
    """
    根据ID获取学生
    - **student_id**: 学生ID，必须为正整数
    """
    student = await Student.get_or_none(id=student_id)
    return {
        "message": "查询成功",
        "status": 200,
        "success": True,
        "code": 200,
        "data": student,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@student_router.post("/student/createStuInfo",
                     summary="新增学生信息",
                     description="创建新的学生信息",
                     response_description="返回创建成功的学生信息"
)
async def createStuInfo(student: StudentResponse = Body(..., description="学生信息")):
    """新增学生信息"""
    print('*'*20,student)
    stu = await Student.create(**student.dict(exclude_unset=True))
    return {
        "message": "新增成功",
        "status": 200,
        "success": True,
        "code": 200,
        "data": stu,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@student_router.post("/student/update",
                    summary="更新学生信息",
                    description="根据ID更新指定学生的信息",
                     response_description="返回更新成功后的学生信息"
)
async def update(student: Student_Pydantic=Body(..., description="学生信息")):
    """更新学生信息"""
    # 1. 校验ID是否存在（Pydantic 模型如果id是必填，这里其实可以省略，FastAPI会自动校验）
    if not student.id:
        return {
            "message": "缺少ID",
            "status": 400,
            "success": False,
            "code": 400
        }
    stu = await Student.get_or_none(id=student.id)
    if not stu:
        return "没有该学生"
    # 更新时候，排除id字段
    update_data = student.dict(exclude_unset=True,exclude={"id"})
    await Student.filter(id=student.id).update(**update_data)
    data = await Student.get(id=student.id)
    return {
        "message": "更新成功",
        "status": 200,
        "success": True,
        "code": 200,
        "data": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@student_router.delete("/student/delete/{student_id}",
                       summary="删除学生信息",
                       description="根据ID删除指定学生的信息",
                       response_description="返回删除成功"
)
async def delete(student_id: int = Path(..., description="学生ID")):
    """删除学生信息"""
    stu = await Student.get_or_none(id=student_id)
    if not stu:
        return "没有该学生"
    await Student.filter(id=student_id).delete()
    return {
        "message": "删除成功",
        "status": 200,
        "success": True,
        "code": 200,
        "timestamp": datetime.now().__format__("%Y-%m-%d %H:%M:%S"),
    }
