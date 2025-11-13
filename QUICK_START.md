# 🚀 快速开始指南

## ✅ 当前状态

项目文件夹已经整理完成！所有路径配置已修正。

```
✅ 目录结构：规范且清晰
✅ 路径配置：已修正并测试通过
✅ 文档：完整齐全
✅ 现有代码：已迁移
```

## 📁 项目位置

```
C:\Users\admin\Desktop\essay-grader-v2\
```

## 🎯 下一步：开始开发

### 方式一：在VS Code中打开项目（推荐）

1. **打开VS Code**

2. **打开文件夹**
   - 点击"文件" → "打开文件夹"
   - 选择 `C:\Users\admin\Desktop\essay-grader-v2`
   - 点击"选择文件夹"

3. **查看项目结构**
   - 左侧会显示完整的项目目录
   - 可以直接编辑文件

### 方式二：命令行操作

```bash
# 进入项目目录
cd C:\Users\admin\Desktop\essay-grader-v2

# 查看项目结构
dir

# 进入后端目录
cd backend

# 测试路径配置
python app/paths.py
```

## 📚 必读文档

按顺序阅读以下文档：

### 1. [README.md](README.md) - 5分钟
- 项目概述
- 技术栈
- 快速开始

### 2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 10分钟
- 详细的目录结构
- 每个文件的作用
- 开发工作流

### 3. [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 5分钟
- 路径配置说明
- 已完成的修改
- 配置原则

### 4. [docs/essay_grader_student_portal_plan.md](docs/essay_grader_student_portal_plan.md) - 30分钟
- 完整的技术规划
- 数据库设计
- API设计
- 前端设计

### 5. [docs/新手部署指南.md](docs/新手部署指南.md) - 20分钟
- 部署准备
- 一键部署脚本
- 常见问题

## 🔧 测试现有系统

在开始开发新功能前，先测试一下现有系统是否正常：

```bash
# 1. 进入后端目录
cd C:\Users\admin\Desktop\essay-grader-v2\backend

# 2. 创建虚拟环境（如果还没有）
python -m venv venv

# 3. 激活虚拟环境
venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行应用
python main.py
```

然后在浏览器访问：
- 主页：http://localhost:8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 📝 开发计划

### 第一阶段：数据库和认证（3-4天）

#### Day 1: 数据库基础
- [ ] 创建 `backend/app/database.py` - 数据库连接
- [ ] 创建 `backend/app/models/` 下的SQLAlchemy模型
- [ ] 创建 `scripts/init_db.py` - 数据库初始化脚本
- [ ] 测试数据库操作

#### Day 2: 认证系统
- [ ] 创建 `backend/app/utils/security.py` - JWT和密码加密
- [ ] 创建 `backend/app/routes/auth.py` - 认证接口
- [ ] 创建 `backend/app/middleware/auth.py` - 认证中间件
- [ ] 测试登录功能

#### Day 3-4: 核心API
- [ ] 修改 `backend/app/services/workflow_engine.py` - 保存到数据库
- [ ] 创建 `backend/app/dao/` - 数据访问层
- [ ] 开发学生端API
- [ ] 开发教师端API

### 第二阶段：前端开发（4-5天）

#### Day 5: 项目搭建
- [ ] 初始化Vue 3项目
- [ ] 配置路由和状态管理
- [ ] 开发公共组件

#### Day 6-7: 学生端
- [ ] 登录页面
- [ ] 仪表盘
- [ ] 批阅记录列表
- [ ] 记录详情

#### Day 8-9: 教师端
- [ ] 批阅管理
- [ ] 学生管理
- [ ] 统计分析

### 第三阶段：测试和部署（3-4天）

- [ ] 前后端联调
- [ ] 功能测试
- [ ] 准备部署脚本
- [ ] 服务器部署

## 🎯 今天可以完成的任务

建议今天先完成以下任务：

### 任务1：创建数据库模型（1-2小时）

创建以下文件：
- `backend/app/database.py`
- `backend/app/models/user.py`
- `backend/app/models/essay.py`
- `backend/app/models/grading.py`

### 任务2：创建数据库初始化脚本（1小时）

创建：
- `scripts/init_db.py`

### 任务3：测试数据库（30分钟）

运行初始化脚本，确认数据库创建成功。

## 💡 开发提示

### 使用路径管理

在所有新代码中，使用统一的路径管理：

```python
from app.paths import DATA_DIR, UPLOADS_DIR, LOGS_DIR, DATABASE_PATH

# 使用路径
db_path = DATABASE_PATH
upload_path = UPLOADS_DIR / "test.jpg"
```

### 查看日志

```bash
# 实时查看日志
type C:\Users\admin\Desktop\essay-grader-v2\logs\app.log
```

### 常用命令

```bash
# 进入项目
cd C:\Users\admin\Desktop\essay-grader-v2

# 进入后端
cd backend

# 激活虚拟环境
venv\Scripts\activate

# 运行应用
python main.py

# 测试路径
python app/paths.py
```

## 🆘 遇到问题？

1. **查看日志**：`logs/app.log`
2. **查看文档**：`docs/` 目录下的文档
3. **测试路径**：运行 `python app/paths.py`

## ✨ 准备好了吗？

现在一切就绪，可以开始开发了！

建议从创建数据库模型开始。需要我帮你创建第一个文件吗？

---

**项目版本**：V2.0
**最后更新**：2024-01-15