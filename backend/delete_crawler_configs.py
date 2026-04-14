#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除数据库中的爬虫配置测试数据
"""

from core.database import get_db_kaoyan, get_db_kaogong
from models.kaoyan import KaoyanCrawlerConfig
from models.kaogong import KaogongCrawlerConfig

def delete_kaoyan_crawler_configs():
    """删除考研爬虫配置"""
    db = next(get_db_kaoyan())
    try:
        # 删除所有考研爬虫配置
        deleted_count = db.query(KaoyanCrawlerConfig).delete()
        db.commit()
        print(f"成功删除 {deleted_count} 条考研爬虫配置")
    except Exception as e:
        print(f"删除考研爬虫配置失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

def delete_kaogong_crawler_configs():
    """删除考公爬虫配置"""
    db = next(get_db_kaogong())
    try:
        # 删除所有考公爬虫配置
        deleted_count = db.query(KaogongCrawlerConfig).delete()
        db.commit()
        print(f"成功删除 {deleted_count} 条考公爬虫配置")
    except Exception as e:
        print(f"删除考公爬虫配置失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始删除爬虫配置测试数据...")
    delete_kaoyan_crawler_configs()
    delete_kaogong_crawler_configs()
    print("爬虫配置测试数据删除完成!")
