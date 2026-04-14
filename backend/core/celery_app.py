#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - Celery 应用模块
"""

from celery import Celery
from config import settings

# 创建 Celery 应用
celery_app = Celery(
    'tasks',
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
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
)
