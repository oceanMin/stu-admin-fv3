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
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="仅支持 .xlsx / .xls 格式的 Excel 文件")
    
    try:
        df = pd.read_excel(file.file)
        required_columns = ["学号", "姓名", "班级", "专业", "学院", "手机号", "邮箱", "地址"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Excel 缺少必要列：{required_columns}")

        # 先拿到【纯字符串】的已有学号列表
        existing_nos = await Student.all().values_list("no", flat=True)
        existing_nos = [str(no).strip() for no in existing_nos]  # 全部转为字符串 + 去空格

        students_to_create = []
        success_count = 0
        skip_count = 0

        for _, row in df.iterrows():
            # 取出来直接转字符串，去掉空格
            no = str(row["学号"]).strip()

            # 现在比较的都是【字符串】，绝对能匹配！
            if no in existing_nos:
                skip_count += 1
                continue

            students_to_create.append({
                "no": no,  # 直接存字符串，保证一致性
                "name": str(row["姓名"]).strip(),
                "clazz": str(row["班级"]).strip(),
                "major": str(row["专业"]).strip(),
                "college": str(row["学院"]).strip(),
                "phone": str(row["手机号"]).strip(),
                "email": str(row["邮箱"]).strip(),
                "address": str(row["地址"]).strip()
            })
            success_count += 1

        if students_to_create:
            await Student.bulk_create([Student(**item) for item in students_to_create])

        return {
            "code": 200,
            "message": f"导入完成：成功 {success_count} 条，重复跳过 {skip_count} 条",
            "data": None
        }
    
    except Exception as e:
        print(f"导入失败：{str(e)}")
        raise HTTPException(status_code=500, detail=f"导入失败：{str(e)}")