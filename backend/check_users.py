#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的用户信息
"""

from core.database import get_db_common
from models.users import User

def check_users():
    """检查数据库中的用户信息"""
    db = next(get_db_common())
    try:
        users = db.query(User).all()
        print("数据库中的用户信息:")
        print("ID | 用户名 | 密码 | 是否管理员")
        print("-" * 50)
        for user in users:
            print(f"{user.id} | {user.username} | {user.password} | {user.is_admin}")
    except Exception as e:
        print(f"查询用户信息失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
