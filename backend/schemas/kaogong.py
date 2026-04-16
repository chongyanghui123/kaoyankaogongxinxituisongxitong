from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KaogongInfoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str
    source: str
    url: str
    province: str
    position_type: str
    major: str
    education: str
    category: str
    publish_date: datetime


class KaogongInfoCreate(KaogongInfoBase):
    pass


class KaogongInfoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    province: Optional[str] = None
    position_type: Optional[str] = None
    major: Optional[str] = None
    education: Optional[str] = None
    category: Optional[str] = None
    publish_date: Optional[datetime] = None


class KaogongInfoResponse(KaogongInfoBase):
    id: int
    read_count: int
    like_count: int
    is_processed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class KaogongCrawlerConfigBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    url: str
    interval: int = Field(..., ge=60)  # 最小60秒
    priority: int = Field(..., ge=1, le=10)
    is_active: bool = True
    config: dict


class KaogongCrawlerConfigCreate(KaogongCrawlerConfigBase):
    pass


class KaogongCrawlerConfigUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[str] = None
    interval: Optional[int] = Field(None, ge=60)
    priority: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None
    config: Optional[dict] = None


class KaogongCrawlerConfigResponse(KaogongCrawlerConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class KaogongCrawlerLogBase(BaseModel):
    crawler_id: int
    status: str
    message: str
    duration: Optional[float] = None
    crawled_count: int = 0


class KaogongCrawlerLogCreate(KaogongCrawlerLogBase):
    pass


class KaogongCrawlerLogResponse(KaogongCrawlerLogBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
