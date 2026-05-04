#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 mentioned_users 字段到 community_group_messages 表
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import common_db_engine

def add_mentioned_users_column():
    """添加 mentioned_users 字段"""
    try:
        with common_db_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'community_group_messages' 
                AND COLUMN_NAME = 'mentioned_users'
            """))
            
            if result.scalar():
                print("字段 mentioned_users 已存在，无需添加")
                return
            
            conn.execute(text("""
                ALTER TABLE community_group_messages 
                ADD COLUMN mentioned_users VARCHAR(500) NULL COMMENT '被@的用户ID列表，逗号分隔'
            """))
            conn.commit()
            print("成功添加 mentioned_users 字段")
            
    except Exception as e:
        print(f"添加字段失败: {e}")
        raise

if __name__ == "__main__":
    add_mentioned_users_column()
