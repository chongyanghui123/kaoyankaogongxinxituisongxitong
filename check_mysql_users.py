#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.core.database import get_db_common
from backend.models.users import User
from backend.core.security import get_password_hash

# 获取数据库会话
db = next(get_db_common())

print('用户表数据:')
users = db.query(User).all()
for user in users:
    print(f'ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 管理员: {user.is_admin}')
