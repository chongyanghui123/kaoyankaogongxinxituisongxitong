#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 社区模型
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey,
    Table, Float, Enum
)
from sqlalchemy.orm import relationship
from core.database import BaseCommon
import enum


class GroupStatus(enum.Enum):
    """小组状态枚举"""
    ACTIVE = 1  # 活跃
    INACTIVE = 0  # 不活跃


class QuestionStatus(enum.Enum):
    """问题状态枚举"""
    OPEN = 1  # 开放
    CLOSED = 0  # 关闭
    RESOLVED = 2  # 已解决


class AnswerStatus(enum.Enum):
    """回答状态枚举"""
    ACTIVE = 1  # 活跃
    DELETED = 0  # 已删除


class CommentStatus(enum.Enum):
    """评论状态枚举"""
    ACTIVE = 1  # 活跃
    DELETED = 0  # 已删除


class LikeType(enum.Enum):
    """点赞类型枚举"""
    QUESTION = 1  # 问题
    ANSWER = 2  # 回答
    COMMENT = 3  # 评论


class Group(BaseCommon):
    """学习小组表"""
    __tablename__ = "community_groups"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="小组ID")
    name = Column(String(100), nullable=False, comment="小组名称")
    description = Column(Text, nullable=True, comment="小组描述")
    avatar = Column(String(255), nullable=True, comment="小组头像URL")
    cover = Column(String(255), nullable=True, comment="小组封面URL")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建者ID")
    status = Column(Integer, default=1, comment="状态: 1-活跃, 0-不活跃")
    member_count = Column(Integer, default=0, comment="成员数量")
    join_type = Column(Integer, default=1, comment="加入类型: 1-自由加入, 2-审核加入, 3-邀请加入")
    tags = Column(String(255), nullable=True, comment="标签，逗号分隔")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    creator = relationship("User", foreign_keys=[creator_id])
    members = relationship("GroupMember", back_populates="group")
    posts = relationship("GroupPost", back_populates="group")
    messages = relationship("GroupMessage", back_populates="group")
    
    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name}, creator_id={self.creator_id})>"


class GroupMember(BaseCommon):
    """小组成员表"""
    __tablename__ = "community_group_members"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="成员ID")
    group_id = Column(Integer, ForeignKey("community_groups.id"), nullable=False, comment="小组ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    role = Column(Integer, default=0, comment="角色: 0-普通成员, 1-管理员, 2-创建者")
    status = Column(Integer, default=1, comment="状态: 1-已加入, 0-待审核, 2-已拒绝")
    join_time = Column(DateTime, default=datetime.now, comment="加入时间")
    last_active_time = Column(DateTime, nullable=True, comment="最后活跃时间")
    
    # 关联
    group = relationship("Group", back_populates="members")
    user = relationship("User")
    
    def __repr__(self):
        return f"<GroupMember(id={self.id}, group_id={self.group_id}, user_id={self.user_id})>"


class GroupPost(BaseCommon):
    """小组帖子表"""
    __tablename__ = "community_group_posts"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="帖子ID")
    group_id = Column(Integer, ForeignKey("community_groups.id"), nullable=False, comment="小组ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    title = Column(String(200), nullable=False, comment="帖子标题")
    content = Column(Text, nullable=False, comment="帖子内容")
    image_urls = Column(String(500), nullable=True, comment="图片URL，逗号分隔")
    view_count = Column(Integer, default=0, comment="浏览量")
    comment_count = Column(Integer, default=0, comment="评论数")
    like_count = Column(Integer, default=0, comment="点赞数")
    status = Column(Integer, default=1, comment="状态: 1-活跃, 0-已删除")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    group = relationship("Group", back_populates="posts")
    user = relationship("User")
    comments = relationship("GroupPostComment", back_populates="post")
    
    def __repr__(self):
        return f"<GroupPost(id={self.id}, title={self.title}, user_id={self.user_id})>"


class GroupPostComment(BaseCommon):
    """小组帖子评论表"""
    __tablename__ = "community_group_post_comments"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="评论ID")
    post_id = Column(Integer, ForeignKey("community_group_posts.id"), nullable=False, comment="帖子ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    content = Column(Text, nullable=False, comment="评论内容")
    parent_id = Column(Integer, nullable=True, comment="父评论ID，用于回复")
    like_count = Column(Integer, default=0, comment="点赞数")
    status = Column(Integer, default=1, comment="状态: 1-活跃, 0-已删除")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    post = relationship("GroupPost", back_populates="comments")
    user = relationship("User")
    
    def __repr__(self):
        return f"<GroupPostComment(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"


class Question(BaseCommon):
    """问题表"""
    __tablename__ = "community_questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="问题ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    title = Column(String(200), nullable=False, comment="问题标题")
    content = Column(Text, nullable=False, comment="问题内容")
    image_urls = Column(String(500), nullable=True, comment="图片URL，逗号分隔")
    category = Column(String(50), nullable=True, comment="分类")
    tags = Column(String(255), nullable=True, comment="标签，逗号分隔")
    view_count = Column(Integer, default=0, comment="浏览量")
    answer_count = Column(Integer, default=0, comment="回答数")
    like_count = Column(Integer, default=0, comment="点赞数")
    status = Column(Integer, default=1, comment="状态: 1-开放, 0-关闭, 2-已解决")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    user = relationship("User")
    answers = relationship("Answer", back_populates="question")
    
    def __repr__(self):
        return f"<Question(id={self.id}, title={self.title}, user_id={self.user_id})>"


class Answer(BaseCommon):
    """回答表"""
    __tablename__ = "community_answers"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="回答ID")
    question_id = Column(Integer, ForeignKey("community_questions.id"), nullable=False, comment="问题ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    content = Column(Text, nullable=False, comment="回答内容")
    image_urls = Column(String(500), nullable=True, comment="图片URL，逗号分隔")
    like_count = Column(Integer, default=0, comment="点赞数")
    is_accepted = Column(Boolean, default=False, comment="是否被采纳")
    status = Column(Integer, default=1, comment="状态: 1-活跃, 0-已删除")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    question = relationship("Question", back_populates="answers")
    user = relationship("User")
    comments = relationship("AnswerComment", back_populates="answer")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, user_id={self.user_id})>"


class AnswerComment(BaseCommon):
    """回答评论表"""
    __tablename__ = "community_answer_comments"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="评论ID")
    answer_id = Column(Integer, ForeignKey("community_answers.id"), nullable=False, comment="回答ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    content = Column(Text, nullable=False, comment="评论内容")
    parent_id = Column(Integer, nullable=True, comment="父评论ID，用于回复")
    like_count = Column(Integer, default=0, comment="点赞数")
    status = Column(Integer, default=1, comment="状态: 1-活跃, 0-已删除")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联
    answer = relationship("Answer", back_populates="comments")
    user = relationship("User")
    
    def __repr__(self):
        return f"<AnswerComment(id={self.id}, answer_id={self.answer_id}, user_id={self.user_id})>"


class Like(BaseCommon):
    """点赞表"""
    __tablename__ = "community_likes"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="点赞ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    target_type = Column(Integer, nullable=False, comment="目标类型: 1-问题, 2-回答, 3-评论, 4-帖子")
    target_id = Column(Integer, nullable=False, comment="目标ID")
    created_at = Column(DateTime, default=datetime.now, comment="点赞时间")
    
    # 关联
    user = relationship("User")
    
    def __repr__(self):
        return f"<Like(id={self.id}, user_id={self.user_id}, target_type={self.target_type}, target_id={self.target_id})>"


class Report(BaseCommon):
    """举报表"""
    __tablename__ = "community_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="举报ID")
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="举报者ID")
    target_type = Column(Integer, nullable=False, comment="目标类型: 1-问题, 2-回答, 3-评论, 4-帖子, 5-用户")
    target_id = Column(Integer, nullable=False, comment="目标ID")
    reason = Column(Text, nullable=False, comment="举报原因")
    status = Column(Integer, default=0, comment="处理状态: 0-待处理, 1-已处理, 2-已驳回")
    handler_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="处理人ID")
    handle_time = Column(DateTime, nullable=True, comment="处理时间")
    handle_note = Column(Text, nullable=True, comment="处理备注")
    created_at = Column(DateTime, default=datetime.now, comment="举报时间")
    
    # 关联
    reporter = relationship("User", foreign_keys=[reporter_id])
    handler = relationship("User", foreign_keys=[handler_id])
    
    def __repr__(self):
        return f"<Report(id={self.id}, reporter_id={self.reporter_id}, target_type={self.target_type})>"


class GroupMessage(BaseCommon):
    """群聊消息表"""
    __tablename__ = "community_group_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="消息ID")
    group_id = Column(Integer, ForeignKey("community_groups.id"), nullable=False, comment="小组ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="发送者ID")
    message_type = Column(Integer, default=1, comment="消息类型: 1-文字, 2-图片, 3-系统消息")
    content = Column(Text, nullable=True, comment="消息内容")
    image_url = Column(String(255), nullable=True, comment="图片URL")
    status = Column(Integer, default=1, comment="状态: 1-正常, 0-已撤回")
    created_at = Column(DateTime, default=datetime.now, comment="发送时间")
    
    # 关联
    group = relationship("Group", back_populates="messages")
    user = relationship("User")
    
    def __repr__(self):
        return f"<GroupMessage(id={self.id}, group_id={self.group_id}, user_id={self.user_id})>"
