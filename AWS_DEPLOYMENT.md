# 🚀 AWS EC2 Ubuntu 部署指南

适用于亚马逊AWS免费套餐EC2实例（Ubuntu系统）

## 📋 前提条件

### 1. AWS EC2 实例要求
- **操作系统**: Ubuntu 20.04 LTS 或更高
- **实例类型**: t2.micro（免费套餐）或更高
- **存储**: 至少 8GB
- **安全组规则**:
  - SSH (22端口) - 允许你的IP访问
  - HTTP (80端口) - 允许所有IP访问
  - HTTPS (443端口) - 允许所有IP访问（可选）

### 2. 本地准备
- SSH密钥文件 (`.pem` 文件)
- 已申请百度OCR API密钥
- 已申请豆包LLM API密钥

---

## 🔧 步骤1: 配置AWS安全组

在AWS控制台配置安全组规则：

| 类型 | 协议 | 端口 | 来源 | 说明 |
|------|------|------|------|------|
| SSH | TCP | 22 | 你的IP | SSH登录 |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web访问 |
| HTTPS | TCP | 443 | 0.0.0.0/0 | HTTPS访问（可选）|

---

## 🚀 步骤2: 连接到服务器

### Windows用户

```powershell
# 使用PowerShell或Git Bash
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

### Mac/Linux用户

```bash
# 设置密钥权限
chmod 400 your-key.pem

# SSH连接
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

---

## 📦 步骤3: 部署项目

### 方法一：从GitHub克隆（推荐）

```bash
# 1. 克隆项目
cd ~
git clone https://github.com/yosemdawn/essay-grader-v2.git
cd essay-grader-v2

# 2. 构建前端
cd frontend
# 安装Node.js（如果没有）
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装依赖并构建
npm install
npm run build
cd ..

# 3. 运行部署脚本
sudo bash deploy/deploy-aws.sh
```

### 方法二：上传本地文件

```bash
# 在本地打包（Windows PowerShell或Mac/Linux终端）
cd essay-grader-v2
tar -czf essay-grader-v2.tar.gz .

# 上传到服务器
scp -i your-key.pem essay-grader-v2.tar.gz ubuntu@your-ec2-ip:~/

# 在服务器上解压
ssh -i your-key.pem ubuntu@your-ec2-ip
cd ~
mkdir -p essay-grader-v2
tar -xzf essay-grader-v2.tar.gz -C essay-grader-v2
cd essay-grader-v2

# 运行部署脚本
sudo bash deploy/deploy-aws.sh
```

---

## ⚙️ 步骤4: 配置API密钥

```bash
# 编辑配置文件
sudo nano /home/ubuntu/essay-grader-v2/backend/.env
```

**必须修改的配置**：

```env
# 百度OCR配置
BAIDU_OCR_API_KEY=你的百度OCR_API_KEY
BAIDU_OCR_SECRET_KEY=你的百度OCR_SECRET_KEY

# 豆包LLM配置
DOUBAO_API_KEY=你的豆包API_KEY
DOUBAO_MODEL_ID=你的豆包模型ID

# 安全密钥（生成一个随机字符串）
SECRET_KEY=your-random-32-character-secret-key-here
```

**保存并退出**: `Ctrl + X`, 然后 `Y`, 然后 `Enter`

---

## 🔄 步骤5: 重启服务

```bash
# 重启后端服务
sudo systemctl restart essay-grader

# 重启Nginx
sudo systemctl restart nginx

# 检查服务状态
sudo systemctl status essay-grader
sudo systemctl status nginx
```

---

## ✅ 步骤6: 访问系统

### 获取公网IP

```bash
curl ifconfig.me
```

### 访问地址

在浏览器打开: `http://你的EC2公网IP`

### 默认账号

- **管理员**: `admin` / `admin123`
- **学生**: 学号 / `123456`

⚠️ **首次登录后请立即修改密码！**

---

## 🔍 常用管理命令

### 查看服务状态

```bash
# 后端服务
sudo systemctl status essay-grader

# Nginx
sudo systemctl status nginx
```

### 查看日志

```bash
# 后端日志
sudo tail -f /var/log/essay-grader/backend.log

# 错误日志
sudo tail -f /var/log/essay-grader/backend-error.log

# Nginx日志
sudo tail -f /var/log/nginx/access.log
```

### 重启服务

```bash
sudo systemctl restart essay-grader
sudo systemctl restart nginx
```

### 停止服务

```bash
sudo systemctl stop essay-grader
sudo systemctl stop nginx
```

---

## 🛠️ 故障排查

### 1. 无法访问网站

```bash
# 检查Nginx是否运行
sudo systemctl status nginx

# 检查端口是否开放
sudo netstat -tlnp | grep :80

# 检查AWS安全组是否允许80端口
```

### 2. 后端服务无法启动

```bash
# 查看详细错误
sudo journalctl -u essay-grader -n 50 --no-pager

# 检查Python环境
/home/ubuntu/essay-grader-v2/venv/bin/python --version

# 手动启动测试
cd /home/ubuntu/essay-grader-v2/backend
source ../venv/bin/activate
python main.py
```

### 3. API调用失败

检查 `.env` 文件中的API密钥是否正确配置

---

## 🔐 配置HTTPS（可选）

使用Let's Encrypt免费SSL证书：

```bash
# 安装Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 申请证书（需要域名）
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 💾 数据备份

```bash
# 备份数据库
sudo cp /home/ubuntu/essay-grader-v2/data/database.db ~/backup-$(date +%Y%m%d).db

# 备份上传文件
sudo tar -czf ~/uploads-backup-$(date +%Y%m%d).tar.gz /home/ubuntu/essay-grader-v2/data/uploads/
```

---

## 📞 需要帮助？

- 查看完整文档: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- GitHub Issues: https://github.com/yosemdawn/essay-grader-v2/issues

---

**部署时间**: 约10-15分钟  
**难度**: ⭐⭐☆☆☆

