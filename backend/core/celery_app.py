#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - Celery 应用模块
"""

from celery import Celery
from config import settings

# 根据配置选择消息代理和结果存储
broker_url = settings.RABBITMQ_URL if settings.RABBITMQ_URL else 'memory://'
backend_url = settings.REDIS_URL if settings.REDIS_URL else 'cache+memory://'

# 创建 Celery 应用
celery_app = Celery(
    'tasks',
    broker=broker_url,
    backend=backend_url,
    include=['core.tasks']
)

# 配置 Celery
celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Shanghai',
    enable_utc=True,
    # 只有在配置了 RabbitMQ 和 Redis 时才启用定时任务
    beat_schedule={} if not (settings.RABBITMQ_URL and settings.REDIS_URL) else {
        # 每小时检查一次服务到期时间
        'check-service-expiration': {
            'task': 'core.tasks.check_service_expiration',
            'schedule': 3600,  # 3600秒 = 1小时
        },
        # 每小时发送一次推送通知
        'send-push-notifications': {
            'task': 'core.tasks.send_push_notifications',
            'schedule': 3600,  # 3600秒 = 1小时
        },
        # 每天发送一次服务到期通知
        'send-expiry-notifications': {
            'task': 'core.tasks.send_expiry_notifications_task',
            'schedule': 86400,  # 86400秒 = 1天
        },
    },
)
