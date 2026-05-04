#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复数据库数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import common_db_engine
from sqlalchemy import text

def fix_data():
    print("=== 修复数据库数据 ===")
    
    with common_db_engine.connect() as conn:
        # 修复 daily_practices 的 is_active 字段
        print("\n1. 修复 daily_practices 的 is_active 字段...")
        result = conn.execute(text("UPDATE daily_practices SET is_active = TRUE WHERE is_active IS NULL"))
        conn.commit()
        print(f"   更新了 {result.rowcount} 条记录")
        
        # 修复 exam_schedules 的 is_active 字段
        print("\n2. 修复 exam_schedules 的 is_active 字段...")
        result = conn.execute(text("UPDATE exam_schedules SET is_active = TRUE WHERE is_active IS NULL"))
        conn.commit()
        print(f"   更新了 {result.rowcount} 条记录")
        
        # 修复 gifts 的 is_active 字段
        print("\n3. 修复 gifts 的 is_active 字段...")
        result = conn.execute(text("UPDATE gifts SET is_active = TRUE WHERE is_active IS NULL"))
        conn.commit()
        print(f"   更新了 {result.rowcount} 条记录")
        
        # 验证修复结果
        print("\n=== 验证修复结果 ===")
        
        result = conn.execute(text("SELECT COUNT(*) FROM daily_practices WHERE is_active = 1"))
        print(f"daily_practices (active): {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM exam_schedules WHERE is_active = 1"))
        print(f"exam_schedules (active): {result.scalar()} 条")
        
        result = conn.execute(text("SELECT COUNT(*) FROM gifts WHERE is_active = 1"))
        print(f"gifts (active): {result.scalar()} 条")
        
    print("\n修复完成！")

if __name__ == "__main__":
    fix_data()
