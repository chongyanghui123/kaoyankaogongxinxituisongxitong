#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import common_db_engine
from sqlalchemy import text

with common_db_engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS daily_practices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50) NOT NULL COMMENT '题目分类',
            question TEXT NOT NULL COMMENT '题目内容',
            options TEXT NOT NULL COMMENT '选项JSON',
            answer VARCHAR(10) NOT NULL COMMENT '正确答案',
            analysis TEXT COMMENT '答案解析',
            difficulty INT DEFAULT 1 COMMENT '难度',
            is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
            show_date DATETIME COMMENT '指定显示日期',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日一练题库'
    """))
    conn.commit()
    print("daily_practices 表创建成功!")
    
    result = conn.execute(text("SELECT COUNT(*) FROM daily_practices"))
    count = result.scalar()
    if count == 0:
        conn.execute(text("""
            INSERT INTO daily_practices (category, question, options, answer, analysis, difficulty) VALUES
            ('行测', '某单位采购办公用品，其中A4纸的数量是B5纸的2倍，B5纸比A3纸多50本。若A3纸有100本，则A4纸有多少本？', '[{\"label\":\"A\",\"text\":\"200本\"},{\"label\":\"B\",\"text\":\"250本\"},{\"label\":\"C\",\"text\":\"300本\"},{\"label\":\"D\",\"text\":\"350本\"}]', 'C', 'A3纸有100本，B5纸比A3纸多50本，所以B5纸有150本。A4纸是B5纸的2倍，所以A4纸有300本。', 2)
        """))
        conn.execute(text("""
            INSERT INTO daily_practices (category, question, options, answer, analysis, difficulty) VALUES
            ('考研英语', 'The professor suggested that the students _____ more attention to their writing skills.', '[{\"label\":\"A\",\"text\":\"pay\"},{\"label\":\"B\",\"text\":\"paid\"},{\"label\":\"C\",\"text\":\"would pay\"},{\"label\":\"D\",\"text\":\"paying\"}]', 'A', 'suggest表示建议时，其后的宾语从句用虚拟语气，结构为(should)+动词原形，should可省略。', 2)
        """))
        conn.execute(text("""
            INSERT INTO daily_practices (category, question, options, answer, analysis, difficulty) VALUES
            ('申论', '下列关于公文写作的说法，正确的是：', '[{\"label\":\"A\",\"text\":\"公文标题可以省略发文机关\"},{\"label\":\"B\",\"text\":\"公文正文必须使用宋体\"},{\"label\":\"C\",\"text\":\"所有公文都必须有附件\"},{\"label\":\"D\",\"text\":\"公文落款日期使用汉字数字\"}]', 'A', '公文标题由发文机关、事由、文种三部分组成，其中发文机关和事由可以省略，文种不能省略。', 1)
        """))
        conn.commit()
        print("示例数据插入成功!")
    else:
        print(f"表中已有 {count} 条数据")
