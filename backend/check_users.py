#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查用户记录脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models.users import User, UserSubscription

def check_users():
    """检查用户记录"""
    try:
        # 连接数据库
        database_url = f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.COMMON_DB}"
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("=== 用户记录 ===")
        users = db.query(User).limit(10).all()
        for user in users:
            subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == user.id
            ).first()
            subscribe_type = subscription.subscribe_type if subscription else "无"
            
            print(f"ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"VIP类型: {user.vip_type}")
            print(f"订阅类型: {subscribe_type}")
            print("-" * 50)
            
        db.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_users()