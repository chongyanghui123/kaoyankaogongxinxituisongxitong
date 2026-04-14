#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.core.database import get_db_common
from backend.models.users import User
from backend.core.security import get_password_hash
from datetime import datetime, timedelta

# 获取数据库会话
db = next(get_db_common())

print('用户表数据:')
users = db.query(User).all()
for user in users:
    print(f'ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 管理员: {user.is_admin}')

# 检查是否需要初始化管理员用户
admin_user = db.query(User).filter(User.is_admin == True).first()
if not admin_user:
    print('\n创建管理员用户:')
    admin = User(
        username='admin',
        email='admin@shuangsai.com',
        phone='13800138000',
        password='admin123',  # 存储明文密码
        real_name='系统管理员',
        avatar=None,
        gender='男',
        birthdate=None,
        is_admin=True,
        is_active=True,
        is_vip=True,
        vip_type=3,
        trial_status=2,
        vip_start_time=datetime.now(),
        vip_end_time=datetime.now() + timedelta(days=3650),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(admin)
    db.commit()
    print('管理员用户创建成功')
