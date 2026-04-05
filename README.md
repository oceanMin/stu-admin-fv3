# 📚 学生信息管理系统 (stu-admin-fv3)
基于 **FastAPI + Vue3 + Element Plus** 开发的现代化学生信息管理系统，实现学生信息的增删改查、分页筛选、Excel 导入导出、批量操作等完整业务功能，前后端分离架构，轻量易部署，适配各类教育场景。

---

## ✨ 项目特性
- **后端技术栈**：FastAPI + Tortoise-ORM + MySQL，高性能异步接口，自动生成 Swagger 文档
- **前端技术栈**：Vue3 + Element Plus + Axios，响应式界面，适配PC端
- **基础核心功能**：学生信息增删改查、分页展示、多条件模糊筛选、前后端表单双重校验
- **高级业务功能**：Excel 数据导入、按筛选条件导出、学生信息批量删除、表格多选
- **工程规范**：前后端分离目录结构，Git 版本控制，接口统一规范，可直接部署上线
- **数据兼容**：接口支持学号（no）字段同时传字符串/数字，自动类型转换
- **体验优化**：操作友好提示、加载状态、异常捕获与错误提示、中文文件名导出兼容

---

## 📁 项目目录结构
```
stu-admin-fv3/
├── fastapi_app/          # 后端服务
│   ├── routers/          # 接口路由（学生管理、用户登录等）
│   ├── utils/            # 工具类（JWT 加密、Excel 处理工具）
│   ├── models.py         # 数据库模型 + Pydantic 校验模型
│   ├── main.py           # 服务入口、跨域配置、路由注册
│   ├── settings.py       # 数据库配置
│   └── ...
├── vue3/                 # 前端项目
│   ├── src/
│   │   ├── api/          # 接口请求封装（CRUD、导入导出、批量删除）
│   │   ├── components/   # 公共组件（ProTable 高级表格、FormDialog 表单弹窗）
│   │   ├── pages/        # 页面组件（学生信息管理页等）
│   │   └── utils/        # 请求工具（请求/响应拦截、Blob 导出处理）
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
pip install fastapi uvicorn[standard] tortoise-orm pydantic python-multipart pandas openpyxl

# 启动服务（默认端口 60527）
python main.py
# 或使用 uvicorn 启动
uvicorn main:app --host 0.0.0.0 --port 60527 --reload
```
启动后访问 `http://localhost:60527/docs` 查看接口文档。

### 2. 前端启动（Vue3）
```bash
# 进入前端目录
cd vue3

# 安装依赖
npm install

# 启动开发服务器（默认端口 9090）
npm run dev
```
启动后访问 `http://localhost:9090` 访问系统页面。

---

## 🎯 核心功能说明
| 功能模块 | 功能描述 |
|----------|----------|
| 学生信息管理 | 支持学生信息的新增、编辑、单条删除、模糊查询 |
| 分页展示 | Element Plus 分页组件，支持页码切换、每页条数调整、总条数/总页数显示 |
| 条件筛选 | 支持按学号、姓名快速筛选学生 |
| 表单校验 | 前后端双重校验，手机号、邮箱格式校验，非空校验 |
| Excel 导出 | 支持**按当前搜索条件筛选后导出**，自动生成中文文件名 Excel |
| Excel 导入 | 支持批量上传 Excel 导入学生数据，格式校验、异常提示 |
| 批量删除 | 表格多选框，支持批量选中并一次性删除多条学生数据 |
| 接口兼容 | 学号字段同时支持字符串/数字输入，自动类型转换 |
| 异常处理 | 全局请求异常捕获，导入导出编码兼容，无乱码、无 422/500 崩溃 |

---

## ⚙️ 技术栈详情
### 后端
- **框架**：FastAPI（高性能异步Web框架）
- **ORM**：Tortoise-ORM（异步ORM，适配FastAPI）
- **数据库**：MySQL（可替换为PostgreSQL）
- **文档**：自动生成 Swagger/OpenAPI 文档
- **跨域**：CORS 中间件，支持前后端分离部署
- **Excel处理**：pandas + openpyxl 实现导入导出、表头映射、批量操作

### 前端
- **框架**：Vue3（Composition API + `<script setup>`）
- **UI组件库**：Element Plus
- **请求库**：Axios（请求拦截、响应拦截、Blob 流处理）
- **构建工具**：Vite（极速开发体验）
- **公共组件**：ProTable（支持多选、搜索、工具栏）、FormDialog（弹窗表单）

---

## 📝 开发说明
### 接口规范
- 统一前缀：`/api/v1`
- 学生管理接口：`/api/v1/student/`
  - `GET /selectAll`：查询学生列表（分页 + 筛选）
  - `POST /createStuInfo`：新增学生
  - `POST /update`：更新学生信息
  - `GET /delete/{id}`：单条删除学生
  - `POST /batchDelete`：**批量删除学生**
  - `GET /export`：**按筛选条件导出 Excel**
  - `POST /import`：**Excel 批量导入学生**

### 模型说明
- **Student**：数据库ORM模型，对应 student 表
- 支持字段：id、no（学号）、name、clazz（班级）、major（专业）、college（学院）、phone、email、address
- 导入导出严格对齐字段，支持表头中文映射
- 批量操作使用 ID 数组进行批量过滤与删除

---

## 📌 部署说明
### 后端部署
- 可直接使用 `uvicorn` 部署，或使用 Nginx 反向代理
- 数据库可替换为 PostgreSQL，修改配置即可
- 生产环境建议关闭 `--reload`，使用守护进程（如 systemd）管理
- 确保服务器安装 pandas、openpyxl 等 Excel 处理依赖

### 前端部署
- 执行 `npm run build` 打包，将 `dist` 目录部署到 Nginx
- 配置 Nginx 反向代理，将 `/api` 请求转发到后端服务
- 导出功能依赖 Blob 响应，生产环境需正确配置跨域与响应头

---

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request 优化项目，可扩展如数据统计图表、登录鉴权、操作日志、数据备份等功能，共同完善系统。

---

## 📄 许可证
本项目基于 MIT 许可证开源，可自由使用、修改和部署。