from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class PushTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    type: int
    template_id: str
    template_content: Optional[str] = None
    is_active: bool = True
    params: Dict[str, Any] = {}


class PushTemplateCreate(PushTemplateBase):
    pass


class PushTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    type: Optional[int] = None
    template_id: Optional[str] = None
    template_content: Optional[str] = None
    is_active: Optional[bool] = None
    params: Optional[Dict[str, Any]] = None


class PushTemplateResponse(PushTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class PushLogBase(BaseModel):
    template_id: int
    user_id: int
    content: str
    status: str


class PushLogCreate(PushLogBase):
    pass


class PushLogResponse(PushLogBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class PushRequest(BaseModel):
    template_id: int
    user_id: int
    content: str
    params: Dict[str, Any] = {}
