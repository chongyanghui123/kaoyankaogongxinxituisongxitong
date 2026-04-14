#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 调度器模块
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# 创建调度器实例
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = BackgroundScheduler(
    executors=executors,
    job_defaults=job_defaults,
    timezone='Asia/Shanghai'
)

# 添加爬虫调度任务
def add_crawler_scheduler_job():
    """添加爬虫调度任务"""
    try:
        from core.crawler_manager import start_crawler_scheduler
        import asyncio
        
        def run_crawler_scheduler():
            """运行爬虫调度器"""
            asyncio.run(start_crawler_scheduler())
        
        # 每10分钟运行一次爬虫调度器
        scheduler.add_job(
            run_crawler_scheduler,
            'interval',
            minutes=10,
            id='crawler_scheduler',
            name='爬虫调度任务',
            replace_existing=True
        )
        
        print("✅ 爬虫调度任务添加成功，每10分钟运行一次")
    except Exception as e:
        print(f"❌ 添加爬虫调度任务失败: {e}")

# 初始化时添加爬虫调度任务
if __name__ == "__main__":
    add_crawler_scheduler_job()
