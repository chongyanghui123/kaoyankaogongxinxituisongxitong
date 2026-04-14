#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.common import User, UserSubscription

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

try:
    print("=== 查询所有用户 ===")
    users = db.query(User).filter(User.is_admin == False).all()
    for user in users:
        print(f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
        
        # 查询该用户的订阅
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id
        ).all()
        
        if subscriptions:
            print(f"  订阅数量: {len(subscriptions)}")
            for sub in subscriptions:
                print(f"    订阅ID: {sub.id}, 类型: {sub.subscribe_type}, 状态: {sub.status}, 创建时间: {sub.created_at}")
        else:
            print(f"  没有订阅记录")
        
        print()
    
    print("\n=== 查询所有有效的订阅（status=1） ===")
    active_subscriptions = db.query(UserSubscription).filter(
        UserSubscription.status == 1
    ).all()
    print(f"有效订阅数量: {len(active_subscriptions)}")
    for sub in active_subscriptions:
        print(f"订阅ID: {sub.id}, 用户ID: {sub.user_id}, 类型: {sub.subscribe_type}, 状态: {sub.status}")
        
finally:
    db.close()
