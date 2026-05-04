#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:123456789@localhost:3306/common_db?charset=utf8mb4"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # 先清空现有数据
    conn.execute(text('DELETE FROM exam_schedules'))
    
    # 添加新的考试日程数据（未来日期）
    schedules = [
        ('2026年教师资格证考试', 2, '2026-09-15', '全国中小学教师资格考试'),
        ('2026年国家公务员考试', 2, '2026-11-28', '国考公共科目笔试'),
        ('2026年考研初试', 1, '2026-12-20', '全国硕士研究生招生考试'),
        ('2027年省公务员考试', 2, '2027-03-15', '各省公务员考试')
    ]
    
    for name, exam_type, exam_date, desc in schedules:
        conn.execute(text('''
            INSERT INTO exam_schedules (name, exam_type, exam_date, description, is_active, created_at)
            VALUES (:name, :type, :date, :desc, TRUE, NOW())
        '''), {'name': name, 'type': exam_type, 'date': exam_date, 'desc': desc})
    
    conn.commit()
    print('已添加考试日程数据')