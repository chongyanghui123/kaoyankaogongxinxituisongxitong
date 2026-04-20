#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用SQL语句创建用户学习资料收藏表
"""

from core.database import common_db_engine
from sqlalchemy import text

def main():
    try:
        with common_db_engine.connect() as conn:
            sql = '''
            CREATE TABLE IF NOT EXISTS user_material_favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT UNSIGNED NOT NULL,
                material_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (material_id) REFERENCES learning_materials(id)
            )
            '''
            conn.execute(text(sql))
            conn.commit()
            print('Table created successfully')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()