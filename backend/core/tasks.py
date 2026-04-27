#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - Celery 任务模块
"""

from celery import shared_task
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task
def send_push_notifications():
    """发送推送通知"""
    try:
        from core.push_manager import send_pending_notifications
        send_pending_notifications()
        logger.info("推送通知任务执行完成")
    except Exception as e:
        logger.error(f"推送通知任务执行失败: {str(e)}")

@shared_task
def check_service_expiration():
    """检查服务到期时间"""
    try:
        from core.database import get_db_common
        from models.users import User
        
        db = next(get_db_common())
        try:
            # 获取所有VIP用户
            vip_users = db.query(User).filter(User.is_vip == True).all()
            
            expired_count = 0
            for user in vip_users:
                # 检查服务是否到期
                if user.vip_end_time and datetime.now() > user.vip_end_time:
                    user.is_vip = False
                    expired_count += 1
                    logger.info(f"用户 {user.username} (ID: {user.id}) 服务已到期，已更新状态")
            
            if expired_count > 0:
                db.commit()
                logger.info(f"共处理 {expired_count} 个服务到期的用户")
            else:
                logger.info("没有服务到期的用户")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"检查服务到期时间任务执行失败: {str(e)}")

@shared_task
def send_expiry_notifications_task():
    """给快到期的用户推送服务到期消息"""
    try:
        from core.push_manager import send_expiry_notifications
        send_expiry_notifications()
        logger.info("服务到期通知任务执行完成")
    except Exception as e:
        logger.error(f"服务到期通知任务执行失败: {str(e)}")
