#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

# 使用直接的数据库连接
DATABASE_URL = "mysql+pymysql://root:123456789@localhost:3306/common_db?charset=utf8mb4"

# 创建数据库连接
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("开始删除trial_start_time和trial_end_time字段...")
    
    # 检查字段是否存在并删除
    def drop_column_if_exists(column_name):
        # 检查字段是否存在
        result = conn.execute(text(f"SHOW COLUMNS FROM users LIKE '{column_name}'"))
        if result.fetchone():
            print(f"字段 {column_name} 存在，正在删除...")
            conn.execute(text(f"ALTER TABLE users DROP COLUMN {column_name}"))
            print(f"字段 {column_name} 删除成功")
        else:
            print(f"字段 {column_name} 不存在，跳过")
    
    # 删除trial_start_time字段
    drop_column_if_exists('trial_start_time')
    
    # 删除trial_end_time字段
    drop_column_if_exists('trial_end_time')
    
    conn.commit()
    print("迁移完成！")
