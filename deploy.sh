#!/bin/bash

# 考研考公双赛道情报监控系统 - 一键部署脚本

echo "========== 开始部署 =========="

# 1. 安装必要软件
echo "[1/7] 安装必要软件..."
apt update && apt install -y python3 python3-pip mysql-server redis-server nginx git

# 2. 克隆代码
echo "[2/7] 克隆代码..."
cd /root
git clone https://github.com/chongyanghui123/kaoyankaogongxinxituisongxitong.git project
cd project

# 3. 创建配置文件
echo "[3/7] 创建配置文件..."
cp backend/.env.example backend/.env
# 编辑 .env 文件，填写以下配置：
# - DATABASE_HOST=localhost (本地MySQL) 或云服务器地址
# - OSS配置 (如果使用阿里云OSS)
# - 邮箱配置
# - 微信配置

# 4. 安装Python依赖
echo "[4/7] 安装Python依赖..."
cd backend
pip3 install -r requirements.txt

# 5. 初始化数据库
echo "[5/7] 初始化数据库..."
# 创建数据库 (需要先配置MySQL)
# mysql -u root -p -e "CREATE DATABASE common_db; CREATE DATABASE kaoyan_db; CREATE DATABASE kaogong_db;"

# 6. 启动后端服务
echo "[6/7] 启动后端服务..."
cd /root/project/backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > /var/log/backend.log 2>&1 &

# 7. 构建并启动前端
echo "[7/7] 构建前端..."
cd /root/project/frontend
npm install
npm run build

# 配置Nginx
cat > /etc/nginx/sites-available/project << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        root /root/project/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo "========== 部署完成 =========="
echo "后端API: http://192.168.16.2:8000"
echo "前端页面: http://192.168.16.2"
echo "API文档: http://192.168.16.2:8000/docs"
