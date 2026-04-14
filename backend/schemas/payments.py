from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    product_id: int
    payment_method: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    transaction_id: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    amount: float
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    price: float = Field(..., gt=0)
    type: int
    duration: Optional[int] = None  # 会员时长（天）
    status: int = 1


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    type: Optional[int] = None
    duration: Optional[int] = None
    status: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    status: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class PaymentCallback(BaseModel):
    order_id: int
    transaction_id: str
    status: str
    amount: float
