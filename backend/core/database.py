#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 数据库连接模块
"""

import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from config import settings

# 创建数据库引擎
def create_db_engine(database_name: str):
    """创建数据库引擎 - 根据配置选择MySQL或SQLite"""
    
    # 优先使用MySQL配置（如果环境变量中配置了）
    if settings.DATABASE_HOST and settings.DATABASE_USER:
        db_url = (
            f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
            f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{database_name}"
        )
        print(f"使用MySQL数据库: {db_url}")
        
        engine = create_engine(
            db_url,
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            pool_timeout=30,
            pool_pre_ping=True,
            pool_use_lifo=True,
            echo=settings.DEBUG
        )
        return engine
    
    # 否则使用SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", f"{database_name}.db")
    
    # 确保data目录存在
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    db_url = f"sqlite:///{db_path}"
    
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_use_lifo=True,
        echo=settings.DEBUG
    )
    return engine

# 创建各个分库的引擎
common_db_engine = create_db_engine(settings.COMMON_DB)
kaoyan_db_engine = create_db_engine(settings.KAOYAN_DB)
kaogong_db_engine = create_db_engine(settings.KAOGONG_DB)

# 导出默认引擎（用于main.py）
engine = common_db_engine

# 创建会话工厂
SessionLocalCommon = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=common_db_engine
)

SessionLocalKaoyan = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=kaoyan_db_engine
)

SessionLocalKaogong = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=kaogong_db_engine
)

# 基础模型类
BaseCommon = declarative_base()
BaseKaoyan = declarative_base()
BaseKaogong = declarative_base()

# 获取数据库会话的依赖函数
def get_db_common() -> Generator:
    """获取公共库会话"""
    db = SessionLocalCommon()
    try:
        yield db
    finally:
        db.close()

def get_db_kaoyan() -> Generator:
    """获取考研库会话"""
    db = SessionLocalKaoyan()
    try:
        yield db
    finally:
        db.close()

def get_db_kaogong() -> Generator:
    """获取考公库会话"""
    db = SessionLocalKaogong()
    try:
        yield db
    finally:
        db.close()

# 默认的get_db函数（用于需要根据上下文自动选择的场景）
def get_db(database: str = "common") -> Generator:
    """根据数据库类型获取会话"""
    if database == "common":
        yield from get_db_common()
    elif database == "kaoyan":
        yield from get_db_kaoyan()
    elif database == "kaogong":
        yield from get_db_kaogong()
    else:
        raise ValueError(f"Unknown database type: {database}")

# 测试数据库连接
def test_db_connections():
    """测试数据库连接"""
    databases = {
        "common_db": common_db_engine,
        "kaoyan_db": kaoyan_db_engine,
        "kaogong_db": kaogong_db_engine
    }
    
    results = []
    for db_name, engine in databases.items():
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                if result.scalar() == 1:
                    results.append(f"{db_name}: 连接成功")
                else:
                    results.append(f"{db_name}: 连接失败")
        except Exception as e:
            results.append(f"{db_name}: 连接异常 - {str(e)}")
    
    return results

if __name__ == "__main__":
    print("测试数据库连接:")
    results = test_db_connections()
    for result in results:
        print(f"  {result}")