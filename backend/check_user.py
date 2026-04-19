#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查用户信息脚本
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db_common
from models.users import User

def check_user(phone):
    """检查用户信息"""
    db = next(get_db_common())
    try:
        user = db.query(User).filter_by(phone=phone).first()
        if user:
            print(f"用户存在:")
            print(f"ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"手机号: {user.phone}")
            print(f"邮箱: {user.email}")
            print(f"密码: {user.password}")
            print(f"是否VIP: {user.is_vip}")
            print(f"VIP类型: {user.vip_type}")
            print(f"VIP结束时间: {user.vip_end_time}")
        else:
            print(f"用户不存在: {phone}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python check_user.py <手机号>")
        sys.exit(1)
    phone = sys.argv[1]
    check_user(phone)
