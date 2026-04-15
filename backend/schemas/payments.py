from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    product_id: int
    user_id: int
    quantity: int = 1
    payment_method: int


class OrderCreate(BaseModel):
    product_id: int
    payment_method: int
    user_requirements: Optional[dict] = None
    user_id: Optional[int] = None


class OrderUpdate(BaseModel):
    payment_status: Optional[int] = Field(None, ge=0, le=3)
    payment_method: Optional[int] = None
    trade_no: Optional[str] = None
    payment_time: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    order_no: str
    user_id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    total_amount: float
    payment_method: int
    payment_status: int

    payment_time: Optional[datetime] = None
    refund_time: Optional[datetime] = None
    expire_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
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
