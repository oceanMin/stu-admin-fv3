# 📚 学生信息管理系统 (stu-admin-fv3)
基于 **FastAPI + Vue3 + Element Plus** 开发的现代化学生信息管理系统，实现学生信息的增删改查、分页筛选等完整功能，前后端分离架构，轻量易部署，适配各类教育场景。

---

## ✨ 项目特性
- **后端技术栈**：FastAPI + Tortoise-ORM + SQLite，高性能异步接口，自动生成 Swagger 文档
- **前端技术栈**：Vue3 + Element Plus + Axios，响应式界面，适配PC端
- **核心功能**：学生信息增删改查、分页展示、条件筛选、表单校验
- **工程规范**：前后端分离目录结构，Git 版本控制，可直接部署上线
- **数据兼容**：接口支持学号（no）字段同时传字符串/数字，自动类型转换

---

## 📁 项目目录结构
```
stu-admin-fv3/
├── fastapi_app/          # 后端服务
│   ├── routers/          # 接口路由（学生管理等）
│   ├── models.py         # 数据库模型 + Pydantic 校验模型
│   ├── main.py           # 服务入口、跨域配置、全局异常处理
│   ├── settings.py       # 数据库配置
│   ├── test_db.py        # 数据库测试连接
│   └── ...
├── vue3/                 # 前端项目
│   ├── src/
│   │   ├── api/          # 接口请求封装
│   │   ├── components/   # 公共组件（表格、弹窗等）
│   │   ├── pages/        # 页面组件（学生信息页等）
│   │   └── utils/        # 工具函数（请求拦截等）
│   └── ...
├── .gitignore            # Git 忽略文件配置
└── README.md             # 项目说明文档
```

---

## 🚀 快速启动
### 1. 后端启动（FastAPI）
```bash
# 进入后端目录
cd fastapi_app

# 安装依赖
pip install fastapi uvicorn[standard] tortoise-orm pydantic python-multipart aiomysql

# 启动服务（默认端口 9090）
python main.py
# 或使用 uvicorn 启动
uvicorn main:app --host 0.0.0.0 --port 9090 --reload
```
启动后访问 `http://localhost:9090/docs` 查看接口文档。

### 2. 前端启动（Vue3）
```bash
# 进入前端目录
cd vue3

# 安装依赖
npm install

# 启动开发服务器（默认端口 5173）
npm run dev
```
启动后访问 `http://localhost:5173` 访问系统页面。

---

## 🎯 核心功能说明
| 功能模块 | 功能描述 |
|----------|----------|
| 学生信息管理 | 支持学生信息的新增、编辑、删除、模糊查询 |
| 分页展示 | Element Plus 分页组件，支持页码切换、每页条数调整、总条数/总页数显示 |
| 条件筛选 | 支持按学号、姓名、班级等字段快速筛选学生 |
| 表单校验 | 前后端双重校验，保证数据合法性 |
| 接口兼容 | 学号字段同时支持字符串/数字输入，自动类型转换 |

---

## ⚙️ 技术栈详情
### 后端
- **框架**：FastAPI（高性能异步Web框架）
- **ORM**：Tortoise-ORM（异步ORM，适配FastAPI）
- **数据库**：MySQL（轻量无服务，可替换为PostgreSQL等）
- **文档**：自动生成 Swagger/OpenAPI 文档
- **跨域**：CORS 中间件，支持前后端分离部署

### 前端
- **框架**：Vue3（Composition API）
- **UI组件库**：Element Plus
- **请求库**：Axios（请求拦截、响应拦截）
- **构建工具**：Vite（极速开发体验）

---

## 📝 开发说明
### 接口规范
- 统一前缀：`/api/v1`
- 学生管理接口：`/api/v1/student/`
  - `GET /selectAll`：查询所有学生（分页）
  - `POST /update`：更新学生信息
  - `POST /createStuInfo`：新增学生
  - `POST /delete`：删除学生

### 模型说明
- **Student**：数据库ORM模型，对应student表
- **StudentResponse**：响应模型，用于返回前端数据
- **StudentUpdateRequest**：请求模型，用于接收更新参数，支持学号类型自动转换

---

## 📌 部署说明
### 后端部署
- 可直接使用 `uvicorn` 部署，或使用 Nginx 反向代理
- 数据库可替换为 PostgreSQL，修改 `settings.py` 配置即可
- 生产环境建议关闭 `--reload`，使用守护进程（如 systemd）管理

### 前端部署
- 执行 `npm run build` 打包，将 `dist` 目录部署到 Nginx
- 配置 Nginx 反向代理，将 `/api` 请求转发到后端服务

---

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request 优化项目，共同完善功能。

---

## 📄 许可证
本项目基于 MIT 许可证开源，可自由使用和修改。

---

需要我帮你把这个README直接生成可复制的 `.md` 文件内容，或者补充**环境依赖清单**、**常见问题排查**等模块吗？
