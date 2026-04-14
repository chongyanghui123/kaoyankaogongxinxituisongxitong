# 双赛道情报通系统部署指南

## 1. 系统要求

- **操作系统**: Ubuntu 20.04 LTS 或 CentOS 7+
- **Python**: 3.8+
- **MySQL**: 5.7+
- **Node.js**: 16.0+
- **Redis**: 6.0+ (用于缓存和任务队列)
- **Nginx**: 1.18+ (用于反向代理)

## 2. 数据库配置

### 2.1 创建数据库

1. 登录MySQL：
   ```bash
   mysql -u root -p
   ```

2. 创建数据库：
   ```sql
   -- 创建通用数据库
   CREATE DATABASE common_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- 创建考研数据库
   CREATE DATABASE kaoyan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- 创建考公数据库
   CREATE DATABASE kaogong_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 创建数据库用户并授权：
   ```sql
   CREATE USER 'kao_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON common_db.* TO 'kao_user'@'localhost';
   GRANT ALL PRIVILEGES ON kaoyan_db.* TO 'kao_user'@'localhost';
   GRANT ALL PRIVILEGES ON kaogong_db.* TO 'kao_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 2.2 导入数据库结构

```bash
mysql -u kao_user -p common_db < docs/database.sql
mysql -u kao_user -p kaoyan_db < docs/database.sql
mysql -u kao_user -p kaogong_db < docs/database.sql
```

## 3. 后端部署

### 3.1 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3.2 配置环境变量

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL="mysql+pymysql://kao_user:your_password@localhost/common_db"
KaoYan_DATABASE_URL="mysql+pymysql://kao_user:your_password@localhost/kaoyan_db"
KaoGong_DATABASE_URL="mysql+pymysql://kao_user:your_password@localhost/kaogong_db"

# Redis配置
REDIS_URL="redis://localhost:6379/0"

# JWT配置
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 服务器配置
HOST="0.0.0.0"
PORT=8000

# 爬虫配置
CRAWLER_INTERVAL=3600
CRAWLER_TIMEOUT=300

# 推送配置
WECHAT_APPID="your_wechat_appid"
WECHAT_APPSECRET="your_wechat_appsecret"
WECHAT_TEMPLATE_ID="your_wechat_template_id"

# 支付配置
WECHAT_MCHID="your_wechat_mchid"
WECHAT_API_KEY="your_wechat_api_key"
ALIPAY_APPID="your_alipay_appid"
ALIPAY_PRIVATE_KEY="your_alipay_private_key"
ALIPAY_PUBLIC_KEY="your_alipay_public_key"

# 日志配置
LOG_LEVEL="INFO"
```

### 3.3 启动后端服务

#### 开发环境

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产环境

使用 Gunicorn 启动：

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## 4. 前端部署

### 4.1 安装依赖

```bash
cd frontend
npm install
```

### 4.2 配置环境变量

创建 `.env` 文件：

```env
VITE_API_BASE_URL="http://localhost:8000/api/v1"
VITE_APP_TITLE="双赛道情报通"
VITE_APP_VERSION="1.0.0"
```

### 4.3 构建前端

```bash
npm run build
```

### 4.4 部署前端静态文件

将 `dist` 目录下的文件复制到 Nginx 配置的静态文件目录：

```bash
cp -r dist/* /var/www/html/
```

## 5. Nginx 配置

创建 Nginx 配置文件：

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

重启 Nginx：

```bash
sudo systemctl restart nginx
```

## 6. 爬虫配置

### 6.1 配置爬虫定时任务

使用 `systemd` 配置 Celery 服务：

创建 `/etc/systemd/system/celery.service` 文件：

```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/project/backend
ExecStart=/path/to/venv/bin/celery -A core.tasks worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

启动并启用 Celery 服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start celery
sudo systemctl enable celery
```

## 7. 系统初始化

### 7.1 创建管理员账户

使用 Python 脚本创建管理员账户：

```python
# create_admin.py
from backend.core.database import get_db
from backend.core.auth import create_user

db = next(get_db())
create_user(db, "admin", "admin@example.com", "admin123", "13800138000", is_admin=True)
print("管理员账户创建成功")
```

运行脚本：

```bash
python create_admin.py
```

### 7.2 初始化系统配置

登录管理员后台，配置系统参数：

1. 访问 `http://example.com/admin`
2. 使用管理员账户登录
3. 进入系统配置页面，设置系统参数

## 8. 监控与维护

### 8.1 日志管理

- 后端日志：`backend/logs/` 目录
- 爬虫日志：`backend/logs/crawler/` 目录
- Nginx 日志：`/var/log/nginx/` 目录

### 8.2 系统监控

使用 Prometheus 和 Grafana 监控系统运行状态：

1. 安装 Prometheus 和 Grafana
2. 配置 Prometheus 采集 FastAPI 指标
3. 在 Grafana 中创建监控面板

### 8.3 定期维护

1. 定期清理数据库中的过期数据
2. 定期备份数据库
3. 检查爬虫运行状态
4. 更新系统依赖

## 9. 常见问题

### 9.1 数据库连接失败

- 检查数据库服务是否运行
- 检查数据库用户名和密码是否正确
- 检查数据库权限是否正确

### 9.2 爬虫无法运行

- 检查网络连接是否正常
- 检查爬虫配置是否正确
- 检查 Celery 服务是否运行

### 9.3 前端页面无法访问

- 检查 Nginx 服务是否运行
- 检查前端静态文件是否正确部署
- 检查 API 接口是否可以正常访问

### 9.4 推送通知失败

- 检查微信公众号配置是否正确
- 检查用户是否关注了公众号
- 检查推送模板是否正确

## 10. 升级指南

### 10.1 代码更新

1. 拉取最新代码：
   ```bash
   git pull origin main
   ```

2. 更新后端依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. 更新前端依赖：
   ```bash
   cd frontend
   npm install
   npm run build
   ```

4. 重启服务：
   ```bash
   sudo systemctl restart celery
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

### 10.2 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
cd backend
alembic upgrade head
```

## 11. 安全注意事项

1. 定期更新系统依赖，修复安全漏洞
2. 使用 HTTPS 协议保护数据传输
3. 配置防火墙，限制访问端口
4. 定期备份数据库和配置文件
5. 监控系统日志，及时发现异常

## 12. 联系方式

- 技术支持：support@example.com
- 系统文档：http://example.com/docs
- GitHub 仓库：https://github.com/example/kao-system
