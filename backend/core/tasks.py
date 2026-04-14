#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - Celery 任务模块
"""

from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def crawl_kaoyan_info():
    """爬取考研情报"""
    try:
        from core.crawler_manager import run_kaoyan_crawler
        run_kaoyan_crawler()
        logger.info("考研情报爬取任务执行完成")
    except Exception as e:
        logger.error(f"考研情报爬取任务执行失败: {str(e)}")

@shared_task
def crawl_kaogong_info():
    """爬取考公情报"""
    try:
        from core.crawler_manager import run_kaogong_crawler
        run_kaogong_crawler()
        logger.info("考公情报爬取任务执行完成")
    except Exception as e:
        logger.error(f"考公情报爬取任务执行失败: {str(e)}")

@shared_task
def send_push_notifications():
    """发送推送通知"""
    try:
        from core.push_manager import send_pending_notifications
        send_pending_notifications()
        logger.info("推送通知任务执行完成")
    except Exception as e:
        logger.error(f"推送通知任务执行失败: {str(e)}")
