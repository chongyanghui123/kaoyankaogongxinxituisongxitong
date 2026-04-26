#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 配置模块
"""

import os
from pydantic_settings import BaseSettings
from pydantic import validator
from pydantic.networks import EmailStr
from typing import List, Optional, Dict, Any

class Settings(BaseSettings):
    """应用配置类"""
    
    # 基本配置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE-ME-IN-PRODUCTION-USE-STRONG-KEY")
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "https://servicewechat.com")
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [i.strip() for i in self.CORS_ORIGINS.split(',')]
    
    # 数据库配置
    DATABASE_USER: str = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 3306))
    COMMON_DB: str = "common_db"
    KAOYAN_DB: str = "kaoyan_db"
    KAOGONG_DB: str = "kaogong_db"
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # RabbitMQ配置（Celery）
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "")
    
    # 邮箱配置
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.qq.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "your-email@qq.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your-smtp-password")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "your-email@qq.com")
    
    # 微信配置
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "")
    WECHAT_TOKEN: str = os.getenv("WECHAT_TOKEN", "")
    WECHAT_AES_KEY: str = os.getenv("WECHAT_AES_KEY", "")
    
    # 支付宝配置
    ALIPAY_APP_ID: str = os.getenv("ALIPAY_APP_ID", "")
    ALIPAY_PRIVATE_KEY: str = os.getenv("ALIPAY_PRIVATE_KEY", "")
    ALIPAY_PUBLIC_KEY: str = os.getenv("ALIPAY_PUBLIC_KEY", "")
    ALIPAY_GATEWAY: str = os.getenv("ALIPAY_GATEWAY", "https://openapi.alipay.com/gateway.do")
    
    # 微信支付配置
    WXPAY_APP_ID: str = os.getenv("WXPAY_APP_ID", "")
    WXPAY_MCH_ID: str = os.getenv("WXPAY_MCH_ID", "")
    WXPAY_API_KEY: str = os.getenv("WXPAY_API_KEY", "")
    WXPAY_NOTIFY_URL: str = os.getenv("WXPAY_NOTIFY_URL", "")
    
    # 爬虫配置
    CRAWLER_INTERVAL: int = int(os.getenv("CRAWLER_INTERVAL", 10))  # 默认10分钟
    MAX_CONCURRENT_CRAWLERS: int = int(os.getenv("MAX_CONCURRENT_CRAWLERS", 5))
    CRAWLER_TIMEOUT: int = int(os.getenv("CRAWLER_TIMEOUT", 30))
    CRAWLER_USER_AGENT: str = os.getenv("CRAWLER_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # 推送配置
    PUSH_ENABLED: bool = os.getenv("PUSH_ENABLED", "True").lower() == "true"
    PUSH_INTERVAL: int = int(os.getenv("PUSH_INTERVAL", 5))  # 默认5分钟
    
    # 会员配置
    TRIAL_DAYS: int = int(os.getenv("TRIAL_DAYS", 3))
    VIP_PRICES: Dict[int, float] = {
        1: 39.00,    # 考研VIP月卡
        2: 99.00,    # 考研VIP季卡
        3: 299.00,   # 考研VIP年卡
        4: 49.00,    # 考公VIP月卡
        5: 119.00,   # 考公VIP季卡
        6: 359.00,   # 考公VIP年卡
        7: 499.00    # 双赛道VIP年卡
    }
    
    # 文件上传配置
    UPLOAD_PATH: str = os.getenv("UPLOAD_PATH", "static/uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS: str = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx")
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        return [i.strip() for i in self.ALLOWED_EXTENSIONS.split(',')]
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "logs/app.log")
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", 100 * 1024 * 1024))  # 100MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", 10))
    
    # 安全性配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))  # 7天
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 30))  # 30天
    
    # API限制配置
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "100/minute")
    
    # 数据库配置扩展
    DATABASE_NAME_PREFIX: str = os.getenv("DATABASE_NAME_PREFIX", "")
    
    # 缓存配置
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "1800"))
    
    # 爬虫配置扩展
    CRAWLER_RETRY_TIMES: int = int(os.getenv("CRAWLER_RETRY_TIMES", "3"))
    
    # 阿里云OSS配置
    OSS_ENABLED: bool = os.getenv("OSS_ENABLED", "false").lower() == "true"
    OSS_ACCESS_KEY_ID: str = os.getenv("OSS_ACCESS_KEY_ID", "")
    OSS_ACCESS_KEY_SECRET: str = os.getenv("OSS_ACCESS_KEY_SECRET", "")
    OSS_BUCKET_NAME: str = os.getenv("OSS_BUCKET_NAME", "")
    OSS_ENDPOINT: str = os.getenv("OSS_ENDPOINT", "")
    OSS_REGION: str = os.getenv("OSS_REGION", "")
    

    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# 实例化配置
settings = Settings()