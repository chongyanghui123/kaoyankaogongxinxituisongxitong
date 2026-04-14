from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.users import Order, Product, User
from schemas.payments import OrderCreate, OrderUpdate, OrderResponse, ProductCreate, ProductUpdate, ProductResponse, PaymentCallback

router = APIRouter(tags=["payments"])


@router.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建订单"""
    # 检查产品是否存在
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 创建订单
    db_order = Order(
        user_id=current_user.id,
        product_id=order.product_id,
        amount=product.price,
        status="pending",
        payment_method=order.payment_method,
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # 生成支付链接或参数
    # 这里需要根据实际的支付接口实现
    
    return db_order


@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户订单列表"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取订单详情"""
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.post("/callback")
async def payment_callback(
    callback: PaymentCallback,
    db: Session = Depends(get_db)
):
    """支付回调"""
    # 验证回调签名
    # 这里需要根据实际的支付接口实现
    
    # 更新订单状态
    order = db.query(Order).filter(Order.id == callback.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    order.status = "completed"
    order.paid_at = datetime.utcnow()
    order.transaction_id = callback.transaction_id
    db.commit()
    
    # 更新用户会员状态
    if order.status == "completed":
        product = db.query(Product).filter(Product.id == order.product_id).first()
        if product:
            user = db.query(User).filter(User.id == order.user_id).first()
            if user:
                # 根据产品类型更新会员状态
                # 这里需要根据实际的会员逻辑实现
                pass
    
    return {"message": "回调处理成功"}


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取产品列表"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """获取产品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


# 管理员接口

@router.post("/products", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """创建产品"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
async def update_product(
    product: ProductUpdate,
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """更新产品"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", dependencies=[Depends(get_current_admin)])
async def delete_product(
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """删除产品"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    db.delete(db_product)
    db.commit()
    return {"message": "产品删除成功"}


@router.get("/admin/orders", response_model=List[OrderResponse], dependencies=[Depends(get_current_admin)])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """获取所有订单（管理员）"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    orders = query.offset(skip).limit(limit).all()
    return orders
