# utils/excel_utils.py
import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException
from models import Student  # 确保 Student 模型导入正确

# Excel 导出：生成学生信息 Excel 文件
async def export_students_to_excel():
    # 1. 查询所有学生数据（用 values() 确保拿到字典）
    students = await Student.all().values(
        "id", "no", "name", "clazz", "major", "college", "phone", "email", "address"
    )
    if not students:
        raise HTTPException(status_code=400, detail="暂无学生数据可导出")
    
    # 2. 创建 DataFrame，严格匹配你的学生字段
    df = pd.DataFrame(students)
    # 3. 调整列顺序和表头，和前端 columns 完全一致
    df = df[["id", "no", "name", "clazz", "major", "college", "phone", "email", "address"]]
    df.columns = ["ID", "学号", "姓名", "班级", "专业", "学院", "手机号", "邮箱", "地址"]
    
    # 4. 写入 BytesIO，用 openpyxl 引擎
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="学生信息", index=False)
    
    # 5. 重置指针，必须执行！
    output.seek(0)
    return output

# Excel 导入：解析上传的 Excel 文件并批量保存
async def import_students_from_excel(file: UploadFile):
    # 校验文件类型
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="仅支持 .xlsx / .xls 格式的 Excel 文件")
    
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file.file)
        # 校验必要列（和导出表头一致）
        required_columns = ["学号", "姓名", "班级", "专业", "学院", "手机号", "邮箱", "地址"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Excel 缺少必要列：{required_columns}")
        
        # 批量创建学生，严格匹配模型字段
        students_to_create = []
        for _, row in df.iterrows():
            students_to_create.append({
                "no": str(row["学号"]),
                "name": str(row["姓名"]),
                "clazz": str(row["班级"]),
                "major": str(row["专业"]),
                "college": str(row["学院"]),
                "phone": str(row["手机号"]),
                "email": str(row["邮箱"]),
                "address": str(row["地址"])
            })
        
        # 批量插入数据库
        await Student.bulk_create([Student(**item) for item in students_to_create])
        return {"code": 200, "message": f"成功导入 {len(students_to_create)} 条学生数据", "data": None}
    
    except Exception as e:
        # 捕获异常，打印错误日志，方便排查
        print(f"Excel 导入失败：{str(e)}")
        raise HTTPException(status_code=500, detail=f"导入失败：{str(e)}")