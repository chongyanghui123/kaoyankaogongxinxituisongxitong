#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 考公模型
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, JSON, Float
)
from core.database import BaseKaogong

class KaogongInfo(BaseKaogong):
    """考公信息表"""
    __tablename__ = "kaogong_info"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="信息ID")
    title = Column(String(500), nullable=False, comment="标题")
    source = Column(String(100), nullable=False, comment="来源")
    source_url = Column(String(500), nullable=True, comment="来源链接")
    publish_time = Column(DateTime, nullable=False, comment="发布时间")
    content = Column(Text, nullable=True, comment="内容")
    url = Column(String(500), unique=True, nullable=False, comment="原文链接")
    tags = Column(String(255), nullable=True, comment="标签(逗号分隔)")
    urgency_level = Column(Integer, default=0, comment="紧急度: 0-普通, 1-重要, 2-紧急, 3-非常紧急")
    category = Column(Integer, default=0, comment="分类: 0-普通通知, 1-公告, 2-职位表, 3-报名, 4-缴费, 5-三不限, 6-应届生, 7-竞争比")
    province = Column(String(50), nullable=True, comment="省份")
    position_type = Column(String(100), nullable=True, comment="岗位类别")
    major = Column(String(100), nullable=True, comment="专业")
    education = Column(String(50), nullable=True, comment="学历要求")
    is_fresh_graduate = Column(Boolean, nullable=True, comment="是否应届生岗: 1-是, 0-否")
    is_unlimited = Column(Boolean, nullable=True, comment="是否三不限: 1-是, 0-否")
    competition_ratio = Column(Float, nullable=True, comment="竞争比")
    is_valid = Column(Boolean, default=True, comment="是否有效: 1-有效, 0-无效")
    is_top = Column(Boolean, default=False, comment="是否置顶: 1-是, 0-否")
    is_excellent = Column(Boolean, default=False, comment="是否加精: 1-是, 0-否")
    view_count = Column(Integer, default=0, comment="浏览次数")
    like_count = Column(Integer, default=0, comment="点赞次数")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<KaogongInfo(id={self.id}, title={self.title}, source={self.source})>"
    
    @property
    def urgency_text(self):
        """获取紧急度文本"""
        urgency_map = {
            0: "普通",
            1: "重要",
            2: "紧急",
            3: "非常紧急"
        }
        return urgency_map.get(self.urgency_level, "普通")
    
    @property
    def category_text(self):
        """获取分类文本"""
        category_map = {
            0: "普通通知",
            1: "公告",
            2: "职位表",
            3: "报名",
            4: "缴费",
            5: "三不限",
            6: "应届生",
            7: "竞争比"
        }
        return category_map.get(self.category, "普通通知")
    
    @property
    def is_fresh_graduate_text(self):
        """获取是否应届生岗文本"""
        if self.is_fresh_graduate is None:
            return ""
        return "是" if self.is_fresh_graduate else "否"
    
    @property
    def is_unlimited_text(self):
        """获取是否三不限文本"""
        if self.is_unlimited is None:
            return ""
        return "是" if self.is_unlimited else "否"
    
class KaogongCrawlerConfig(BaseKaogong):
    """考公爬虫配置表"""
    __tablename__ = "kaogong_crawler_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="配置ID")
    name = Column(String(100), nullable=False, comment="配置名称")
    url = Column(String(500), unique=True, nullable=False, comment="监控网址")
    selector = Column(Text, nullable=True, comment="页面选择器")
    parse_rules = Column(JSON, nullable=True, comment="解析规则")
    interval = Column(Integer, default=10, comment="抓取间隔(分钟)")
    status = Column(Integer, default=1, comment="状态: 1-启用, 0-禁用")
    priority = Column(Integer, default=0, comment="优先级: 0-普通, 1-高, 2-非常高")
    user_id = Column(Integer, nullable=True, comment="用户ID")
    last_crawl_time = Column(DateTime, nullable=True, comment="最后抓取时间")
    next_crawl_time = Column(DateTime, nullable=True, comment="下次抓取时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<KaogongCrawlerConfig(id={self.id}, name={self.name}, url={self.url})>"
    
    @property
    def status_text(self):
        """获取状态文本"""
        return "启用" if self.status == 1 else "禁用"
    
    @property
    def priority_text(self):
        """获取优先级文本"""
        priority_map = {
            0: "普通",
            1: "高",
            2: "非常高"
        }
        return priority_map.get(self.priority, "普通")
    
class KaogongCrawlerLog(BaseKaogong):
    """考公爬虫日志表"""
    __tablename__ = "kaogong_crawler_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    config_id = Column(Integer, nullable=False, comment="配置ID")
    url = Column(String(500), nullable=False, comment="抓取网址")
    status = Column(Integer, nullable=False, comment="状态: 1-成功, 0-失败")
    info_count = Column(Integer, default=0, comment="抓取信息数量")
    error_msg = Column(Text, nullable=True, comment="错误信息")
    crawl_time = Column(DateTime, default=datetime.now, comment="抓取时间")
    
    def __repr__(self):
        return f"<KaogongCrawlerLog(id={self.id}, config_id={self.config_id}, status={self.status})>"
    
    @property
    def status_text(self):
        """获取状态文本"""
        return "成功" if self.status == 1 else "失败"