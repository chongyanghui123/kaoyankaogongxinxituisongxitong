from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MessageResponse(BaseModel):
    """消息响应模型"""
    id: int
    type: str
    title: str
    content: str
    time: str
    read: bool


class MessageListResponse(BaseModel):
    """消息列表响应模型"""
    total: int
    items: List[MessageResponse]
