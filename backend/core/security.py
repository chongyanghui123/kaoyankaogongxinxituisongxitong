#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 安全模块
"""

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import settings
from core.database import get_db_common
from models.users import User



# JWT配置
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# HTTPBearer认证
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码（直接比较明文）"""
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """获取密码哈希（直接返回明文）"""
    return password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> dict:
    """验证令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = {"user_id": user_id}
        
    except JWTError:
        raise credentials_exception
        
    return token_data

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_common)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials, credentials_exception)
    
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    
    if user is None:
        raise credentials_exception
    
    # 检查服务到期时间
    if user.is_vip and user.vip_end_time:
        if datetime.now() > user.vip_end_time:
            # 服务到期，更新用户状态
            user.is_vip = False
            user.is_active = False  # 设置为非活跃，在用户管理页面显示为"到期"
            db.commit()
        
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
        
    return current_user

def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃的管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
        
    return current_user

def get_current_active_vip(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃的VIP用户"""
    if not current_user.is_vip:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要VIP权限"
        )
        
    # 检查VIP是否过期
    if current_user.vip_end_time and current_user.vip_end_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="VIP已过期"
        )
        
    return current_user

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_phone(phone: str) -> bool:
    """验证手机号格式"""
    import re
    phone_regex = r'^1[3-9]\d{9}$'
    return re.match(phone_regex, phone) is not None

def validate_password(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 6:
        return False
        
    # 至少包含一个字母和一个数字
    import re
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
        return False
        
    return True

def generate_verification_code(length: int = 6) -> str:
    """生成验证码"""
    import random
    import string
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

def hash_text(text: str) -> str:
    """对文本进行哈希处理"""
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def is_safe_url(target: str, allowed_hosts: list) -> bool:
    """验证URL安全性"""
    from urllib.parse import urlparse, urljoin
    from fastapi import Request
    
    if target and target.startswith("/"):
        return True
        
    if target and target.startswith("http://") or target.startswith("https://"):
        parsed_url = urlparse(target)
        return parsed_url.netloc in allowed_hosts
        
    return False