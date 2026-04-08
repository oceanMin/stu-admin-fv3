from urllib.parse import quote
from fastapi import APIRouter, Depends, File, HTTPException, Header, UploadFile
from fastapi.params import Body, Path, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime
from tortoise.expressions import Q
from jose import JWTError, jwt
from utils.utils import SECRET_KEY, ALGORITHM
from utils.excel_utils import  import_students_from_excel
from tortoise.functions import Count

from models import Student, StudentResponse

# 创建 APIRouter 实例
student_router = APIRouter()
# 创建 Pydantic 模型
Student_Pydantic = pydantic_model_creator(Student, name="Student")

async def get_current_user(token: str = Header(None)):
    if not token:
        # 替换HTTPException为JSONResponse，返回统一格式
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "未登录，请先登录", "data": []}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "登录已过期，请重新登录", "data": []}
        )

# Excel 导出接口
@student_router.get("/export")
async def export_students(search: str = None):
    try:
        query = Student.all()

        # 🔥 关键：有搜索关键词就过滤
        if search:
            query = query.filter(
                Q(name__icontains=search) | Q(no__icontains=search)
            )

        # 查询过滤后的数据
        students = await query.values(
            "id", "no", "name", "clazz", "major", "college", "phone", "email", "address"
        )

        if not students:
            raise HTTPException(status_code=400, detail="没有符合条件的数据")

        import pandas as pd
        from io import BytesIO

        df = pd.DataFrame(students)
        df = df[["id", "no", "name", "clazz", "major", "college", "phone", "email", "address"]]
        df.columns = ["ID", "学号", "姓名", "班级", "专业", "学院", "手机号", "邮箱", "地址"]

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="学生信息", index=False)
        output.seek(0)

        from urllib.parse import quote
        filename = quote("学生信息表.xlsx")

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename*=utf-8''{filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败：{str(e)}")

# 🔥 新增：Excel 导入接口
@student_router.post("/import")
async def import_students(file: UploadFile = File(...)):
    result = await import_students_from_excel(file)
    return result

# 下载模板接口
@student_router.get("/template")
async def download_template():
    from io import BytesIO
    import pandas as pd

    # 1. 生成标准表头的空模板
    columns = ["学号", "姓名", "班级", "专业", "学院", "手机号", "邮箱", "地址"]
    df = pd.DataFrame(columns=columns)
    
    # 2. 写入 BytesIO，必须用 openpyxl 引擎
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="导入模板", index=False)
    
    # 3. 重置指针，关键！
    output.seek(0)

    # 4. 中文文件名编码，避免乱码
    filename = quote("学生信息导入模板.xlsx")
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename*=utf-8''{filename}",
            "Content-Length": str(output.getbuffer().nbytes)
        }
    )

# 查询所有学生信息
@student_router.get(
    "/selectAll",
    summary="查询所有学生信息",
    description="获取系统中所有学生的信息列表，支持分页查询",
    response_description="返回学生信息列表及分页数据",
)
async def select_all(
    page: int = Query(1, description="当前页码", ge=1),
    size: int = Query(10, description="每页显示数量", ge=1, le=100),
    search: str = Query("", description="搜索关键词"),
    user: dict = Depends(get_current_user)
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
            Q(no__icontains=search)
            | Q(name__icontains=search)
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
    "/select/{student_id}",
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


@student_router.post(
    "/createStuInfo",
    summary="新增学生信息",
    description="创建新的学生信息",
    response_description="返回创建成功的学生信息",
)
async def createStuInfo(student: StudentResponse = Body(..., description="学生信息")):
    """新增学生信息"""
    print("*" * 20, student)
    stu = await Student.create(**student.dict(exclude_unset=True))
    return {
        "message": "新增成功",
        "status": 200,
        "success": True,
        "code": 200,
        "data": stu,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@student_router.post(
    "/update",
    summary="更新学生信息",
    description="根据ID更新指定学生的信息",
    response_description="返回更新成功后的学生信息",
)
async def update(student: StudentResponse = Body(..., description="学生信息")):
    """更新学生信息"""
    print("*" * 20, student)
    # 1. 校验ID是否存在（Pydantic 模型如果id是必填，这里其实可以省略，FastAPI会自动校验）
    if not student.id:
        return {"message": "缺少ID", "status": 400, "success": False, "code": 400}
    stu = await Student.get_or_none(id=student.id)
    if not stu:
        return "没有该学生"
    # 更新时候，排除id字段
    update_data = student.dict(exclude_unset=True, exclude={"id"})
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


@student_router.delete(
    "/delete/{student_id}",
    summary="删除学生信息",
    description="根据ID删除指定学生的信息",
    response_description="返回删除成功",
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

# 定义请求体模型，匹配前端传的 { ids: [1,2,3] } 格式
class BatchDeleteRequest(BaseModel):
    ids: list[int]
# 批量删除学生
@student_router.post("/batchDelete")
async def batch_delete_students(req: BatchDeleteRequest):
    ids = req.ids
    if not ids:
        raise HTTPException(status_code=400, detail="请选择要删除的学生")
    
    # 批量删除
    await Student.filter(id__in=ids).delete()
    return {"code": 200, "message": f"成功删除 {len(ids)} 条数据"}

# ======================== 统计图表 ========================

# 按学院统计人数
@student_router.get("/stats/college")
async def stats_by_college():
    stats = await Student.annotate(
        count=Count("id")
    ).group_by("college").values("college", "count")
    return {"code": 200, "data": stats}

# 按班级统计人数
@student_router.get("/stats/clazz")
async def stats_by_clazz():
    stats = await Student.annotate(
        count=Count("id")
    ).group_by("clazz").values("clazz", "count")
    return {"code": 200, "data": stats}


# 获取统计数据
@student_router.get("/statistics")
async def get_statistics():
    total = await Student.all().count()
    colleges = await Student.all().distinct().values("college")
    clazzes = await Student.all().distinct().values("clazz")
    majors = await Student.all().distinct().values("major")

    college_data = []
    for c in colleges:
        count = await Student.filter(college=c["college"]).count()
        college_data.append({"name": c["college"], "value": count})

    return {
        "code":200,
        "data": {
            "total": total,
            "collegeCount": len(colleges),
            "clazzCount": len(clazzes),
            "majorCount": len(majors),
            "collegeChart": college_data
        }
    }