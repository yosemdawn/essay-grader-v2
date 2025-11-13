# 🚀 部署就绪说明

本项目已完成清理和优化，可以直接部署到生产服务器。

## ✅ 已完成的清理工作

### 删除的冗余文件
- ✅ `backend/venv/` - Python虚拟环境 (83MB)
- ✅ `backend/__pycache__/` - Python缓存文件
- ✅ `logs/app.log` - 日志文件
- ✅ `data/backup/` - 备份文件
- ✅ `frontend/node_modules/` - Node依赖

### 项目统计
- **文件数量**: 121个
- **项目大小**: 11.19MB
- **Git仓库**: 0.73MB

## 📦 项目结构

```
essay-grader-v2/
├── backend/              # 后端代码 (FastAPI)
│   ├── app/             # 应用核心
│   ├── requirements.txt # Python依赖
│   └── main.py          # 入口文件
├── frontend/            # 前端代码 (Vue 3)
│   ├── dist/           # 构建产物
│   ├── src/            # 源代码
│   └── package.json    # Node依赖
├── deploy/              # 部署脚本
│   ├── deploy.sh       # 一键部署
│   ├── nginx.conf      # Nginx配置
│   └── *.service       # Systemd服务
├── data/                # 数据目录
│   ├── database.db     # SQLite数据库
│   └── students.json   # 学生数据
└── docs/                # 文档
```

## 🚀 快速部署

### 方法一：从GitHub克隆（推荐）

```bash
# 在服务器上
git clone https://github.com/yosemmmmmm/essay-grader-v2.git
cd essay-grader-v2

# 构建前端（如果需要）
cd frontend
npm install
npm run build
cd ..

# 运行部署脚本
sudo bash deploy/deploy.sh
```

### 方法二：上传压缩包

```bash
# 在本地
tar -czf essay-grader-v2.tar.gz essay-grader-v2/
scp essay-grader-v2.tar.gz root@your-server:/tmp/

# 在服务器上
cd /tmp
tar -xzf essay-grader-v2.tar.gz
cd essay-grader-v2
sudo bash deploy/deploy.sh
```

## ⚙️ 部署后配置

### 1. 配置API密钥

```bash
sudo nano /var/www/essay-grader-v2/backend/.env
```

必须配置：
- `BAIDU_OCR_API_KEY` - 百度OCR API密钥
- `BAIDU_OCR_SECRET_KEY` - 百度OCR密钥
- `DOUBAO_API_KEY` - 豆包LLM API密钥
- `DOUBAO_MODEL_ID` - 豆包模型ID
- `SECRET_KEY` - JWT密钥（随机32位字符串）

### 2. 重启服务

```bash
sudo systemctl restart essay-grader
sudo systemctl restart nginx
```

### 3. 验证部署

访问: `http://your-server-ip`

默认账号:
- 管理员: `admin` / `admin123`
- 学生: 学号 / `123456`

## 📝 注意事项

1. **首次部署前必须构建前端**
2. **必须配置API密钥**，否则OCR和AI功能无法使用
3. **首次登录后立即修改管理员密码**
4. **定期备份数据库**: `cp /var/www/essay-grader-v2/data/database.db ~/backup/`

## 🔧 常用命令

```bash
# 查看服务状态
sudo systemctl status essay-grader

# 查看日志
sudo journalctl -u essay-grader -f

# 重启服务
sudo systemctl restart essay-grader

# 更新部署
sudo bash deploy/update.sh
```

## 📞 故障排查

详见: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

**准备时间**: 2024-11-11  
**项目版本**: V2.0  
**部署状态**: ✅ 就绪

