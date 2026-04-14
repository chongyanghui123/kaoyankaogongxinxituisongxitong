# 考研考公双赛道情报监控系统 - 百度云部署指南

## 📋 目录
- [服务器信息](#服务器信息)
- [前置准备](#前置准备)
- [部署步骤](#部署步骤)
- [安全配置](#安全配置)
- [常见问题](#常见问题)
- [服务管理](#服务管理)

---

## 🌐 服务器信息

### 您的百度云服务器配置
- **公网IP**: 180.76.234.28
- **内网IP**: 192.168.16.2
- **带宽**: 1Mbps
- **推荐操作系统**: Ubuntu 20.04 LTS / CentOS 7+

---

## 📦 前置准备

### 1. 本地准备

确保您在本地有完整的项目文件：

```bash
考研考公双赛道情报监控系统/
├── backend/
│   ├── .env.baiducloud      # 百度云环境配置
│   ├── requirements.txt      # Python依赖
│   └── main.py             # 后端主程序
├── frontend/
│   ├── .env.production      # 前端生产环境配置
│   └── package.json        # 前端依赖
├── docs/
│   └── database.sql         # 数据库结构
├── deploy_to_baiducloud.sh  # 部署脚本
└── BAIDUCLOUD_DEPLOYMENT.md # 本文档
```

### 2. 百度云安全组配置

在百度云控制台配置安全组，开放以下端口：

| 端口 | 协议 | 用途 | 说明 |
|------|------|------|------|
| 22 | TCP | SSH | 远程连接服务器 |
| 80 | TCP | HTTP | Web服务访问 |
| 443 | TCP | HTTPS | 加密Web访问（可选） |

**配置步骤**：
1. 登录百度云控制台
2. 进入云服务器 BCC → 安全组
3. 创建或编辑安全组规则
4. 添加上述端口规则

### 3. 远程连接服务器

使用 SSH 连接到您的百度云服务器：

```bash
# 使用 root 用户连接（请替换为实际用户名）
ssh root@180.76.234.28

# 如果有非 root 用户，推荐使用非 root 用户
ssh your_username@180.76.234.28
```

---

## 🚀 部署步骤

### 方式一：使用自动化部署脚本（推荐）

#### 步骤 1: 上传项目文件到服务器

在本地终端执行：

```bash
# 1. 进入项目目录
cd /path/to/考研考公双赛道情报监控系统

# 2. 给部署脚本添加执行权限
chmod +x deploy_to_baiducloud.sh

# 3. 上传项目文件到服务器
scp -r deploy_to_baiducloud.sh root@180.76.234.28:/root/

# 4. 上传完整项目（注意：这可能需要一些时间）
scp -r backend root@180.76.234.28:/root/kao-system/
scp -r frontend root@180.76.234.28:/root/kao-system/
scp -r docs root@180.76.234.28:/root/kao-system/
```

或者使用 rsync（更快）：

```bash
# 使用 rsync 同步项目（推荐）
rsync -avz --progress ./ root@180.76.234.28:/root/kao-system/
```

#### 步骤 2: 在服务器上执行部署脚本

```bash
# 1. SSH 连接到服务器
ssh root@180.76.234.28

# 2. 进入项目目录
cd /root/kao-system

# 3. 给部署脚本执行权限
chmod +x deploy_to_baiducloud.sh

# 4. 执行部署脚本
./deploy_to_baiducloud.sh
```

部署脚本会自动完成以下工作：
- ✅ 更新系统包管理器
- ✅ 安装基础工具
- ✅ 安装 Python 3.8+
- ✅ 安装 MySQL 数据库
- ✅ 安装 Redis 缓存
- ✅ 安装 Node.js 和 npm
- ✅ 设置 Python 虚拟环境
- ✅ 安装项目依赖
- ✅ 配置环境变量
- ✅ 创建数据库
- ✅ 导入数据库结构
- ✅ 构建前端
- ✅ 安装并配置 Nginx
- ✅ 创建 systemd 服务
- ✅ 启动所有服务

---

### 方式二：手动部署

如果您想更精细地控制部署过程，可以按以下步骤手动部署。

#### 1. 系统环境准备

```bash
# 更新系统
apt update && apt upgrade -y  # Ubuntu
# 或
yum update -y                  # CentOS

# 安装基础工具
apt install -y curl wget git vim net-tools  # Ubuntu
# 或
yum install -y curl wget git vim net-tools  # CentOS
```

#### 2. 安装 Python 3.8+

```bash
# Ubuntu/Debian
apt install -y python3 python3-pip python3-venv

# CentOS/RHEL
yum install -y python3 python3-pip

# 验证安装
python3 --version
pip3 --version

# 升级 pip
pip3 install --upgrade pip
```

#### 3. 安装 MySQL

```bash
# Ubuntu/Debian
apt install -y mysql-server

# CentOS/RHEL
yum install -y mysql-server
systemctl start mysqld
systemctl enable mysqld

# 启动 MySQL
systemctl start mysql    # Ubuntu
systemctl start mysqld   # CentOS
systemctl enable mysql   # 设置开机自启
```

**安全配置（重要）**：

```bash
# 运行 MySQL 安全配置脚本
mysql_secure_installation

# 按照提示设置：
# 1. 设置 root 密码（请使用强密码）
# 2. 移除匿名用户
# 3. 禁止 root 远程登录
# 4. 移除测试数据库
# 5. 重新加载权限表
```

#### 4. 安装 Redis

```bash
# Ubuntu/Debian
apt install -y redis-server

# CentOS/RHEL
yum install -y redis

# 启动 Redis
systemctl start redis-server  # Ubuntu
systemctl start redis         # CentOS
systemctl enable redis-server # 开机自启

# 验证 Redis
redis-cli ping
# 应该返回 PONG
```

#### 5. 安装 Node.js 和 npm

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# 验证安装
node -v
npm -v
```

#### 6. 上传并配置项目

```bash
# 创建项目目录
mkdir -p /root/kao-system
cd /root/kao-system

# 上传项目文件（从本地执行）
# scp -r ./ root@180.76.234.28:/root/kao-system/

# 配置后端
cd backend

# 创建 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.baiducloud .env

# 编辑 .env 文件，修改敏感配置
vim .env
# 需要修改的配置：
# - DATABASE_PASSWORD: MySQL root 密码
# - SECRET_KEY: 随机生成的长字符串
# - 其他第三方服务密钥
```

#### 7. 创建数据库

```bash
# 登录 MySQL
mysql -u root -p

# 在 MySQL 中执行以下 SQL
CREATE DATABASE IF NOT EXISTS common_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS kaoyan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS kaogong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出 MySQL
exit;

# 导入数据库结构
mysql -u root -p common_db < docs/database.sql
mysql -u root -p kaoyan_db < docs/database.sql
mysql -u root -p kaogong_db < docs/database.sql
```

#### 8. 构建前端

```bash
cd /root/kao-system/frontend

# 配置前端环境变量
cp .env.production .env

# 安装依赖
npm install

# 构建生产版本
npm run build
```

#### 9. 安装并配置 Nginx

```bash
# 安装 Nginx
apt install -y nginx  # Ubuntu
# 或
yum install -y nginx  # CentOS

# 创建 Nginx 配置文件
vim /etc/nginx/sites-available/kao-system
```

粘贴以下内容：

```nginx
server {
    listen 80;
    server_name 180.76.234.28;

    client_max_body_size 20M;

    # 前端静态文件
    location / {
        root /root/kao-system/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

```bash
# 启用站点
ln -sf /etc/nginx/sites-available/kao-system /etc/nginx/sites-enabled/

# 测试 Nginx 配置
nginx -t

# 重启 Nginx
systemctl restart nginx
systemctl enable nginx
```

#### 10. 创建 systemd 服务

```bash
# 创建后端服务文件
vim /etc/systemd/system/kao-backend.service
```

粘贴以下内容：

```ini
[Unit]
Description=双赛道情报通后端服务
After=network.target mysql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/kao-system/backend
Environment="PATH=/root/kao-system/backend/venv/bin"
ExecStart=/root/kao-system/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 重载 systemd 配置
systemctl daemon-reload

# 启动后端服务
systemctl start kao-backend
systemctl enable kao-backend

# 查看服务状态
systemctl status kao-backend
```

---

## 🔒 安全配置

### 1. 修改 SSH 配置（安全建议）

```bash
# 编辑 SSH 配置
vim /etc/ssh/sshd_config

# 修改以下配置：
Port 2222                    # 改为非默认端口
PermitRootLogin no           # 禁止 root 直接登录
PasswordAuthentication yes   # 保持密码认证（如有密钥可改为 no）

# 重启 SSH 服务
systemctl restart sshd
```

### 2. 配置防火墙

```bash
# Ubuntu 使用 UFW
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# CentOS 使用 firewalld
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload
```

### 3. 配置 HTTPS（可选但推荐）

使用 Let's Encrypt 免费证书：

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx  # Ubuntu
# 或
yum install -y certbot python3-certbot-nginx  # CentOS

# 获取证书（需要有域名）
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

---

## 🔧 服务管理

### 常用命令

```bash
# 查看后端服务状态
systemctl status kao-backend

# 查看后端日志
journalctl -u kao-backend -f

# 重启后端服务
systemctl restart kao-backend

# 停止后端服务
systemctl stop kao-backend

# 查看 Nginx 状态
systemctl status nginx

# 重启 Nginx
systemctl restart nginx

# 查看 Nginx 错误日志
tail -f /var/log/nginx/error.log

# 查看 Nginx 访问日志
tail -f /var/log/nginx/access.log

# 查看 MySQL 状态
systemctl status mysql

# 查看 Redis 状态
systemctl status redis-server
```

### 后端日志位置

- 应用日志: `/root/kao-system/backend/logs/app.log`
- Systemd 日志: `journalctl -u kao-backend -f`

---

## ❓ 常见问题

### 1. 部署脚本执行失败

**问题**: 脚本执行过程中出现错误

**解决方案**:
- 检查网络连接是否正常
- 确保有足够的磁盘空间
- 查看错误日志，手动执行失败的步骤

### 2. 无法访问网站

**问题**: 浏览器访问 http://180.76.234.28 无法打开

**检查清单**:
- [ ] 百度云安全组是否开放了 80 端口
- [ ] Nginx 服务是否运行: `systemctl status nginx`
- [ ] 防火墙是否允许 80 端口
- [ ] 前端构建文件是否存在: `ls -la /root/kao-system/frontend/dist/`

### 3. API 请求失败

**问题**: 前端页面显示但 API 请求失败

**检查清单**:
- [ ] 后端服务是否运行: `systemctl status kao-backend`
- [ ] Nginx 配置中的 proxy_pass 是否正确
- [ ] 后端日志是否有错误: `journalctl -u kao-backend -n 50`
- [ ] 数据库连接是否正常

### 4. 数据库连接失败

**问题**: 后端日志显示数据库连接错误

**解决方案**:
- 检查 MySQL 服务是否运行: `systemctl status mysql`
- 验证 .env 文件中的数据库密码是否正确
- 测试数据库连接: `mysql -u root -p`

### 5. 内存不足

**问题**: 部署过程中出现内存不足错误

**解决方案**:
- 升级服务器配置（推荐）
- 或创建交换文件：

```bash
# 创建 2GB 交换文件
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

## 📊 访问地址

部署完成后，您可以通过以下地址访问系统：

| 服务 | 地址 |
|------|------|
| 前端页面 | http://180.76.234.28 |
| 后端API | http://180.76.234.28/api/v1 |
| API文档 | http://180.76.234.28/docs |
| 管理后台 | http://180.76.234.28/admin |

### 默认管理员账号

- **用户名**: admin
- **密码**: admin123

⚠️ **重要**: 首次登录后请立即修改管理员密码！

---

## 🆘 获取帮助

如果在部署过程中遇到问题：

1. 查看本文档的「常见问题」章节
2. 检查服务日志
3. 查看系统运行状态
4. 联系技术支持

---

## 📝 更新记录

- 2026-04-11: 初始版本，支持百度云部署

---

**祝您部署顺利！** 🎉
