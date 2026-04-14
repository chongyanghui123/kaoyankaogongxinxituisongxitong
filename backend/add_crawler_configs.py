#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向数据库中添加爬虫配置数据
"""

from core.database import get_db_kaoyan, get_db_kaogong
from models.kaoyan import KaoyanCrawlerConfig
from models.kaogong import KaogongCrawlerConfig
from datetime import datetime

def add_kaoyan_crawler_configs():
    """添加考研爬虫配置"""
    db = next(get_db_kaoyan())
    try:
        # 检查是否已经存在数据
        existing_configs = db.query(KaoyanCrawlerConfig).count()
        if existing_configs > 0:
            print(f"考研爬虫配置已存在 {existing_configs} 条，跳过添加")
            return
        
        # 添加考研爬虫配置
        kaoyan_configs = [
            {
                'name': '中国研究生招生信息网',
                'url': 'https://yz.chsi.com.cn/',
                'selector': '.news-list',
                'parse_rules': {"title": ".title", "link": ".link", "date": ".date"},
                'interval': 60,
                'status': 1,
                'priority': 1,
                'user_id': 43
            },
            {
                'name': '考研论坛',
                'url': 'https://bbs.kaoyan.com/',
                'selector': '.forum-list',
                'parse_rules': {"title": ".thread-title", "link": ".thread-link", "date": ".thread-date"},
                'interval': 120,
                'status': 1,
                'priority': 0,
                'user_id': 43
            },
            {
                'name': '考研网',
                'url': 'https://www.kaoyan.com/',
                'selector': '.news-content',
                'parse_rules': {"title": ".news-title", "link": ".news-link", "date": ".news-date"},
                'interval': 90,
                'status': 1,
                'priority': 0,
                'user_id': 43
            }
        ]
        
        for config_data in kaoyan_configs:
            config = KaoyanCrawlerConfig(**config_data)
            db.add(config)
        
        db.commit()
        print(f"成功添加 {len(kaoyan_configs)} 条考研爬虫配置")
    except Exception as e:
        print(f"添加考研爬虫配置失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

def add_kaogong_crawler_configs():
    """添加考公爬虫配置"""
    db = next(get_db_kaogong())
    try:
        # 检查是否已经存在数据
        existing_configs = db.query(KaogongCrawlerConfig).count()
        if existing_configs > 0:
            print(f"考公爬虫配置已存在 {existing_configs} 条，跳过添加")
            return
        
        # 添加考公爬虫配置
        kaogong_configs = [
            {
                'name': '国家公务员局',
                'url': 'http://www.scs.gov.cn/',
                'selector': '.news-section',
                'parse_rules': {"title": ".news-title", "link": ".news-link", "date": ".news-date"},
                'interval': 60,
                'status': 1,
                'priority': 1,
                'user_id': 43
            },
            {
                'name': '公务员考试网',
                'url': 'https://www.gwy.com/',
                'selector': '.exam-news',
                'parse_rules': {"title": ".news-title", "link": ".news-link", "date": ".news-date"},
                'interval': 120,
                'status': 1,
                'priority': 0,
                'user_id': 43
            },
            {
                'name': '中公教育',
                'url': 'https://www.offcn.com/',
                'selector': '.gwy-news',
                'parse_rules': {"title": ".news-title", "link": ".news-link", "date": ".news-date"},
                'interval': 90,
                'status': 1,
                'priority': 0,
                'user_id': 43
            }
        ]
        
        for config_data in kaogong_configs:
            config = KaogongCrawlerConfig(**config_data)
            db.add(config)
        
        db.commit()
        print(f"成功添加 {len(kaogong_configs)} 条考公爬虫配置")
    except Exception as e:
        print(f"添加考公爬虫配置失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始添加爬虫配置数据...")
    add_kaoyan_crawler_configs()
    add_kaogong_crawler_configs()
    print("爬虫配置数据添加完成!")
