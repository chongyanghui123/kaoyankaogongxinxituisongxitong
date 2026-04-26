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

session = SessionLocalCommon()

def update_user_passwords(default_password: str = None):
    """为现有用户设置默认密码"""
    if default_password is None:
        default_password = os.getenv("DEFAULT_USER_PASSWORD", "changeme123")

    try:
        users = session.query(User).all()
        
        updated_count = 0
        
        for user in users:
            if not user.password or user.password == "":
                user.password = get_password_hash(default_password)
                updated_count += 1
        
        session.commit()
        
        print(f"成功更新 {updated_count} 个用户的密码")
        
    except Exception as e:
        print(f"更新密码时出错: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    update_user_passwords()
