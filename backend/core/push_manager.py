#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 推送管理模块
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

from core.database import get_db_common
from models.users import PushLog, User, UserSubscription
from models.kaoyan import KaoyanInfo
from models.kaogong import KaogongInfo

logger = logging.getLogger(__name__)

def send_pending_notifications():
    """发送待处理的推送通知"""
    try:
        # 这里实现推送通知的逻辑
        # 1. 从数据库获取待发送的通知
        # 2. 调用推送服务发送通知
        # 3. 更新通知状态
        logger.info("开始发送推送通知")
        
        # 获取待发送的通知
        db = next(get_db_common())
        try:
            # 获取所有活跃用户
            active_users = db.query(User).filter(User.is_active == True).all()
            
            for user in active_users:
                # 检查用户的订阅类型
                subscription = db.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
                if not subscription:
                    continue
                
                # 根据订阅类型发送不同的推送
                if subscription.subscription_type == 1:  # 考研
                    send_kaoyan_notifications(db, user, subscription)
                elif subscription.subscription_type == 2:  # 考公
                    send_kaogong_notifications(db, user, subscription)
                elif subscription.subscription_type == 3:  # 双赛道
                    send_kaoyan_notifications(db, user, subscription)
                    send_kaogong_notifications(db, user, subscription)
            
        finally:
            db.close()
        
        logger.info("推送通知发送完成")
    except Exception as e:
        logger.error(f"发送推送通知失败: {str(e)}")

def send_kaoyan_notifications(db, user, subscription):
    """发送考研通知"""
    try:
        # 获取用户的关键词
        keywords = [kw.keyword for kw in user.keywords if kw.category == 1] if hasattr(user, 'keywords') else []
        
        # 获取用户关注的省份、学校、专业
        provinces = subscription.provinces.split(',') if subscription.provinces else []
        schools = subscription.schools.split(',') if subscription.schools else []
        majors = subscription.majors.split(',') if subscription.majors else []
        
        # 获取最近24小时的考研信息
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_info = db.query(KaoyanInfo).filter(
            KaoyanInfo.publish_time >= cutoff_time,
            KaoyanInfo.is_valid == True
        ).all()
        
        # 筛选符合用户需求的信息
        relevant_info = []
        for info in recent_info:
            # 检查省份
            if provinces and info.province and info.province not in provinces:
                continue
            # 检查学校
            if schools and info.school and info.school not in schools:
                continue
            # 检查专业
            if majors and info.major and info.major not in majors:
                continue
            # 检查关键词
            if keywords:
                info_text = f"{info.title} {info.content or ''}"
                if not any(keyword in info_text for keyword in keywords):
                    continue
            relevant_info.append(info)
        
        # 发送推送
        for info in relevant_info:
            # 检查是否已经发送过
            existing_log = db.query(PushLog).filter(
                PushLog.user_id == user.id,
                PushLog.content.contains(info.title)
            ).first()
            
            if not existing_log:
                # 创建推送日志
                push_log = PushLog(
                    template_id=1,  # 默认模板
                    user_id=user.id,
                    content=f"【考研情报】{info.title}\n{info.source}\n{info.publish_time.strftime('%Y-%m-%d %H:%M')}",
                    status="sent",
                    created_at=datetime.utcnow()
                )
                db.add(push_log)
                
                # 这里可以添加实际的推送逻辑，比如发送邮件、短信等
                logger.info(f"向用户 {user.username} 发送考研推送: {info.title}")
        
        db.commit()
    except Exception as e:
        logger.error(f"发送考研通知失败: {str(e)}")
        db.rollback()

def send_kaogong_notifications(db, user, subscription):
    """发送考公通知"""
    try:
        # 获取用户的关键词
        keywords = [kw.keyword for kw in user.keywords if kw.category == 2] if hasattr(user, 'keywords') else []
        
        # 获取用户关注的省份、岗位类别、专业
        provinces = subscription.provinces.split(',') if subscription.provinces else []
        position_types = subscription.position_types.split(',') if subscription.position_types else []
        majors = subscription.majors.split(',') if subscription.majors else []
        
        # 获取最近24小时的考公信息
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_info = db.query(KaogongInfo).filter(
            KaogongInfo.publish_time >= cutoff_time,
            KaogongInfo.is_valid == True
        ).all()
        
        # 筛选符合用户需求的信息
        relevant_info = []
        for info in recent_info:
            # 检查省份
            if provinces and info.province and info.province not in provinces:
                continue
            # 检查岗位类别
            if position_types and info.position_type and info.position_type not in position_types:
                continue
            # 检查专业
            if majors and info.major and info.major not in majors:
                continue
            # 检查关键词
            if keywords:
                info_text = f"{info.title} {info.content or ''}"
                if not any(keyword in info_text for keyword in keywords):
                    continue
            relevant_info.append(info)
        
        # 发送推送
        for info in relevant_info:
            # 检查是否已经发送过
            existing_log = db.query(PushLog).filter(
                PushLog.user_id == user.id,
                PushLog.content.contains(info.title)
            ).first()
            
            if not existing_log:
                # 创建推送日志
                push_log = PushLog(
                    template_id=2,  # 默认模板
                    user_id=user.id,
                    content=f"【考公情报】{info.title}\n{info.source}\n{info.publish_time.strftime('%Y-%m-%d %H:%M')}",
                    status="sent",
                    created_at=datetime.utcnow()
                )
                db.add(push_log)
                
                # 这里可以添加实际的推送逻辑，比如发送邮件、短信等
                logger.info(f"向用户 {user.username} 发送考公推送: {info.title}")
        
        db.commit()
    except Exception as e:
        logger.error(f"发送考公通知失败: {str(e)}")
        db.rollback()

def start_push_scheduler():
    """启动推送调度器"""
    try:
        from core.scheduler import scheduler
        from core.tasks import send_push_notifications
        
        # 每5分钟发送一次推送通知
        scheduler.add_job(
            send_push_notifications,
            'interval',
            minutes=5,
            id='send_push_notifications',
            replace_existing=True
        )
        logger.info("推送调度器启动成功")
    except Exception as e:
        logger.error(f"推送调度器启动失败: {str(e)}")
