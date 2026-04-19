from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import time

from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.users import Order, Product, User, UserSubscription
from schemas.payments import OrderCreate, OrderUpdate, OrderResponse, ProductCreate, ProductUpdate, ProductResponse, PaymentCallback

# 导入邮件发送功能
from core.push_manager import send_email

router = APIRouter(tags=["payments"])


@router.post("/orders")
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """创建订单"""
    # 检查产品是否存在
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 确定订单关联的用户ID
    user_id = None
    
    # 如果订单中包含用户ID，则使用该用户ID
    if hasattr(order, 'user_id') and order.user_id:
        # 检查指定的用户是否存在
        target_user = db.query(User).filter(User.id == order.user_id).first()
        if target_user:
            user_id = order.user_id
    
    # 如果没有提供用户ID，但有用户需求信息，则创建新用户或使用现有用户
    if not user_id and order.user_requirements:
        # 从用户需求中提取联系方式
        user_email = None
        user_phone = None
        user_username = None
        
        if isinstance(order.user_requirements, dict):
            if "email" in order.user_requirements:
                user_email = order.user_requirements["email"]
            if "phone" in order.user_requirements:
                user_phone = order.user_requirements["phone"]
            if "username" in order.user_requirements:
                user_username = order.user_requirements["username"]
            if "real_name" in order.user_requirements:
                user_username = order.user_requirements["real_name"]
        
        # 检查用户是否已存在（通过邮箱或手机号）
        existing_user = None
        if user_email:
            existing_user = db.query(User).filter(User.email == user_email).first()
        if not existing_user and user_phone:
            existing_user = db.query(User).filter(User.phone == user_phone).first()
        
        if existing_user:
            user_id = existing_user.id
        else:
            # 邮箱和手机号都不存在，创建新用户
            if not user_username:
                user_username = f"user_{int(time.time() * 1000)}"
            if not user_phone:
                user_phone = f"138{int(time.time() * 1000) % 10000000}"
            
            from core.security import get_password_hash
            new_user = User(
                username=user_username,
                email=user_email,
                phone=user_phone,
                password=get_password_hash("123456789"),  # 为用户设置默认密码
                is_admin=False,
                is_active=True,
                is_vip=False
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_id = new_user.id
    
    # 确保有用户ID
    if not user_id:
        # 如果没有提供用户ID，且没有用户需求信息，则返回错误
        if not order.user_requirements:
            raise HTTPException(status_code=400, detail="需要提供用户ID或用户需求信息")
        
        # 从用户需求信息中提取联系方式并创建新用户
        user_username = f"user_{int(time.time() * 1000)}"
        user_email = f"user_{int(time.time() * 1000)}@example.com"
        user_phone = f"138{int(time.time() * 1000) % 10000000}"  # 生成唯一的手机号
        
        if isinstance(order.user_requirements, dict):
            if "email" in order.user_requirements:
                user_email = order.user_requirements["email"]
            if "phone" in order.user_requirements:
                user_phone = order.user_requirements["phone"]
            if "username" in order.user_requirements:
                user_username = order.user_requirements["username"]
            if "real_name" in order.user_requirements:
                user_username = order.user_requirements["real_name"]
        
        from core.security import get_password_hash
        new_user = User(
            username=user_username,
            email=user_email,
            phone=user_phone,
            password=get_password_hash("123456789"),  # 为用户设置默认密码
            is_admin=False,
            is_active=True,
            is_vip=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_id = new_user.id
    
    # 创建订单
    db_order = Order(
        order_no=f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id}{product.id}",
        user_id=user_id,
        product_id=order.product_id,
        product_name=product.name,
        price=product.price,
        quantity=1,
        total_amount=product.price,
        payment_method=int(order.payment_method),
        payment_status=0,  # 0-待支付
        user_requirements=order.user_requirements,
        created_at=datetime.now()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # 处理用户需求信息
    if order.user_requirements:
        # 检查用户是否已有订阅配置
        existing_subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if existing_subscription:
            # 更新现有订阅配置
            # 只保存考研和考公需求信息
            config_data = {
                'kaoyan': order.user_requirements.get('kaoyan_requirements', {}),
                'kaogong': order.user_requirements.get('kaogong_requirements', {})
            }
            existing_subscription.config_json = config_data
            existing_subscription.updated_at = datetime.now()
        else:
            # 创建新的订阅配置
            # 根据产品类型确定订阅类型
            subscribe_type = product.type
            
            # 只保存考研和考公需求信息
            config_data = {
                'kaoyan': order.user_requirements.get('kaoyan_requirements', {}),
                'kaogong': order.user_requirements.get('kaogong_requirements', {})
            }
            
            new_subscription = UserSubscription(
                user_id=user_id,
                subscribe_type=subscribe_type,
                status=1,
                config_json=config_data,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_subscription)
            print(f"DEBUG: 保存用户需求信息到订阅配置: user_id={user_id}, config_json={config_data}")
        
        # 处理关键词
        from models.users import UserKeyword
        
        # 清除用户现有关键词
        db.query(UserKeyword).filter(
            UserKeyword.user_id == user_id
        ).delete()
        
        # 添加新关键词
        if order.user_requirements:
            # 处理考研关键词
            if order.user_requirements.get('kaoyan_requirements'):
                kaoyan_keywords = order.user_requirements['kaoyan_requirements'].get('keywords', [])
                # 兼容字符串和数组格式的关键词
                if isinstance(kaoyan_keywords, str):
                    if kaoyan_keywords:
                        for keyword in kaoyan_keywords.split(','):
                            keyword = keyword.strip()
                            if keyword:
                                new_keyword = UserKeyword(
                                    user_id=user_id,
                                    keyword=keyword,
                                    category=1,  # 1-考研
                                    is_active=True,
                                    created_at=datetime.now()
                                )
                                db.add(new_keyword)
                elif isinstance(kaoyan_keywords, list):
                    for keyword in kaoyan_keywords:
                        keyword = str(keyword).strip()
                        if keyword:
                            new_keyword = UserKeyword(
                                user_id=user_id,
                                keyword=keyword,
                                category=1,  # 1-考研
                                is_active=True,
                                created_at=datetime.now()
                            )
                            db.add(new_keyword)
            
            # 处理考公关键词
            if order.user_requirements.get('kaogong_requirements'):
                kaogong_keywords = order.user_requirements['kaogong_requirements'].get('keywords', [])
                # 兼容字符串和数组格式的关键词
                if isinstance(kaogong_keywords, str):
                    if kaogong_keywords:
                        for keyword in kaogong_keywords.split(','):
                            keyword = keyword.strip()
                            if keyword:
                                new_keyword = UserKeyword(
                                    user_id=user_id,
                                    keyword=keyword,
                                    category=2,  # 2-考公
                                    is_active=True,
                                    created_at=datetime.now()
                                )
                                db.add(new_keyword)
                elif isinstance(kaogong_keywords, list):
                    for keyword in kaogong_keywords:
                        keyword = str(keyword).strip()
                        if keyword:
                            new_keyword = UserKeyword(
                                user_id=user_id,
                                keyword=keyword,
                                category=2,  # 2-考公
                                is_active=True,
                                created_at=datetime.now()
                            )
                            db.add(new_keyword)
        
        db.commit()
    db.refresh(db_order)
    
    # 生成支付链接或参数
    # 这里需要根据实际的支付接口实现
    
    return JSONResponse(content={
        "success": True,
        "code": 200,
        "message": "订单创建成功",
        "data": {
            "id": db_order.id,
            "order_no": db_order.order_no,
            "user_id": db_order.user_id,
            "product_id": db_order.product_id,
            "product_name": db_order.product_name,
            "price": db_order.price,
            "quantity": db_order.quantity,
            "total_amount": db_order.total_amount,
            "payment_method": db_order.payment_method,
            "payment_status": db_order.payment_status,
            "created_at": db_order.created_at.isoformat(),
            "updated_at": db_order.updated_at.isoformat() if db_order.updated_at else None
        }
    })


@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    payment_status: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户订单列表"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.get("/orders/{order_id}")
async def get_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取订单详情"""
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"success": True, "code": 200, "message": "获取订单详情成功", "data": order}


@router.post("/orders/{order_id}/pay")
async def pay_order(
    order_id: int = Path(..., gt=0),
    payment_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """支付订单"""
    # 如果是管理员，可以支付任意订单；否则只能支付自己的订单
    if current_user.is_admin:
        order = db.query(Order).filter(Order.id == order_id).first()
    else:
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
        
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.payment_status == 1:
        raise HTTPException(status_code=400, detail="订单已支付")
    
    if order.payment_status == 2:
        raise HTTPException(status_code=400, detail="订单已取消")
    
    # 更新支付方式
    payment_method = payment_data.get("payment_method")
    if payment_method:
        order.payment_method = payment_method
    
    # 模拟支付成功
    order.payment_status = 1
    order.payment_time = datetime.now()
    order.updated_at = datetime.now()
    
    # 更新用户会员状态
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        user = db.query(User).filter(User.id == order.user_id).first()
        if user:
            # 计算服务到期时间：从支付的第二天开始算
            from datetime import timedelta
            vip_start_time = order.payment_time + timedelta(days=1)  # 支付第二天开始
            vip_end_time = vip_start_time + timedelta(days=product.duration)  # 根据产品有效期计算
            
            # 更新用户VIP状态
            user.is_vip = True
            user.vip_start_time = vip_start_time
            user.vip_end_time = vip_end_time
            user.vip_type = product.type
            user.updated_at = datetime.now()
            
            # 发送邮件通知
            if user.email:
                # 根据产品类型确定服务类型
                if product.type == 1:
                    service_type = "考研"
                elif product.type == 2:
                    service_type = "考公"
                elif product.type == 3:
                    service_type = "考研考公"
                else:
                    service_type = "推送"
                
                email_subject = f"【支付成功】您的{service_type}推送服务已开通"
                email_content = f"尊敬的 {user.username}：\n\n恭喜您支付成功！您的{service_type}推送服务已开通。\n\n服务详情：\n产品名称：{product.name}\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                send_email(user.email, email_subject, email_content)
    
    db.commit()
    db.refresh(order)
    
    return {"success": True, "code": 200, "message": "支付成功", "data": order}


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
    
    order.payment_status = 1  # 已支付
    order.payment_time = datetime.now()
    order.trade_no = callback.transaction_id
    order.updated_at = datetime.now()
    db.commit()
    
    # 更新用户会员状态
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        user = db.query(User).filter(User.id == order.user_id).first()
        if user:
            # 计算服务到期时间：从支付的第二天开始算
            from datetime import timedelta
            vip_start_time = order.payment_time + timedelta(days=1)  # 支付第二天开始
            vip_end_time = vip_start_time + timedelta(days=product.duration)  # 根据产品有效期计算
            
            # 更新用户VIP状态
            user.is_vip = True
            user.vip_start_time = vip_start_time
            user.vip_end_time = vip_end_time
            user.vip_type = product.type
            user.updated_at = datetime.now()
            
            # 发送邮件通知
            if user.email:
                # 根据产品类型确定服务类型
                if product.type == 1:
                    service_type = "考研"
                elif product.type == 2:
                    service_type = "考公"
                elif product.type == 3:
                    service_type = "考研考公"
                else:
                    service_type = "推送"
                
                email_subject = f"【支付成功】您的{service_type}推送服务已开通"
                email_content = f"尊敬的 {user.username}：\n\n恭喜您支付成功！您的{service_type}推送服务已开通。\n\n服务详情：\n产品名称：{product.name}\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                send_email(user.email, email_subject, email_content)
            
            db.commit()
    
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
    payment_status: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    order_no: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取所有订单（管理员）"""
    query = db.query(Order)
    
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    if order_no:
        query = query.filter(Order.order_no.like(f"%{order_no}%"))
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.put("/orders/{order_id}")
async def update_order(
    order_id: int = Path(..., ge=1),
    order: OrderUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新订单信息"""
    # 只允许用户更新自己的订单
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 普通用户可以更新支付方式和支付状态（取消支付）
    if order.payment_method:
        db_order.payment_method = order.payment_method
    
    if order.payment_status:
        # 只允许用户取消支付（状态为2）
        if order.payment_status == 2:
            db_order.payment_status = order.payment_status
    
    db_order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    
    return {"success": True, "code": 200, "message": "订单更新成功", "data": db_order}


@router.put("/admin/orders/{order_id}", response_model=OrderResponse, dependencies=[Depends(get_current_admin)])
async def update_order_status_admin(
    order_id: int = Path(..., ge=1),
    order: OrderUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """更新订单状态（管理员）"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 管理员可以更新所有字段
    if order.payment_status is not None:
        db_order.payment_status = order.payment_status
    
    if order.payment_method:
        db_order.payment_method = order.payment_method
    
    if order.trade_no:
        db_order.trade_no = order.trade_no
    
    if order.payment_time:
        db_order.payment_time = order.payment_time
    
    db_order.updated_at = datetime.utcnow()
    
    # 如果订单状态更新为已支付，更新用户会员状态
    if order.payment_status == 1 and db_order.payment_status != 1:
        product = db.query(Product).filter(Product.id == db_order.product_id).first()
        if product:
            user = db.query(User).filter(User.id == db_order.user_id).first()
            if user:
                # 计算服务到期时间：从支付的第二天开始算
                from datetime import timedelta
                payment_time = order.payment_time or datetime.now()
                vip_start_time = payment_time + timedelta(days=1)  # 支付第二天开始
                vip_end_time = vip_start_time + timedelta(days=product.duration)  # 根据产品有效期计算
                
                # 更新用户VIP状态
                user.is_vip = True
                user.vip_start_time = vip_start_time
                user.vip_end_time = vip_end_time
                user.vip_type = product.type
                user.updated_at = datetime.now()
                
                # 发送邮件通知
                if user.email:
                    # 根据产品类型确定服务类型
                    if product.type == 1:
                        service_type = "考研"
                    elif product.type == 2:
                        service_type = "考公"
                    elif product.type == 3:
                        service_type = "考研考公"
                    else:
                        service_type = "推送"
                    
                    email_subject = f"【支付成功】您的{service_type}推送服务已开通"
                    email_content = f"尊敬的 {user.username}：\n\n恭喜您支付成功！您的{service_type}推送服务已开通。\n\n服务详情：\n产品名称：{product.name}\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                    send_email(user.email, email_subject, email_content)
    
    db.commit()
    db.refresh(db_order)
    
    return db_order


@router.delete("/admin/orders/{order_id}", dependencies=[Depends(get_current_admin)])
async def delete_order(
    order_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """删除订单（管理员）"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    db.delete(db_order)
    db.commit()
    
    return {"success": True, "code": 200, "message": "订单删除成功"}


@router.delete("/admin/orders", dependencies=[Depends(get_current_admin)])
async def delete_all_orders(
    db: Session = Depends(get_db)
):
    """删除所有订单（管理员）"""
    # 删除所有订单
    db.query(Order).delete()
    db.commit()
    
    return {"success": True, "code": 200, "message": "所有订单删除成功"}
