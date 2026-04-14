from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SystemConfigBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str
    description: Optional[str] = None
    is_active: bool = True


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SystemConfigResponse(SystemConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class SystemStatsResponse(BaseModel):
    user_count: int
    kaoyan_count: int
    kaogong_count: int
    order_count: int
    push_count: int
    timestamp: datetime
    user_type_distribution: Optional[Dict[str, int]] = Field(None, description="用户类型分布")
