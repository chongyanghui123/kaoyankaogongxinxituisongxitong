from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ExamScheduleBase(BaseModel):
    """考试日程基本信息"""
    name: str = Field(..., max_length=255, description="考试名称")
    exam_type: int = Field(..., ge=1, le=2, description="考试类型: 1-考研, 2-考公")
    exam_date: datetime = Field(..., description="考试日期")
    description: Optional[str] = Field(None, description="考试描述")
    is_active: Optional[bool] = Field(True, description="是否启用")
    
    class Config:
        orm_mode = True


class ExamScheduleCreate(ExamScheduleBase):
    """创建考试日程"""
    pass


class ExamScheduleUpdate(BaseModel):
    """更新考试日程"""
    name: Optional[str] = Field(None, max_length=255, description="考试名称")
    exam_type: Optional[int] = Field(None, ge=1, le=2, description="考试类型: 1-考研, 2-考公")
    exam_date: Optional[datetime] = Field(None, description="考试日期")
    description: Optional[str] = Field(None, description="考试描述")
    is_active: Optional[bool] = Field(None, description="是否启用")
    
    class Config:
        orm_mode = True


class ExamScheduleResponse(ExamScheduleBase):
    """考试日程响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class ExamScheduleWithCountdown(ExamScheduleResponse):
    """考试日程带倒计时"""
    countdown: dict = Field(..., description="倒计时信息: {days, hours, minutes, seconds}")


class CarouselBase(BaseModel):
    """轮播图基本信息"""
    title: str = Field(..., max_length=255, description="轮播图标题")
    subtitle: Optional[str] = Field(None, max_length=500, description="轮播图副标题")
    image_url: Optional[str] = Field(None, max_length=500, description="轮播图图片URL")
    link_url: Optional[str] = Field(None, max_length=500, description="跳转链接URL")
    sort_order: Optional[int] = Field(0, description="排序顺序")
    is_active: Optional[bool] = Field(True, description="是否启用")
    
    class Config:
        orm_mode = True


class CarouselCreate(CarouselBase):
    """创建轮播图"""
    pass


class CarouselUpdate(BaseModel):
    """更新轮播图"""
    title: Optional[str] = Field(None, max_length=255, description="轮播图标题")
    subtitle: Optional[str] = Field(None, max_length=500, description="轮播图副标题")
    image_url: Optional[str] = Field(None, max_length=500, description="轮播图图片URL")
    link_url: Optional[str] = Field(None, max_length=500, description="跳转链接URL")
    sort_order: Optional[int] = Field(None, description="排序顺序")
    is_active: Optional[bool] = Field(None, description="是否启用")
    
    class Config:
        orm_mode = True


class CarouselResponse(CarouselBase):
    """轮播图响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class ExamScheduleList(BaseModel):
    """考试日程列表响应"""
    total: int
    items: List[ExamScheduleResponse]


class CarouselList(BaseModel):
    """轮播图列表响应"""
    total: int
    items: List[CarouselResponse]
