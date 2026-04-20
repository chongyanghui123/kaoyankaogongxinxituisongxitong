#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查表列类型
"""

from core.database import common_db_engine
from sqlalchemy import text

def main():
    try:
        with common_db_engine.connect() as conn:
            # 检查 users 表
            print("=== users 表 ===")
            result = conn.execute(text("DESCRIBE users"))
            for row in result:
                print(row)
            
            # 检查 learning_materials 表
            print("\n=== learning_materials 表 ===")
            result = conn.execute(text("DESCRIBE learning_materials"))
            for row in result:
                print(row)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()