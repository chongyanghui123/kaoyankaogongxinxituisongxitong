#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查所有用户信息脚本
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db_common
from models.users import User

def check_all_users():
    """检查所有用户信息"""
    db = next(get_db_common())
    try:
        users = db.query(User).all()
        print(f"总用户数: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, 手机号: {user.phone}, 用户名: {user.username}, 密码: {user.password}")
    finally:
        db.close()

if __name__ == "__main__":
    check_all_users()
