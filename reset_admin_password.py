#!/usr/bin/env python3
# 重置管理员密码

import os
import sys

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from core.database import get_db_common
from models.users import User
from core.security import get_password_hash

# 获取数据库连接
db = next(get_db_common())

try:
    # 查找管理员用户
    admin = db.query(User).filter(User.is_admin == 1).first()
    
    if admin:
        # 重置密码为admin123
        hashed_password = get_password_hash('admin123')
        print(f"生成的哈希密码: {hashed_password}")
        admin.password = hashed_password
        db.commit()
        print('管理员密码已重置为admin123')
    else:
        # 创建新的管理员用户
        from datetime import datetime, timedelta
        hashed_password = get_password_hash("admin123")
        print(f"生成的哈希密码: {hashed_password}")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            phone="13800138000",
            password=hashed_password,
            is_admin=True,
            is_active=True,
            is_vip=True,
            vip_type=3,  # 双赛道
            vip_start_time=datetime.now(),
            vip_end_time=datetime.now() + timedelta(days=365*10)  # 10年有效期
        )
        db.add(admin_user)
        db.commit()
        print('管理员用户创建成功，密码为admin123')
except Exception as e:
    print(f"错误: {e}")
finally:
    db.close()
