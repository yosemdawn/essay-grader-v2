# 🔄 服务器更新指南

当你在GitHub上更新了代码后，如何更新AWS服务器上的文件。

---

## 🚀 方法一：一键更新脚本（推荐）

最简单的方法，自动备份、拉取、重启：

```bash
# SSH连接到服务器
ssh -i your-key.pem ubuntu@your-ec2-ip

# 进入项目目录
cd ~/essay-grader-v2

# 运行AWS更新脚本
sudo bash deploy/update-aws.sh
```

**这个脚本会自动：**
- ✅ 停止服务
- ✅ 备份当前版本
- ✅ 从GitHub拉取最新代码
- ✅ 保留你的 `.env` 配置
- ✅ 更新Python依赖
- ✅ 重启服务

---

## 🔄 方法二：手动Git Pull

如果你只想更新代码，不想运行完整脚本：

```bash
# 进入项目目录
cd ~/essay-grader-v2

# 拉取最新代码
git pull origin main

# 如果提示有本地修改冲突
git stash              # 暂存本地修改
git pull origin main   # 拉取最新代码
git stash pop          # 恢复本地修改（可选）

# 或者强制覆盖本地修改
git reset --hard origin/main
git pull origin main

# 重启服务
sudo systemctl restart essay-grader
```

---

## 🗑️ 方法三：删除重建

如果遇到严重问题，可以删除旧文件重新部署：

```bash
# 1. 备份配置文件（重要！）
cp ~/essay-grader-v2/backend/.env ~/env-backup

# 2. 备份数据库（如果需要）
cp ~/essay-grader-v2/data/database.db ~/db-backup.db

# 3. 停止服务
sudo systemctl stop essay-grader

# 4. 删除旧项目
cd ~
rm -rf essay-grader-v2

# 5. 重新克隆
git clone https://github.com/yosemdawn/essay-grader-v2.git
cd essay-grader-v2

# 6. 恢复配置文件
cp ~/env-backup backend/.env

# 7. 恢复数据库（如果需要）
mkdir -p data
cp ~/db-backup.db data/database.db

# 8. 重新部署
sudo bash deploy/deploy-aws.sh
```

---

## 📋 常见更新场景

### 场景1: 只更新了后端代码

```bash
cd ~/essay-grader-v2
git pull origin main
sudo systemctl restart essay-grader
```

### 场景2: 只更新了前端代码

```bash
cd ~/essay-grader-v2
git pull origin main

# 如果GitHub上已有构建文件，直接重启Nginx
sudo systemctl restart nginx

# 如果需要重新构建
cd frontend
npm install
npm run build
cd ..
sudo systemctl restart nginx
```

### 场景3: 更新了Python依赖 (requirements.txt)

```bash
cd ~/essay-grader-v2
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart essay-grader
```

### 场景4: 更新了部署脚本

```bash
cd ~/essay-grader-v2
git pull origin main
# 部署脚本已更新，下次使用时会自动生效
```

---

## ⚠️ 重要提醒

### 1. 更新前备份配置文件

你的 `.env` 文件包含API密钥，不在Git中，更新时要注意保留：

```bash
# 更新前备份
cp ~/essay-grader-v2/backend/.env ~/env-backup

# 更新后恢复
cp ~/env-backup ~/essay-grader-v2/backend/.env
```

### 2. 更新前备份数据库

如果有重要数据，先备份：

```bash
cp ~/essay-grader-v2/data/database.db ~/db-backup-$(date +%Y%m%d).db
```

### 3. 检查服务状态

更新后检查服务是否正常：

```bash
# 检查后端服务
sudo systemctl status essay-grader

# 检查Nginx
sudo systemctl status nginx

# 查看日志
sudo tail -f /var/log/essay-grader/backend.log
```

---

## 🔍 故障排查

### 问题1: git pull 提示冲突

```bash
# 查看冲突文件
git status

# 方案A: 保留远程版本（覆盖本地修改）
git reset --hard origin/main
git pull origin main

# 方案B: 保留本地修改
git stash
git pull origin main
git stash pop
```

### 问题2: 服务启动失败

```bash
# 查看详细错误
sudo journalctl -u essay-grader -n 50 --no-pager

# 检查Python环境
source ~/essay-grader-v2/venv/bin/activate
python --version
pip list

# 重新安装依赖
pip install -r ~/essay-grader-v2/backend/requirements.txt
```

### 问题3: 前端页面没更新

```bash
# 清除浏览器缓存，或强制刷新（Ctrl+F5）

# 检查前端文件
ls -la ~/essay-grader-v2/frontend/dist/

# 重启Nginx
sudo systemctl restart nginx
```

---

## 📊 更新流程对比

| 方法 | 速度 | 安全性 | 适用场景 |
|------|------|--------|----------|
| **一键更新脚本** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 推荐，自动备份 |
| **手动Git Pull** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 小改动，快速更新 |
| **删除重建** | ⭐⭐ | ⭐⭐⭐⭐ | 严重问题，完全重置 |

---

## ✅ 推荐更新流程

```bash
# 1. SSH连接
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. 进入项目
cd ~/essay-grader-v2

# 3. 运行更新脚本
sudo bash deploy/update-aws.sh

# 4. 检查状态
sudo systemctl status essay-grader

# 5. 访问测试
curl ifconfig.me  # 获取IP
# 浏览器访问: http://你的IP
```

**就这么简单！** 🎉

---

## 📝 更新记录模板

建议每次更新后记录：

```
更新时间: 2024-11-11 15:30
更新内容: 修复了XXX功能
Git提交: abc1234
备份位置: /home/ubuntu/essay-grader-v2_backup_20241111_153000
状态: ✅ 成功
```

---

需要帮助？查看 [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) 或提交 Issue。

