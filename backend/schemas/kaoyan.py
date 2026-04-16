from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KaoyanInfoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str
    source: str
    url: str
    province: str
    school: str
    major: str
    category: str
    publish_date: datetime


class KaoyanInfoCreate(KaoyanInfoBase):
    pass


class KaoyanInfoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    province: Optional[str] = None
    school: Optional[str] = None
    major: Optional[str] = None
    category: Optional[str] = None
    publish_date: Optional[datetime] = None


class KaoyanInfoResponse(KaoyanInfoBase):
    id: int
    read_count: int
    like_count: int
    is_processed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class KaoyanCrawlerConfigBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    url: str
    interval: int = Field(..., ge=60)  # 最小60秒
    priority: int = Field(..., ge=1, le=10)
    is_active: bool = True
    config: dict


class KaoyanCrawlerConfigCreate(KaoyanCrawlerConfigBase):
    pass


class KaoyanCrawlerConfigUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[str] = None
    interval: Optional[int] = Field(None, ge=60)
    priority: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None
    config: Optional[dict] = None


class KaoyanCrawlerConfigResponse(KaoyanCrawlerConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class KaoyanCrawlerLogBase(BaseModel):
    crawler_id: int
    status: str
    message: str
    duration: Optional[float] = None
    crawled_count: int = 0


class KaoyanCrawlerLogCreate(KaoyanCrawlerLogBase):
    pass


class KaoyanCrawlerLogResponse(KaoyanCrawlerLogBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
