#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 日志模块
"""

import os
import logging
import logging.handlers
from datetime import datetime

from config import settings

def setup_logging():
    """设置日志配置"""
    # 创建日志目录
    log_dir = os.path.dirname(settings.LOG_FILE_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # 移除现有的处理器（防止重复）
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 创建文件处理器（带轮转）
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE_PATH,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # 配置SQLAlchemy日志
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
    
    # 配置FastAPI日志
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    
    # 配置第三方库日志
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger.info(f"日志系统初始化完成，日志文件路径: {settings.LOG_FILE_PATH}")

def get_logger(name: str = __name__) -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)

def log_info(msg: str, extra: dict = None):
    """记录信息级别日志"""
    logger = get_logger()
    if extra:
        logger.info(msg, extra=extra)
    else:
        logger.info(msg)

def log_warning(msg: str, extra: dict = None):
    """记录警告级别日志"""
    logger = get_logger()
    if extra:
        logger.warning(msg, extra=extra)
    else:
        logger.warning(msg)

def log_error(msg: str, extra: dict = None):
    """记录错误级别日志"""
    logger = get_logger()
    if extra:
        logger.error(msg, extra=extra)
    else:
        logger.error(msg)

def log_debug(msg: str, extra: dict = None):
    """记录调试级别日志"""
    logger = get_logger()
    if extra:
        logger.debug(msg, extra=extra)
    else:
        logger.debug(msg)

def log_critical(msg: str, extra: dict = None):
    """记录严重级别日志"""
    logger = get_logger()
    if extra:
        logger.critical(msg, extra=extra)
    else:
        logger.critical(msg)

def log_exception(msg: str, extra: dict = None):
    """记录异常信息"""
    logger = get_logger()
    if extra:
        logger.exception(msg, extra=extra)
    else:
        logger.exception(msg)

def log_request(request, response, duration):
    """记录API请求日志"""
    logger = get_logger('api_requests')
    
    log_data = {
        'method': request.method,
        'url': str(request.url),
        'status_code': response.status_code,
        'duration': f"{duration:.2f}ms",
        'remote_addr': request.client.host,
        'user_agent': request.headers.get('user-agent', ''),
        'content_type': request.headers.get('content-type', ''),
        'content_length': request.headers.get('content-length', 0)
    }
    
    if response.status_code >= 500:
        logger.error(f"API请求失败: {log_data['method']} {log_data['url']} - {log_data['status_code']}", extra=log_data)
    elif response.status_code >= 400:
        logger.warning(f"API请求警告: {log_data['method']} {log_data['url']} - {log_data['status_code']}", extra=log_data)
    else:
        logger.info(f"API请求成功: {log_data['method']} {log_data['url']} - {log_data['status_code']}", extra=log_data)

def log_user_action(user_id, action, details=None):
    """记录用户操作日志"""
    logger = get_logger('user_actions')
    
    log_data = {
        'user_id': user_id,
        'action': action,
        'details': details
    }
    
    logger.info(f"用户操作: 用户ID={user_id}, 操作={action}", extra=log_data)

def log_crawler_activity(crawler_name, url, status, info_count=0, error_msg=None):
    """记录爬虫活动日志"""
    logger = get_logger('crawlers')
    
    log_data = {
        'crawler_name': crawler_name,
        'url': url,
        'status': status,
        'info_count': info_count,
        'error_msg': error_msg
    }
    
    if status == 'success':
        logger.info(f"爬虫成功: {crawler_name} - {info_count}条信息", extra=log_data)
    else:
        logger.error(f"爬虫失败: {crawler_name} - {error_msg}", extra=log_data)

def log_push_activity(user_id, push_type, status, content=None, error_msg=None):
    """记录推送活动日志"""
    logger = get_logger('push')
    
    log_data = {
        'user_id': user_id,
        'push_type': push_type,
        'status': status,
        'content': content,
        'error_msg': error_msg
    }
    
    if status == 'success':
        logger.info(f"推送成功: 用户ID={user_id}, 类型={push_type}", extra=log_data)
    else:
        logger.error(f"推送失败: 用户ID={user_id}, 类型={push_type} - {error_msg}", extra=log_data)

def log_payment_activity(order_no, user_id, amount, status, payment_method=None):
    """记录支付活动日志"""
    logger = get_logger('payments')
    
    log_data = {
        'order_no': order_no,
        'user_id': user_id,
        'amount': amount,
        'status': status,
        'payment_method': payment_method
    }
    
    logger.info(f"支付活动: 订单号={order_no}, 用户ID={user_id}, 金额={amount}, 状态={status}", extra=log_data)

def log_system_event(event_type, event_data=None):
    """记录系统事件日志"""
    logger = get_logger('system_events')
    
    log_data = {
        'event_type': event_type,
        'event_data': event_data
    }
    
    logger.info(f"系统事件: {event_type}", extra=log_data)

# 初始化日志系统
if __name__ == "__main__":
    setup_logging()
    logger = get_logger()
    logger.info("日志系统测试")
    logger.warning("警告测试")
    logger.error("错误测试")
    logger.debug("调试测试")