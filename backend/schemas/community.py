#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 社区相关Schema
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# 学习小组相关Schema

class GroupBase(BaseModel):
    """小组基础信息"""
    name: str = Field(..., min_length=1, max_length=100, description="小组名称")
    description: Optional[str] = Field(None, max_length=500, description="小组描述")
    avatar: Optional[str] = Field(None, description="小组头像URL")
    cover: Optional[str] = Field(None, description="小组封面URL")
    join_type: int = Field(1, ge=1, le=3, description="加入类型: 1-自由加入, 2-审核加入, 3-邀请加入")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class GroupCreate(GroupBase):
    """创建小组请求"""
    pass


class GroupUpdate(BaseModel):
    """更新小组请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="小组名称")
    description: Optional[str] = Field(None, max_length=500, description="小组描述")
    avatar: Optional[str] = Field(None, description="小组头像URL")
    cover: Optional[str] = Field(None, description="小组封面URL")
    join_type: Optional[int] = Field(None, ge=1, le=3, description="加入类型: 1-自由加入, 2-审核加入, 3-邀请加入")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class GroupResponse(GroupBase):
    """小组响应"""
    id: int
    creator_id: int
    status: int
    member_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GroupMemberBase(BaseModel):
    """小组成员基础信息"""
    group_id: int
    user_id: int
    role: int = Field(0, ge=0, le=2, description="角色: 0-普通成员, 1-管理员, 2-创建者")
    status: int = Field(1, ge=0, le=2, description="状态: 1-已加入, 0-待审核, 2-已拒绝")


class GroupMemberCreate(GroupMemberBase):
    """创建小组成员请求"""
    pass


class GroupMemberResponse(GroupMemberBase):
    """小组成员响应"""
    id: int
    join_time: datetime
    last_active_time: Optional[datetime]
    
    class Config:
        from_attributes = True


# 问答板块相关Schema

class QuestionBase(BaseModel):
    """问题基础信息"""
    title: str = Field(..., min_length=1, max_length=200, description="问题标题")
    content: str = Field(..., min_length=1, description="问题内容")
    image_urls: Optional[str] = Field(None, description="图片URL，逗号分隔")
    category: Optional[str] = Field(None, description="分类")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class QuestionCreate(QuestionBase):
    """创建问题请求"""
    pass


class QuestionUpdate(BaseModel):
    """更新问题请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="问题标题")
    content: Optional[str] = Field(None, min_length=1, description="问题内容")
    image_urls: Optional[str] = Field(None, description="图片URL，逗号分隔")
    category: Optional[str] = Field(None, description="分类")
    tags: Optional[str] = Field(None, description="标签，逗号分隔")


class QuestionResponse(QuestionBase):
    """问题响应"""
    id: int
    user_id: int
    view_count: int
    answer_count: int
    like_count: int
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    """回答基础信息"""
    content: str = Field(..., min_length=1, description="回答内容")
    image_urls: Optional[str] = Field(None, description="图片URL，逗号分隔")


class AnswerCreate(AnswerBase):
    """创建回答请求"""
    pass


class AnswerUpdate(BaseModel):
    """更新回答请求"""
    content: Optional[str] = Field(None, min_length=1, description="回答内容")
    image_urls: Optional[str] = Field(None, description="图片URL，逗号分隔")


class AnswerResponse(AnswerBase):
    """回答响应"""
    id: int
    question_id: int
    user_id: int
    like_count: int
    is_accepted: bool
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    """评论基础信息"""
    content: str = Field(..., min_length=1, description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID，用于回复")


class CommentCreate(CommentBase):
    """创建评论请求"""
    pass


class CommentResponse(CommentBase):
    """评论响应"""
    id: int
    user_id: int
    like_count: int
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LikeResponse(BaseModel):
    """点赞响应"""
    id: int
    user_id: int
    target_type: int
    target_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportBase(BaseModel):
    """举报基础信息"""
    target_type: int = Field(..., ge=1, le=5, description="目标类型: 1-问题, 2-回答, 3-评论, 4-帖子, 5-用户")
    target_id: int
    reason: str = Field(..., min_length=1, description="举报原因")


class ReportCreate(ReportBase):
    """创建举报请求"""
    pass


class ReportResponse(ReportBase):
    """举报响应"""
    id: int
    reporter_id: int
    status: int
    handler_id: Optional[int]
    handle_time: Optional[datetime]
    handle_note: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
