#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import common_db_engine, kaoyan_db_engine, kaogong_db_engine
from sqlalchemy import text

def check_data():
    print("=== 检查各表数据情况 ===")
    
    with common_db_engine.connect() as conn:
        print("\n--- common_db ---")
        
        # daily_practices
        result = conn.execute(text("SELECT COUNT(*) FROM daily_practices"))
        print(f"daily_practices: {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM daily_practices WHERE is_active = 1"))
        print(f"daily_practices (active): {result.scalar()} 条")
        
        # carousels
        result = conn.execute(text("SELECT COUNT(*) FROM carousels"))
        print(f"carousels: {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM carousels WHERE is_active = 1"))
        print(f"carousels (active): {result.scalar()} 条")
        
        # exam_schedules
        result = conn.execute(text("SELECT COUNT(*) FROM exam_schedules"))
        print(f"exam_schedules: {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM exam_schedules WHERE is_active = 1"))
        print(f"exam_schedules (active): {result.scalar()} 条")
        
        # gifts
        result = conn.execute(text("SELECT COUNT(*) FROM gifts"))
        print(f"gifts: {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM gifts WHERE is_active = 1"))
        print(f"gifts (active): {result.scalar()} 条")
        
        # products
        result = conn.execute(text("SELECT COUNT(*) FROM products"))
        print(f"products: {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM products WHERE status = 1"))
        print(f"products (active): {result.scalar()} 条")
        
        # material_categories
        result = conn.execute(text("SELECT COUNT(*) FROM material_categories"))
        print(f"material_categories: {result.scalar()} 条")
        
        # learning_materials
        result = conn.execute(text("SELECT COUNT(*) FROM learning_materials"))
        print(f"learning_materials: {result.scalar()} 条")

    with kaoyan_db_engine.connect() as conn:
        print("\n--- kaoyan_db ---")
        result = conn.execute(text("SELECT COUNT(*) FROM kaoyan_info"))
        print(f"kaoyan_info: {result.scalar()} 条")

    with kaogong_db_engine.connect() as conn:
        print("\n--- kaogong_db ---")
        result = conn.execute(text("SELECT COUNT(*) FROM kaogong_info"))
        print(f"kaogong_info: {result.scalar()} 条")

if __name__ == "__main__":
    check_data()
