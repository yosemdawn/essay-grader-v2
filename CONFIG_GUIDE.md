# ⚙️ 配置指南

## 📁 目录结构说明

本项目采用**最佳实践**：代码和数据分离

```
essay-grader-v2/
├── backend/          # 仅包含代码
├── frontend/         # 仅包含代码
├── data/            # 所有持久化数据
├── logs/            # 所有日志文件
└── ...
```

## 🔧 需要修改的配置

由于我们将数据目录从 `backend/data/` 移到了 `data/`，需要修改以下配置：

### 1. backend/app/config.py

需要修改路径配置，将相对路径从 `data/` 改为 `../data/`：

```python
# 修改前
student_db_path: str = "data/students.json"
upload_dir: str = "uploads"
data_dir: str = "data"
logs_dir: str = "logs"

# 修改后
student_db_path: str = "../data/students.json"
upload_dir: str = "../data/uploads"
data_dir: str = "../data"
logs_dir: str = "../logs"
```

### 2. backend/main.py

修改目录创建逻辑：

```python
# 修改前
os.makedirs("logs", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)

# 修改后
os.makedirs("../logs", exist_ok=True)
os.makedirs("../data/uploads", exist_ok=True)
os.makedirs("../data", exist_ok=True)
```

### 3. backend/app/routes/grading.py

修改上传目录：

```python
# 修改前
UPLOAD_DIRECTORY = "uploads"

# 修改后
UPLOAD_DIRECTORY = "../data/uploads"
```

## 📝 路径配置原则

### 相对路径规则

从 `backend/` 目录运行程序时：
- 访问数据：`../data/`
- 访问日志：`../logs/`
- 访问上传文件：`../data/uploads/`

### 绝对路径（生产环境推荐）

```python
import os
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
UPLOADS_DIR = DATA_DIR / "uploads"
```

## 🚀 快速修复脚本

创建 `backend/fix_paths.py`：

```python
"""
路径修复脚本
将所有硬编码的路径改为相对于项目根目录的路径
"""
import os
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 定义路径
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
UPLOADS_DIR = DATA_DIR / "uploads"
STUDENTS_JSON = DATA_DIR / "students.json"
DATABASE_PATH = DATA_DIR / "database.db"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
(UPLOADS_DIR / "prompts").mkdir(exist_ok=True)
(UPLOADS_DIR / "essays").mkdir(exist_ok=True)

print("✅ 路径配置完成")
print(f"数据目录: {DATA_DIR}")
print(f"日志目录: {LOGS_DIR}")
print(f"上传目录: {UPLOADS_DIR}")
```

## 📋 修改清单

### 必须修改的文件

- [ ] `backend/app/config.py` - 修改路径配置
- [ ] `backend/main.py` - 修改目录创建
- [ ] `backend/app/routes/grading.py` - 修改上传目录
- [ ] `backend/app/services/student_db.py` - 修改数据库路径

### 建议修改的文件

- [ ] 创建 `backend/app/paths.py` - 统一管理所有路径
- [ ] 修改所有服务类使用新的路径配置

## 💡 最佳实践示例

创建 `backend/app/paths.py`：

```python
"""
统一路径管理
"""
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
STUDENTS_JSON = DATA_DIR / "students.json"
DATABASE_PATH = DATA_DIR / "database.db"

# 上传目录
UPLOADS_DIR = DATA_DIR / "uploads"
PROMPTS_DIR = UPLOADS_DIR / "prompts"
ESSAYS_DIR = UPLOADS_DIR / "essays"

# 日志目录
LOGS_DIR = PROJECT_ROOT / "logs"
APP_LOG = LOGS_DIR / "app.log"

# 备份目录
BACKUP_DIR = DATA_DIR / "backup"

# 确保所有目录存在
def ensure_directories():
    """确保所有必要的目录存在"""
    for directory in [DATA_DIR, UPLOADS_DIR, PROMPTS_DIR, 
                      ESSAYS_DIR, LOGS_DIR, BACKUP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
```

然后在其他文件中使用：

```python
from app.paths import DATA_DIR, UPLOADS_DIR, LOGS_DIR, ensure_directories

# 确保目录存在
ensure_directories()

# 使用路径
student_db_path = DATA_DIR / "students.json"
```

## 🔍 验证配置

运行以下命令验证路径配置：

```bash
cd backend
python -c "from app.paths import *; ensure_directories(); print('✅ 路径配置正确')"
```

## ⚠️ 注意事项

1. **开发环境**：使用相对路径 `../data/`
2. **生产环境**：使用绝对路径或环境变量
3. **Docker部署**：使用容器内的绝对路径 `/app/data/`
4. **权限问题**：确保应用有读写 data/ 和 logs/ 的权限

## 📚 相关文档

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
- [README.md](README.md) - 项目说明
- [docs/essay_grader_student_portal_plan.md](docs/essay_grader_student_portal_plan.md) - 完整规划

---

**最后更新**：2024-01-15