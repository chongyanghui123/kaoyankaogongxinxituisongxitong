#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 用户模型
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float, Text, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from core.database import BaseCommon

class User(BaseCommon):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, nullable=False, comment="手机号")
    password = Column(String(255), nullable=True, comment="密码（仅管理员用户需要）")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    id_card = Column(String(20), nullable=True, comment="身份证号")
    gender = Column(Integer, default=0, comment="性别: 0-未知, 1-男, 2-女")
    birthdate = Column(DateTime, nullable=True, comment="出生日期")
    register_ip = Column(String(45), nullable=True, comment="注册IP")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    is_active = Column(Boolean, default=True, comment="是否激活: 1-激活, 0-未激活")
    is_admin = Column(Boolean, default=False, comment="是否管理员: 1-是, 0-否")
    is_vip = Column(Boolean, default=False, comment="是否VIP: 1-是, 0-否")
    vip_start_time = Column(DateTime, nullable=True, comment="VIP开始时间")
    vip_end_time = Column(DateTime, nullable=True, comment="VIP结束时间")
    vip_type = Column(Integer, default=0, comment="VIP类型: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP")
    trial_status = Column(Integer, default=0, comment="试用状态: 0-未试用, 1-试用中, 2-已过期")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    @property
    def is_vip_active(self):
        """检查VIP是否有效"""
        if not self.is_vip or not self.vip_end_time:
            return False
        # VIP服务从vip_start_time开始，到vip_end_time结束
        if self.vip_start_time:
            return self.vip_start_time <= datetime.now() < self.vip_end_time
        return datetime.now() < self.vip_end_time
    
    @property
    def is_trial_active(self):
        """检查试用是否有效"""
        return self.trial_status == 1
    
    @property
    def has_access(self):
        """检查是否有权限访问内容"""
        return self.is_vip_active or self.is_trial_active or self.is_admin
    
class UserSubscription(BaseCommon):
    """用户订阅配置表"""
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="订阅ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    subscribe_type = Column(Integer, nullable=False, comment="订阅类型: 1-考研, 2-考公, 3-双赛道")
    status = Column(Integer, default=1, comment="订阅状态: 1-有效, 0-无效")
    config_json = Column(JSON, nullable=True, comment="订阅配置JSON")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<UserSubscription(id={self.id}, user_id={self.user_id}, subscribe_type={self.subscribe_type})>"
    
class UserKeyword(BaseCommon):
    """用户关键词表"""
    __tablename__ = "user_keywords"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="关键词ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    keyword = Column(String(100), nullable=False, comment="关键词")
    category = Column(Integer, nullable=False, comment="分类: 1-考研, 2-考公")
    is_active = Column(Boolean, default=True, comment="是否启用: 1-是, 0-否")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<UserKeyword(id={self.id}, user_id={self.user_id}, keyword={self.keyword})>"
    
class UserReadInfo(BaseCommon):
    """用户已读信息表"""
    __tablename__ = "user_read_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="已读ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    info_id = Column(Integer, nullable=False, comment="信息ID")
    category = Column(Integer, nullable=False, comment="分类: 1-考研, 2-考公")
    read_time = Column(DateTime, default=datetime.now, comment="阅读时间")
    
    def __repr__(self):
        return f"<UserReadInfo(id={self.id}, user_id={self.user_id}, info_id={self.info_id})>"
    
class UserFavorite(BaseCommon):
    """用户收藏信息表"""
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    info_id = Column(Integer, nullable=False, comment="信息ID")
    category = Column(Integer, nullable=False, comment="分类: 1-考研, 2-考公")
    created_at = Column(DateTime, default=datetime.now, comment="收藏时间")
    
    def __repr__(self):
        return f"<UserFavorite(id={self.id}, user_id={self.user_id}, info_id={self.info_id})>"
    
class Order(BaseCommon):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(32), unique=True, nullable=False, comment="订单编号")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    product_id = Column(Integer, nullable=False, comment="产品ID")
    product_name = Column(String(100), nullable=False, comment="产品名称")
    user_requirements = Column(JSON, nullable=True, comment="用户需求信息JSON")
    price = Column(Float, nullable=False, comment="价格")
    quantity = Column(Integer, default=1, comment="数量")
    total_amount = Column(Float, nullable=False, comment="总金额")
    payment_method = Column(Integer, nullable=False, comment="支付方式: 1-微信支付, 2-支付宝")
    payment_status = Column(Integer, default=0, comment="支付状态: 0-待支付, 1-已支付, 2-已取消, 3-已退款")
    trade_no = Column(String(100), nullable=True, comment="支付平台交易号")
    payment_time = Column(DateTime, nullable=True, comment="支付时间")
    refund_time = Column(DateTime, nullable=True, comment="退款时间")
    expire_time = Column(DateTime, nullable=True, comment="过期时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_no={self.order_no}, user_id={self.user_id})>"
    
class Product(BaseCommon):
    """产品/套餐表"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="产品ID")
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(Text, nullable=True, comment="产品描述")
    price = Column(Float, nullable=False, comment="价格")
    original_price = Column(Float, nullable=True, comment="原价")
    type = Column(Integer, nullable=False, comment="产品类型: 1-考研VIP, 2-考公VIP, 3-双赛道VIP")
    duration = Column(Integer, nullable=False, comment="有效期(天)")
    features = Column(JSON, nullable=True, comment="产品特色JSON")
    status = Column(Integer, default=1, comment="状态: 1-上架, 0-下架")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, type={self.type})>"
    
class SystemConfig(BaseCommon):
    """系统配置表"""
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置ID")
    config_key = Column(String(100), unique=True, nullable=False, comment="配置键")
    config_value = Column(Text, nullable=True, comment="配置值")
    config_type = Column(Integer, default=0, comment="配置类型: 0-字符串, 1-数字, 2-布尔值, 3-JSON")
    description = Column(String(255), nullable=True, comment="配置描述")
    is_system = Column(Boolean, default=False, comment="是否系统配置: 1-是, 0-否")
    status = Column(Integer, default=1, comment="状态: 1-启用, 0-禁用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<SystemConfig(id={self.id}, config_key={self.config_key})>"
    
class PushTemplate(BaseCommon):
    """推送模板表"""
    __tablename__ = "push_templates"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="模板ID")
    name = Column(String(100), nullable=False, comment="模板名称")
    type = Column(Integer, nullable=False, comment="推送类型: 1-微信模板消息, 2-企业微信, 3-短信")
    template_id = Column(String(100), nullable=False, comment="第三方模板ID")
    template_content = Column(Text, nullable=True, comment="模板内容")
    status = Column(Integer, default=1, comment="状态: 1-启用, 0-禁用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<PushTemplate(id={self.id}, name={self.name}, type={self.type})>"
    
class PushLog(BaseCommon):
    """推送日志表"""
    __tablename__ = "push_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    info_id = Column(Integer, nullable=False, comment="信息ID")
    category = Column(Integer, nullable=False, comment="分类: 1-考研, 2-考公")
    push_type = Column(Integer, nullable=False, comment="推送类型: 1-微信模板消息, 2-企业微信, 3-短信")
    push_status = Column(Integer, nullable=False, comment="推送状态: 1-成功, 0-失败")
    push_content = Column(Text, nullable=True, comment="推送内容")
    error_msg = Column(Text, nullable=True, comment="错误信息")
    push_time = Column(DateTime, default=datetime.now, comment="推送时间")
    
    def __repr__(self):
        return f"<PushLog(id={self.id}, user_id={self.user_id}, info_id={self.info_id})>"