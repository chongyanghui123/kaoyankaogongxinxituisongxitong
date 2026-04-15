#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 推送管理模块
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime, timedelta

from core.database import get_db_common
from models.users import PushLog, User, UserSubscription, UserKeyword, Order
from models.kaoyan import KaoyanInfo
from models.kaogong import KaogongInfo

# 邮箱配置
EMAIL_SENDER = "1322835898@qq.com"  # 发送者QQ邮箱
EMAIL_PASSWORD = "jmqyjcmkrrnnifaa"  # QQ邮箱授权码
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587

logger = logging.getLogger(__name__)

def send_email(to_email, subject, content):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加邮件正文
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 连接SMTP服务器
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # 发送邮件
        server.send_message(msg)
        server.quit()
        
        logger.info(f"邮件发送成功: {to_email}")
        return True
    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")
        return False

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
                if subscription.subscribe_type == 1:  # 考研
                    send_kaoyan_notifications(db, user, subscription)
                elif subscription.subscribe_type == 2:  # 考公
                    send_kaogong_notifications(db, user, subscription)
                elif subscription.subscribe_type == 3:  # 双赛道
                    send_kaoyan_notifications(db, user, subscription)
                    send_kaogong_notifications(db, user, subscription)
            
        finally:
            db.close()
        
        logger.info("推送通知发送完成")
    except Exception as e:
        logger.error(f"发送推送通知失败: {str(e)}")

def send_payment_users_notifications():
    """给已经支付订单的用户推送消息"""
    try:
        logger.info("开始给已支付订单的用户发送推送通知")
        
        db = next(get_db_common())
        try:
            # 获取已经支付订单的用户
            paid_users = db.query(User).join(Order).filter(
                User.is_active == True,
                Order.payment_status == 1  # 已支付
            ).distinct().all()
            
            logger.info(f"找到 {len(paid_users)} 个已支付订单的用户")
            
            for user in paid_users:
                # 检查用户的订阅类型
                subscription = db.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
                if not subscription:
                    continue
                
                # 根据订阅类型发送不同的推送
                if subscription.subscribe_type == 1:  # 考研
                    send_kaoyan_notifications(db, user, subscription)
                elif subscription.subscribe_type == 2:  # 考公
                    send_kaogong_notifications(db, user, subscription)
                elif subscription.subscribe_type == 3:  # 双赛道
                    send_kaoyan_notifications(db, user, subscription)
                    send_kaogong_notifications(db, user, subscription)
            
        finally:
            db.close()
        
        logger.info("给已支付订单的用户发送推送通知完成")
    except Exception as e:
        logger.error(f"给已支付订单的用户发送推送通知失败: {str(e)}")

def send_kaoyan_notifications(db, user, subscription):
    """发送考研通知"""
    try:
        # 获取用户的关键词
        keywords = [kw.keyword for kw in db.query(UserKeyword).filter(
            UserKeyword.user_id == user.id,
            UserKeyword.category == 1,
            UserKeyword.is_active == True
        ).all()]
        
        # 从订阅配置中获取用户关注的省份、学校、专业
        config_json = subscription.config_json or {}
        provinces = config_json.get('provinces', [])
        schools = config_json.get('schools', [])
        majors = config_json.get('majors', [])
        
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
                PushLog.info_id == info.id,
                PushLog.category == 1
            ).first()
            
            if not existing_log:
                # 创建推送日志
                push_log = PushLog(
                    user_id=user.id,
                    info_id=info.id,
                    category=1,  # 考研
                    push_type=1,  # 微信模板消息
                    push_status=1,  # 成功
                    push_content=f"【考研情报】{info.title}\n{info.source}\n{info.publish_time.strftime('%Y-%m-%d %H:%M')}",
                    push_time=datetime.now()
                )
                db.add(push_log)
                
                # 发送邮件通知
                if user.email:
                    email_subject = f"【考研情报】{info.title}"
                    email_content = f"尊敬的 {user.username}：\n\n{info.title}\n\n{info.content or ''}\n\n来源：{info.source}\n发布时间：{info.publish_time.strftime('%Y-%m-%d %H:%M')}\n\n此致\n双赛道情报通团队"
                    send_email(user.email, email_subject, email_content)
                
                # 这里可以添加其他推送逻辑，比如发送短信等
                logger.info(f"向用户 {user.username} 发送考研推送: {info.title}")
        
        db.commit()
    except Exception as e:
        logger.error(f"发送考研通知失败: {str(e)}")
        db.rollback()

def send_kaogong_notifications(db, user, subscription):
    """发送考公通知"""
    try:
        # 获取用户的关键词
        keywords = [kw.keyword for kw in db.query(UserKeyword).filter(
            UserKeyword.user_id == user.id,
            UserKeyword.category == 2,
            UserKeyword.is_active == True
        ).all()]
        
        # 从订阅配置中获取用户关注的省份、岗位类别、专业
        config_json = subscription.config_json or {}
        provinces = config_json.get('provinces', [])
        position_types = config_json.get('position_types', [])
        majors = config_json.get('majors', [])
        
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
                PushLog.info_id == info.id,
                PushLog.category == 2
            ).first()
            
            if not existing_log:
                # 创建推送日志
                push_log = PushLog(
                    user_id=user.id,
                    info_id=info.id,
                    category=2,  # 考公
                    push_type=1,  # 微信模板消息
                    push_status=1,  # 成功
                    push_content=f"【考公情报】{info.title}\n{info.source}\n{info.publish_time.strftime('%Y-%m-%d %H:%M')}",
                    push_time=datetime.now()
                )
                db.add(push_log)
                
                # 发送邮件通知
                if user.email:
                    email_subject = f"【考公情报】{info.title}"
                    email_content = f"尊敬的 {user.username}：\n\n{info.title}\n\n{info.content or ''}\n\n来源：{info.source}\n发布时间：{info.publish_time.strftime('%Y-%m-%d %H:%M')}\n\n此致\n双赛道情报通团队"
                    send_email(user.email, email_subject, email_content)
                
                # 这里可以添加其他推送逻辑，比如发送短信等
                logger.info(f"向用户 {user.username} 发送考公推送: {info.title}")
        
        db.commit()
    except Exception as e:
        logger.error(f"发送考公通知失败: {str(e)}")
        db.rollback()

def send_expiry_notifications():
    """给快到期的用户推送服务到期消息"""
    try:
        logger.info("开始给快到期的用户发送服务到期通知")
        
        db = next(get_db_common())
        try:
            # 获取3天后到期的用户
            three_days_later = datetime.now() + timedelta(days=3)
            users_to_notify = db.query(User).filter(
                User.is_vip == True,
                User.vip_end_time <= three_days_later,
                User.vip_end_time > datetime.now()
            ).all()
            
            logger.info(f"找到 {len(users_to_notify)} 个快到期的用户")
            
            for user in users_to_notify:
                # 检查是否已经发送过到期通知
                existing_log = db.query(PushLog).filter(
                    PushLog.user_id == user.id,
                    PushLog.category == 3,  # 3-服务到期通知
                    PushLog.push_time >= datetime.now() - timedelta(days=7)  # 7天内只发送一次
                ).first()
                
                if not existing_log:
                    # 获取用户的订阅类型
                    subscription = db.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
                    if subscription:
                        if subscription.subscribe_type == 1:
                            service_type = "考研"
                        elif subscription.subscribe_type == 2:
                            service_type = "考公"
                        elif subscription.subscribe_type == 3:
                            service_type = "考研考公"
                        else:
                            service_type = "推送"
                    else:
                        service_type = "推送"
                    
                    # 计算剩余天数
                    remaining_days = (user.vip_end_time - datetime.now()).days
                    
                    # 创建推送日志
                    push_log = PushLog(
                        user_id=user.id,
                        info_id=0,  # 服务到期通知，没有具体的信息ID
                        category=3,  # 3-服务到期通知
                        push_type=1,  # 微信模板消息
                        push_status=1,  # 成功
                        push_content=f"【服务到期提醒】尊敬的 {user.username}，您的{service_type}推送服务将在 {remaining_days} 天后到期，请及时续费以继续享受服务。",
                        push_time=datetime.now()
                    )
                    db.add(push_log)
                    
                    # 发送邮件通知
                    if user.email:
                        email_subject = f"【服务到期提醒】您的{service_type}推送服务即将到期"
                        email_content = f"尊敬的 {user.username}：\n\n您的{service_type}推送服务将在 {remaining_days} 天后到期，请及时续费以继续享受服务。\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                        send_email(user.email, email_subject, email_content)
                    
                    # 这里可以添加其他推送逻辑，比如发送短信等
                    logger.info(f"向用户 {user.username} 发送{service_type}推送服务到期提醒，剩余 {remaining_days} 天")
            
            db.commit()
        finally:
            db.close()
        
        logger.info("给快到期的用户发送服务到期通知完成")
    except Exception as e:
        logger.error(f"给快到期的用户发送服务到期通知失败: {str(e)}")

def start_push_scheduler():
    """启动推送调度器"""
    try:
        logger.info("推送调度器已禁用")
    except Exception as e:
        logger.error(f"推送调度器启动失败: {str(e)}")
