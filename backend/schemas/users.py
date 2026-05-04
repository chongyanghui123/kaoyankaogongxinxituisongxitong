from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    real_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_vip: bool = False  # 新增字段：是否VIP
    vip_type: int = 0  # 新增字段：VIP类型
    vip_start_time: Optional[datetime] = None  # 新增字段：VIP开始时间
    vip_end_time: Optional[datetime] = None  # 新增字段：服务到期时间
    login_count: int = 0  # 新增字段：登录次数
    
    class Config:
        orm_mode = True


class UserSubscription(BaseModel):
    id: int
    user_id: int
    subscription_type: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    
    class Config:
        orm_mode = True


class UserKeyword(BaseModel):
    id: int
    user_id: int
    keyword: str
    category: str
    
    class Config:
        orm_mode = True


class UserReadInfo(BaseModel):
    id: int
    user_id: int
    info_type: str
    info_id: int
    read_at: datetime
    
    class Config:
        orm_mode = True


class UserFavorite(BaseModel):
    id: int
    user_id: int
    info_type: str
    info_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserStats(BaseModel):
    total_read: int
    total_favorites: int
    total_keywords: int
    subscription_status: Optional[str] = None
