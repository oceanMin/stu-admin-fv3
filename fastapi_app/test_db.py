# test_db.py
import asyncio
from tortoise import Tortoise
from settings import TORTOISE_ORM
from models import Student


async def test_connection():
    try:
        # 初始化数据库连接
        await Tortoise.init(config=TORTOISE_ORM)
        print("数据库连接成功！")

        # 测试查询
        students = await Student.all()
        print(f"查询到 {len(students)} 条数据")

        for stu in students:
            print(f"ID: {stu.id}, 姓名: {stu.name}")

        # 关闭连接
        await Tortoise.close_connections()

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())