#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 签到模型
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.database import BaseCommon


class SignInRecord(BaseCommon):
    """签到记录表"""
    __tablename__ = "sign_in_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="签到ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    sign_date = Column(Date, nullable=False, comment="签到日期")
    points_earned = Column(Integer, default=10, comment="获得积分")
    continuous_days = Column(Integer, default=1, comment="连续签到天数")
    ip_address = Column(String(45), nullable=True, comment="签到IP")
    device_info = Column(String(255), nullable=True, comment="设备信息")
    created_at = Column(DateTime, default=datetime.now, comment="签到时间")
    
    user = relationship("User", backref="sign_in_records")
    
    def __repr__(self):
        return f"<SignInRecord(id={self.id}, user_id={self.user_id}, sign_date={self.sign_date})>"


class PointsRecord(BaseCommon):
    """积分变动记录表"""
    __tablename__ = "points_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    points = Column(Integer, nullable=False, comment="积分变动(正数增加,负数减少)")
    balance = Column(Integer, nullable=False, comment="变动后余额")
    type = Column(Integer, nullable=False, comment="类型: 1-签到, 2-兑换, 3-系统赠送, 4-消费, 5-其他")
    description = Column(String(255), nullable=True, comment="描述")
    related_id = Column(Integer, nullable=True, comment="关联ID(如签到记录ID)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    user = relationship("User", backref="points_records")
    
    def __repr__(self):
        return f"<PointsRecord(id={self.id}, user_id={self.user_id}, points={self.points})>"
