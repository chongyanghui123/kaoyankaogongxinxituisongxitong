#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为现有用户设置默认密码
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import common_db_engine, BaseCommon, SessionLocalCommon
from core.security import get_password_hash
from models.users import User
from sqlalchemy.orm import sessionmaker

# 创建数据库会话
session = SessionLocalCommon()

def update_user_passwords():
    """为现有用户设置默认密码"""
    try:
        # 获取所有用户
        users = session.query(User).all()
        
        # 为每个用户设置默认密码
        default_password = "123456789"
        updated_count = 0
        
        for user in users:
            # 检查用户是否已有密码
            if not user.password or user.password == "":
                # 设置默认密码
                user.password = get_password_hash(default_password)
                updated_count += 1
        
        # 提交更改
        session.commit()
        
        print(f"成功更新 {updated_count} 个用户的密码")
        print(f"默认密码: {default_password}")
        
    except Exception as e:
        print(f"更新密码时出错: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    update_user_passwords()
