#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取用户 Token 脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import jwt
from datetime import datetime, timedelta
from config import settings
from models.users import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问 Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_user_token(user_id):
    """获取用户 Token"""
    try:
        # 连接数据库
        database_url = f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.COMMON_DB}"
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"User with id {user_id} not found")
            return None
            
        # 创建 Token
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires
        )
        
        print(f"Token for user {user.username} (ID: {user.id}): {access_token}")
        print(f"VIP Type: {user.vip_type}")
        return access_token
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    # 获取用户 ID 为 1 的 Token（管理员用户）
    if len(sys.argv) > 1:
        get_user_token(int(sys.argv[1]))
    else:
        print("Usage: python get_token.py <user_id>")