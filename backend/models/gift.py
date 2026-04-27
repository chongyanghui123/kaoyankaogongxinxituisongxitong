#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 礼品模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import BaseCommon


class Gift(BaseCommon):
    """礼品表"""
    __tablename__ = "gifts"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="礼品ID")
    name = Column(String(100), nullable=False, comment="礼品名称")
    description = Column(Text, nullable=True, comment="礼品描述")
    image_url = Column(String(500), nullable=True, comment="礼品图片URL")
    points_required = Column(Integer, nullable=False, comment="所需积分")
    stock = Column(Integer, default=0, comment="库存数量")
    exchanged_count = Column(Integer, default=0, comment="已兑换数量")
    is_active = Column(Boolean, default=True, comment="是否上架")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<Gift(id={self.id}, name={self.name}, points={self.points_required})>"


class GiftExchange(BaseCommon):
    """礼品兑换记录表"""
    __tablename__ = "gift_exchanges"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="兑换ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    gift_id = Column(Integer, ForeignKey("gifts.id"), nullable=False, comment="礼品ID")
    points_used = Column(Integer, nullable=False, comment="使用积分")
    status = Column(Integer, default=0, comment="状态: 0-待处理, 1-已发货, 2-已完成, 3-已取消")
    tracking_number = Column(String(100), nullable=True, comment="快递单号")
    remark = Column(String(255), nullable=True, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="兑换时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    user = relationship("User", backref="gift_exchanges")
    gift = relationship("Gift", backref="exchanges")
    
    def __repr__(self):
        return f"<GiftExchange(id={self.id}, user_id={self.user_id}, gift_id={self.gift_id})>"
