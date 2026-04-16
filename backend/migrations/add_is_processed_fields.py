#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

# 使用直接的数据库连接
DATABASE_COMMON_URL = "mysql+pymysql://root:123456789@localhost:3306/common_db?charset=utf8mb4"
DATABASE_KAOYAN_URL = "mysql+pymysql://root:123456789@localhost:3306/kaoyan_db?charset=utf8mb4"
DATABASE_KAOGONG_URL = "mysql+pymysql://root:123456789@localhost:3306/kaogong_db?charset=utf8mb4"

# 创建数据库连接
common_engine = create_engine(DATABASE_COMMON_URL)
kaoyan_engine = create_engine(DATABASE_KAOYAN_URL)
kaogong_engine = create_engine(DATABASE_KAOGONG_URL)

def add_column_if_not_exists(engine, table_name, column_name, column_definition):
    """在指定表中添加字段（如果字段不存在）"""
    with engine.connect() as conn:
        # 检查字段是否存在
        result = conn.execute(text(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'"))
        if result.fetchone():
            print(f"字段 {column_name} 在 {table_name} 表中已存在，跳过")
            return
        
        # 添加字段
        print(f"正在为 {table_name} 表添加 {column_name} 字段...")
        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_definition}"))
        conn.commit()
        print(f"字段 {column_name} 添加成功")

# 为 common_db 数据库中的 push_logs 表添加 is_processed 字段
print("正在处理 common_db 数据库...")
add_column_if_not_exists(common_engine, 'push_logs', 'is_processed', 'is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否"')

# 为 kaoyan_db 数据库中的 kaoyan_info 表添加 is_processed 字段
print("正在处理 kaoyan_db 数据库...")
add_column_if_not_exists(kaoyan_engine, 'kaoyan_info', 'is_processed', 'is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否"')

# 为 kaogong_db 数据库中的 kaogong_info 表添加 is_processed 字段
print("正在处理 kaogong_db 数据库...")
add_column_if_not_exists(kaogong_engine, 'kaogong_info', 'is_processed', 'is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否"')

print("所有字段添加完成！")
