#!/bin/bash
# ============================================================================
# 考研考公双赛道情报监控系统 - 百度云部署脚本
# ============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 项目配置
PROJECT_DIR="/root/kao-system"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"

echo "=================================================="
echo "  考研考公双赛道情报监控系统 - 百度云部署"
echo "=================================================="
echo ""

# 检查是否在本地还是在服务器上
if [ "$(hostname)" != "localhost" ] && [ "$(hostname)" != "127.0.0.1" ]; then
    log_info "检测到在服务器上运行，开始部署流程"
else
    log_warn "检测到在本地运行，请将此脚本上传到百度云服务器后执行"
    log_info "上传命令示例: scp deploy_to_baiducloud.sh root@180.76.234.28:/root/"
    exit 0
fi

# ============================================================================
# 1. 系统环境准备
# ============================================================================
log_info "=========================================="
log_info "阶段 1/7: 系统环境准备"
log_info "=========================================="

# 检查操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    log_info "检测到操作系统: $PRETTY_NAME"
else
    log_error "无法检测操作系统"
    exit 1
fi

# 更新系统
log_info "更新系统包管理器..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    apt-get update -y
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    yum update -y
fi

# ============================================================================
# 2. 安装基础依赖
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 2/7: 安装基础依赖"
log_info "=========================================="

log_info "安装基础工具..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    apt-get install -y curl wget git vim net-tools
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    yum install -y curl wget git vim net-tools
fi

# ============================================================================
# 3. 安装 Python 3.8+
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 3/7: 安装 Python 3.8+"
log_info "=========================================="

if ! command -v python3 &> /dev/null; then
    log_info "安装 Python 3.8..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        apt-get install -y python3 python3-pip python3-venv
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y python3 python3-pip
    fi
else
    PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    log_info "检测到 Python 版本: $PYTHON_VERSION"
    
    # 检查版本是否 >= 3.8
    if python3 -c "import sys; assert sys.version_info >= (3, 8), 'Python version too old'"; then
        log_info "Python 版本符合要求"
    else
        log_error "Python 版本过低，需要 3.8 或更高版本"
        exit 1
    fi
fi

log_info "升级 pip..."
python3 -m pip install --upgrade pip

# ============================================================================
# 4. 安装 MySQL
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 4/7: 安装 MySQL"
log_info "=========================================="

if ! command -v mysql &> /dev/null; then
    log_info "安装 MySQL 服务器..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y mysql-server
        systemctl start mysqld
        systemctl enable mysqld
    fi
else
    log_info "MySQL 已安装"
fi

# 启动 MySQL
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    if ! systemctl is-active --quiet mysql; then
        log_info "启动 MySQL 服务..."
        systemctl start mysql
        systemctl enable mysql
    fi
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    if ! systemctl is-active --quiet mysqld; then
        log_info "启动 MySQL 服务..."
        systemctl start mysqld
        systemctl enable mysqld
    fi
fi

# ============================================================================
# 5. 安装 Redis
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 5/7: 安装 Redis"
log_info "=========================================="

if ! command -v redis-server &> /dev/null; then
    log_info "安装 Redis..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        apt-get install -y redis-server
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y redis
    fi
else
    log_info "Redis 已安装"
fi

# 启动 Redis
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    if ! systemctl is-active --quiet redis-server; then
        log_info "启动 Redis 服务..."
        systemctl start redis-server
        systemctl enable redis-server
    fi
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    if ! systemctl is-active --quiet redis; then
        log_info "启动 Redis 服务..."
        systemctl start redis
        systemctl enable redis
    fi
fi

# ============================================================================
# 6. 安装 Node.js 和 npm
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 6/7: 安装 Node.js 和 npm"
log_info "=========================================="

if ! command -v node &> /dev/null; then
    log_info "安装 Node.js..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt-get install -y nodejs
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
        yum install -y nodejs
    fi
else
    NODE_VERSION=$(node -v)
    log_info "检测到 Node.js 版本: $NODE_VERSION"
fi

# ============================================================================
# 7. 部署应用
# ============================================================================
log_info ""
log_info "=========================================="
log_info "阶段 7/7: 部署应用"
log_info "=========================================="

# 创建项目目录
log_info "创建项目目录..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 克隆或复制项目（这里需要用户手动上传项目文件）
log_warn "请上传项目文件到 $PROJECT_DIR 目录"
log_info "示例命令: scp -r /path/to/kao-system/* root@180.76.234.28:$PROJECT_DIR/"
echo ""

# 检查项目文件是否存在
if [ ! -d "$BACKEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
    log_warn "项目文件未找到，请先上传项目文件"
    log_info "上传后重新运行此脚本"
    exit 1
fi

# 设置 Python 虚拟环境
log_info "设置 Python 虚拟环境..."
cd $BACKEND_DIR
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 安装 Python 依赖
log_info "安装 Python 依赖..."
pip install -r requirements.txt

# 配置环境变量
log_info "配置环境变量..."
cp .env.baiducloud .env
log_warn "请编辑 .env 文件，修改数据库密码等敏感信息"

# 创建数据库
log_info "创建数据库..."
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS common_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS kaoyan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS kaogong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

# 导入数据库结构
if [ -f "../docs/database.sql" ]; then
    log_info "导入数据库结构..."
    mysql -u root -p common_db < ../docs/database.sql
    mysql -u root -p kaoyan_db < ../docs/database.sql
    mysql -u root -p kaogong_db < ../docs/database.sql
fi

# 构建前端
log_info "构建前端..."
cd $FRONTEND_DIR
cp .env.production .env
npm install
npm run build

# 安装 Nginx
log_info "安装 Nginx..."
if ! command -v nginx &> /dev/null; then
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        apt-get install -y nginx
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y nginx
    fi
fi

# 配置 Nginx
log_info "配置 Nginx..."
NGINX_CONF="/etc/nginx/sites-available/kao-system"
if [ ! -f "$NGINX_CONF" ]; then
    cat > $NGINX_CONF << 'EOF'
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
EOF

    # 启用站点
    ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
fi

# 测试 Nginx 配置
nginx -t

# 重启 Nginx
log_info "重启 Nginx..."
systemctl restart nginx
systemctl enable nginx

# 创建 systemd 服务文件
log_info "创建后端服务..."
BACKEND_SERVICE="/etc/systemd/system/kao-backend.service"
if [ ! -f "$BACKEND_SERVICE" ]; then
    cat > $BACKEND_SERVICE << 'EOF'
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
EOF

    systemctl daemon-reload
fi

# 启动后端服务
log_info "启动后端服务..."
systemctl start kao-backend
systemctl enable kao-backend

# ============================================================================
# 部署完成
# ============================================================================
echo ""
echo "=================================================="
log_info "部署完成！"
echo "=================================================="
echo ""
log_info "服务访问地址："
echo "  - 前端页面: http://180.76.234.28"
echo "  - 后端API:  http://180.76.234.28/api/v1"
echo "  - API文档:  http://180.76.234.28/docs"
echo ""
log_info "服务管理命令："
echo "  - 查看后端状态: systemctl status kao-backend"
echo "  - 重启后端:     systemctl restart kao-backend"
echo "  - 查看后端日志: journalctl -u kao-backend -f"
echo "  - 重启Nginx:    systemctl restart nginx"
echo ""
log_warn "重要：请确保百度云安全组已开放以下端口："
echo "  - 80 (HTTP)"
echo "  - 443 (HTTPS，如需要)"
echo ""
log_warn "请修改 .env 文件中的敏感配置："
echo "  - DATABASE_PASSWORD (数据库密码)"
echo "  - SECRET_KEY (JWT密钥)"
echo "  - 其他第三方服务密钥"
echo ""
