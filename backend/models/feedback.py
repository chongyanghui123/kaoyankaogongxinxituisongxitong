from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from core.database import BaseCommon as Base


class FeedbackType(enum.Enum):
    SUGGESTION = 1  # 功能建议
    PROBLEM = 2     # 问题反馈
    OTHER = 3       # 其他


class FeedbackStatus(enum.Enum):
    PENDING = "pending"     # 处理中
    PROCESSED = "processed" # 已处理


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, comment="用户ID")
    type = Column(Enum(FeedbackType), nullable=False)
    content = Column(Text, nullable=False)
    contact = Column(String(255), nullable=True)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.PENDING)
    reply = Column(Text, nullable=True, comment="管理员回复")
    reply_at = Column(DateTime(timezone=True), nullable=True, comment="回复时间")
    is_deleted_by_user = Column(Boolean, default=False, comment="用户是否删除")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())