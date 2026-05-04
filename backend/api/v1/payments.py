from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import time
import hashlib
import uuid
import json
import os

from core.database import get_db, get_db_common
from core.security import get_current_user, get_current_admin
from models.users import Order, Product, User, UserSubscription
from models.users import PushLog
from models.users import SystemConfig
from schemas.payments import OrderCreate, OrderUpdate, OrderResponse, ProductCreate, ProductUpdate, ProductResponse, PaymentCallback

# 导入日志功能
from core.logger import log_error, log_user_action

# 导入邮件发送功能
from core.push_manager import send_email

# 导入配置
from config import settings

router = APIRouter(tags=["payments"])


def generate_wechat_pay_params(order: Order, product: Product, user: User) -> dict:
    """生成微信支付参数"""
    import random
    import string
    
    # 生成随机字符串
    nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # 订单号
    out_trade_no = f"ORDER{order.id}{int(time.time())}"
    
    # 商品描述
    body = f"双赛道情报通-{product.name}"
    
    # 价格（转为分）
    total_fee = int(product.price * 100)
    
    # 微信支付参数
    pay_params = {
        "appid": settings.WXPAY_APP_ID,
        "mch_id": settings.WXPAY_MCH_ID,
        "nonce_str": nonce_str,
        "body": body,
        "out_trade_no": out_trade_no,
        "total_fee": total_fee,
        "spbill_create_ip": "127.0.0.1",
        "notify_url": settings.WXPAY_NOTIFY_URL or "http://your-domain.com/api/v1/payments/callback",
        "trade_type": "JSAPI",
        "openid": user.phone  # 使用phone作为openid的替代
    }
    
    # 生成签名
    sign_str = "&".join([f"{k}={v}" for k, v in sorted(pay_params.items()) if v]) + f"&key={settings.WXPAY_API_KEY}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    pay_params["sign"] = sign
    
    # 生成支付签名（用于wx.requestPayment）
    timeStamp = str(int(time.time()))
    package = f"prepay_id=PREPAY_ID_PLACEHOLDER"
    pay_sign_str = f"appId={settings.WXPAY_APP_ID}&nonceStr={nonce_str}&package={package}&signType=MD5&timeStamp={timeStamp}&key={settings.WXPAY_API_KEY}"
    pay_sign = hashlib.md5(pay_sign_str.encode('utf-8')).hexdigest().upper()
    
    return {
        "timeStamp": timeStamp,
        "nonceStr": nonce_str,
        "package": package,
        "signType": "MD5",
        "paySign": pay_sign,
        "out_trade_no": out_trade_no
    }


def generate_alipay_params(order: Order, product: Product) -> dict:
    """生成支付宝支付参数"""
    import random
    import string
    
    # 订单号
    out_trade_no = f"ORDER{order.id}{int(time.time())}"
    
    # 商品描述
    subject = f"双赛道情报通-{product.name}"
    
    # 价格
    total_amount = str(product.price)
    
    # 生成随机字符串
    nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # 支付宝支付参数（模拟）
    # 实际使用时需要集成支付宝SDK
    alipay_params = {
        "out_trade_no": out_trade_no,
        "subject": subject,
        "total_amount": total_amount,
        "product_code": "QUICK_MSECURITY_PAY",
        "timeout_express": "30m"
    }
    
    # 如果配置了支付宝，生成真实支付参数
    if settings.ALIPAY_APP_ID and settings.ALIPAY_PRIVATE_KEY:
        try:
            from alipay import AliPay
            
            alipay = AliPay(
                appid=settings.ALIPAY_APP_ID,
                app_notify_url=settings.ALIPAY_NOTIFY_URL or "http://your-domain.com/api/v1/payments/alipay/callback",
                app_private_key_string=settings.ALIPAY_PRIVATE_KEY,
                alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
                sign_type="RSA2",
                debug=False
            )
            
            order_string = alipay.api_alipay_trade_app_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject,
                notify_url=settings.ALIPAY_NOTIFY_URL or "http://your-domain.com/api/v1/payments/alipay/callback"
            )
            
            return {
                "order_string": order_string,
                "out_trade_no": out_trade_no,
                "alipay_trade_no": out_trade_no
            }
        except Exception as e:
            log_error(f"生成支付宝支付参数失败: {str(e)}")
            # 返回模拟参数
            return {
                "out_trade_no": out_trade_no,
                "subject": subject,
                "total_amount": total_amount,
                "alipay_trade_no": out_trade_no,
                "mock": True
            }
    
    # 返回模拟参数
    return {
        "out_trade_no": out_trade_no,
        "subject": subject,
        "total_amount": total_amount,
        "alipay_trade_no": out_trade_no,
        "mock": True
    }


def process_payment_success(order: Order, db: Session, db_common: Session, trade_no: str = None):
    """处理支付成功后的业务逻辑"""
    # 更新订单状态
    order.payment_status = 1
    order.payment_time = datetime.now()
    if trade_no:
        order.trade_no = trade_no
    order.updated_at = datetime.now()
    
    # 更新用户会员状态
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        user = db.query(User).filter(User.id == order.user_id).first()
        if user:
            # 计算服务到期时间：如果是续费，从当前到期时间延长；否则从支付第二天开始
            if user.is_vip and user.vip_end_time and user.vip_end_time > datetime.now():
                # 续费：从当前到期时间延长
                vip_start_time = user.vip_end_time
                vip_end_time = vip_start_time + timedelta(days=product.duration)
            else:
                # 新开通：从支付第二天开始
                vip_start_time = order.payment_time + timedelta(days=1)
                vip_end_time = vip_start_time + timedelta(days=product.duration)
            
            # 更新用户VIP状态
            user.is_vip = True
            user.user_type = 2
            user.vip_start_time = vip_start_time
            user.vip_end_time = vip_end_time
            user.vip_type = product.type
            user.updated_at = datetime.now()
            
            # 发送邮件通知
            if user.email:
                # 判断是续费还是新开通
                is_renewal = False
                if user.is_vip and user.vip_end_time and user.vip_end_time > datetime.now():
                    is_renewal = True
                
                if product.type == 1:
                    service_type = "考研"
                elif product.type == 2:
                    service_type = "考公"
                elif product.type == 3:
                    service_type = "考研考公"
                else:
                    service_type = "推送"
                
                # 检查是否是升级服务
                is_upgrade = False
                if is_renewal and product.type > user.vip_type:
                    is_upgrade = True
                
                # 从系统配置中获取邮件文案
                email_config = db_common.query(SystemConfig).filter(
                    SystemConfig.config_key == f"email_{product.type}"
                ).first()
                
                if email_config and email_config.config_value:
                    if is_renewal:
                        if is_upgrade:
                            email_subject = email_config.description or f"【支付成功】您的{service_type}推送服务已升级"
                        else:
                            email_subject = email_config.description or f"【支付成功】您的{service_type}推送服务已续费"
                    else:
                        email_subject = email_config.description or f"【支付成功】您的{service_type}推送服务已开通"
                    
                    email_content = email_config.config_value
                    # 替换模板变量
                    email_content = email_content.replace("{username}", user.username or "")
                    email_content = email_content.replace("{product_name}", product.name or "")
                    email_content = email_content.replace("{service_type}", service_type or "")
                    email_content = email_content.replace("{start_date}", vip_start_time.strftime('%Y-%m-%d'))
                    email_content = email_content.replace("{end_date}", vip_end_time.strftime('%Y-%m-%d'))
                    email_content = email_content.replace("{duration}", str(product.duration))
                else:
                    # 使用默认文案
                    if is_renewal:
                        if is_upgrade:
                            email_subject = f"【支付成功】您的{service_type}推送服务已升级"
                            email_content = f"""尊敬的 {user.username}：

恭喜您支付成功！您的{service_type}推送服务已升级。

服务详情：
产品名称：{product.name}
服务类型：{service_type}推送服务
原服务到期时间：{user.vip_end_time.strftime('%Y-%m-%d')}
新服务到期时间：{vip_end_time.strftime('%Y-%m-%d')}
服务时长：{product.duration}天

升级信息：
您已成功升级到{service_type}推送服务，我们将为您提供以下内容：
- 最新{service_type}相关资讯和政策变化
- 个性化的考试信息推送
- 专业的备考指导和建议
- 更多高级功能和服务

如有疑问，请联系客服。

此致
双赛道情报通团队"""
                        else:
                            email_subject = f"【支付成功】您的{service_type}推送服务已续费"
                            email_content = f"""尊敬的 {user.username}：

恭喜您支付成功！您的{service_type}推送服务已续费。

服务详情：
产品名称：{product.name}
服务类型：{service_type}推送服务
原服务到期时间：{user.vip_end_time.strftime('%Y-%m-%d')}
新服务到期时间：{vip_end_time.strftime('%Y-%m-%d')}
续费时长：{product.duration}天

续费信息：
您已成功续费{service_type}推送服务，我们将继续为您提供以下内容：
- 最新{service_type}相关资讯和政策变化
- 个性化的考试信息推送
- 专业的备考指导和建议

如有疑问，请联系客服。

此致
双赛道情报通团队"""
                    else:
                        email_subject = f"【支付成功】您的{service_type}推送服务已开通"
                        email_content = f"""尊敬的 {user.username}：

恭喜您支付成功！您的{service_type}推送服务已开通。

服务详情：
产品名称：{product.name}
服务类型：{service_type}推送服务
服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}
服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}
服务时长：{product.duration}天

订阅信息：
您已成功订阅{service_type}推送服务，我们将为您提供以下内容：
- 最新{service_type}相关资讯和政策变化
- 个性化的考试信息推送
- 专业的备考指导和建议

如有疑问，请联系客服。

此致
双赛道情报通团队"""
                send_email(user.email, email_subject, email_content)
                
                # 记录到推送历史记录
                try:
                    # 修改推送内容，添加"系统"关键词，确保归类到系统通知
                    if is_renewal:
                        if is_upgrade:
                            push_content = f"【系统通知】您的{service_type}推送服务已升级\n\n服务详情：\n产品名称：{product.name}\n服务类型：{service_type}推送服务\n原服务到期时间：{user.vip_end_time.strftime('%Y-%m-%d')}\n新服务到期时间：{vip_end_time.strftime('%Y-%m-%d')}\n服务时长：{product.duration}天\n\n升级信息：\n您已成功升级到{service_type}推送服务，我们将为您提供更多高级功能和服务。\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                        else:
                            push_content = f"【系统通知】您的{service_type}推送服务已续费\n\n服务详情：\n产品名称：{product.name}\n服务类型：{service_type}推送服务\n原服务到期时间：{user.vip_end_time.strftime('%Y-%m-%d')}\n新服务到期时间：{vip_end_time.strftime('%Y-%m-%d')}\n续费时长：{product.duration}天\n\n续费信息：\n您已成功续费{service_type}推送服务，我们将继续为您提供优质的信息推送服务。\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                    else:
                        push_content = f"【系统通知】您的{service_type}推送服务已开通\n\n服务详情：\n产品名称：{product.name}\n服务类型：{service_type}推送服务\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n服务时长：{product.duration}天\n\n订阅信息：\n您已成功订阅{service_type}推送服务，我们将为您提供以下内容：\n- 最新{service_type}相关资讯和政策变化\n- 个性化的考试信息推送\n- 专业的备考指导和建议\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                    
                    push_log = PushLog(
                        user_id=user.id,
                        info_id=order.id,
                        category=3,
                        push_type=3,
                        push_status=1,
                        push_content=push_content,
                        is_processed=1,
                        push_time=datetime.now()
                    )
                    db_common.add(push_log)
                    db_common.commit()
                except Exception as e:
                    log_error(f"记录推送历史失败: {str(e)}")
    
    db.commit()
    db.refresh(order)


@router.post("/orders")
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    db_common: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """创建订单（小程序端已登录用户直接下单）"""
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    user_id = current_user.id
    
    if order.user_requirements:
        # 更新用户基本信息
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if order.user_requirements.get('username'):
                user.username = order.user_requirements['username']
            if order.user_requirements.get('real_name'):
                user.real_name = order.user_requirements['real_name']
            if order.user_requirements.get('email'):
                user.email = order.user_requirements['email']
            if order.user_requirements.get('phone'):
                user.phone = order.user_requirements['phone']
                user.phone_bound = True
            if order.user_requirements.get('gender') is not None:
                user.gender = int(order.user_requirements['gender'])
            if order.user_requirements.get('birthdate'):
                try:
                    from datetime import datetime
                    user.birthdate = datetime.strptime(order.user_requirements['birthdate'], '%Y-%m-%d')
                except Exception as e:
                    log_error(f"解析出生日期失败: {str(e)}")
        
        # 更新用户订阅配置
        existing_subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if existing_subscription:
            config_data = {
                'kaoyan': order.user_requirements.get('kaoyan_requirements', {}),
                'kaogong': order.user_requirements.get('kaogong_requirements', {})
            }
            existing_subscription.config_json = config_data
            existing_subscription.updated_at = datetime.now()
        else:
            subscribe_type = product.type
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
        
        from models.users import UserKeyword
        db.query(UserKeyword).filter(UserKeyword.user_id == user_id).delete()
        
        if order.user_requirements.get('kaoyan_requirements'):
            kaoyan_keywords = order.user_requirements['kaoyan_requirements'].get('keywords', [])
            keyword_list = [k.strip() for k in kaoyan_keywords.split(',')] if isinstance(kaoyan_keywords, str) else kaoyan_keywords
            for keyword in keyword_list:
                keyword = str(keyword).strip()
                if keyword:
                    new_keyword = UserKeyword(
                        user_id=user_id, keyword=keyword, category=1,
                        is_active=True, created_at=datetime.now()
                    )
                    db.add(new_keyword)
        
        if order.user_requirements.get('kaogong_requirements'):
            kaogong_keywords = order.user_requirements['kaogong_requirements'].get('keywords', [])
            keyword_list = [k.strip() for k in kaogong_keywords.split(',')] if isinstance(kaogong_keywords, str) else kaogong_keywords
            for keyword in keyword_list:
                keyword = str(keyword).strip()
                if keyword:
                    new_keyword = UserKeyword(
                        user_id=user_id, keyword=keyword, category=2,
                        is_active=True, created_at=datetime.now()
                    )
                    db.add(new_keyword)
        
        db.commit()
    
    db_order = Order(
        order_no=f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id}{product.id}",
        user_id=user_id,
        product_id=order.product_id,
        product_name=product.name,
        price=product.price,
        quantity=1,
        total_amount=product.price,
        payment_method=int(order.payment_method),
        payment_status=0,
        user_requirements=order.user_requirements,
        created_at=datetime.now()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
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
            "total_amount": db_order.total_amount,
            "payment_method": db_order.payment_method,
            "payment_status": db_order.payment_status,
            "created_at": db_order.created_at.isoformat()
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
    db_common: Session = Depends(get_db_common),
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
    payment_method = payment_data.get("pay_method", "wechat")
    if payment_method:
        # 支付方式映射: 1-微信支付, 2-支付宝
        payment_method_map = {
            "wechat": 1,
            "wechatpay": 1,
            "alipay": 2
        }
        order.payment_method = payment_method_map.get(payment_method.lower(), 1)
    
    # 获取产品信息
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="产品不存在")
    
    # 根据支付方式处理
    # 检查是否使用模拟支付（需要明确确认）
    use_mock_payment = payment_data.get("mock_payment", False)
    
    if payment_method == "alipay":
        # 支付宝支付
        if settings.ALIPAY_APP_ID and settings.ALIPAY_PRIVATE_KEY:
            # 有配置支付宝，使用真实支付
            alipay_params = generate_alipay_params(order, product)
            return {"success": True, "code": 200, "message": "支付宝支付", "data": alipay_params}
        else:
            # 没有配置，使用模拟支付
            if use_mock_payment:
                # 用户明确确认使用模拟支付
                process_payment_success(order, db, db_common)
                return {"success": True, "code": 200, "message": "支付成功（模拟）", "data": {"mock": True, "alipay_trade_no": f"MOCK{order.id}{int(time.time())}"}}
            else:
                # 直接使用模拟支付
                alipay_params = generate_alipay_params(order, product)
                process_payment_success(order, db, db_common)
                return {"success": True, "code": 200, "message": "支付成功", "data": alipay_params}
    
    elif payment_method == "wechat" or payment_method == "wechatpay":
        # 微信支付
        if settings.WXPAY_APP_ID and settings.WXPAY_MCH_ID and settings.WXPAY_API_KEY:
            # 有配置微信支付，使用真实支付
            # 先创建预支付订单
            try:
                import httpx
                wechat_params = generate_wechat_pay_params(order, product, current_user)
                
                # 调用微信统一下单接口
                async with httpx.AsyncClient() as client:
                    # 准备下单参数
                    unified_order_params = {
                        "appid": settings.WXPAY_APP_ID,
                        "mch_id": settings.WXPAY_MCH_ID,
                        "nonce_str": wechat_params["nonceStr"],
                        "body": f"双赛道情报通-{product.name}",
                        "out_trade_no": wechat_params["out_trade_no"],
                        "total_fee": int(product.price * 100),
                        "spbill_create_ip": "127.0.0.1",
                        "notify_url": settings.WXPAY_NOTIFY_URL or "http://your-domain.com/api/v1/payments/callback",
                        "trade_type": "JSAPI"
                    }
                    
                    # 生成签名
                    sign_str = "&".join([f"{k}={v}" for k, v in sorted(unified_order_params.items()) if v]) + f"&key={settings.WXPAY_API_KEY}"
                    unified_order_params["sign"] = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
                    
                    # 调用微信下单接口
                    response = await client.post(
                        "https://api.mch.weixin.qq.com/pay/unifiedorder",
                        data=unified_order_params
                    )
                    
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.text)
                    result_code = root.find("result_code").text
                    
                    if result_code == "SUCCESS":
                        prepay_id = root.find("prepay_id").text
                        
                        # 生成支付签名
                        timeStamp = str(int(time.time()))
                        package = f"prepay_id={prepay_id}"
                        pay_sign_str = f"appId={settings.WXPAY_APP_ID}&nonceStr={wechat_params['nonceStr']}&package={package}&signType=MD5&timeStamp={timeStamp}&key={settings.WXPAY_API_KEY}"
                        pay_sign = hashlib.md5(pay_sign_str.encode('utf-8')).hexdigest().upper()
                        
                        return {
                            "success": True,
                            "code": 200,
                            "message": "微信支付",
                            "data": {
                                "timeStamp": timeStamp,
                                "nonceStr": wechat_params["nonceStr"],
                                "package": package,
                                "signType": "MD5",
                                "paySign": pay_sign,
                                "out_trade_no": wechat_params["out_trade_no"]
                            }
                        }
                    else:
                        error_msg = root.find("return_msg").text or root.find("err_code_des").text or "下单失败"
                        log_error(f"微信下单失败: {error_msg}")
                        # 失败后返回提示
                        if use_mock_payment:
                            process_payment_success(order, db, db_common)
                            return {"success": True, "code": 200, "message": "支付成功（模拟）", "data": {"mock": True}}
                        else:
                            return {
                                "success": False, 
                                "code": 400, 
                                "message": f"微信下单失败: {error_msg}，是否使用模拟支付？", 
                                "data": {
                                    "need_confirmation": True,
                                    "mock_payment_available": True
                                }
                            }
                        
            except Exception as e:
                log_error(f"微信支付异常: {str(e)}")
                # 异常时返回提示
                if use_mock_payment:
                    process_payment_success(order, db, db_common)
                    return {"success": True, "code": 200, "message": "支付成功（模拟）", "data": {"mock": True}}
                else:
                    return {
                        "success": False, 
                        "code": 400, 
                        "message": f"微信支付异常: {str(e)}，是否使用模拟支付？", 
                        "data": {
                            "need_confirmation": True,
                            "mock_payment_available": True
                        }
                    }
        else:
            # 没有配置微信支付，返回提示
            if use_mock_payment:
                process_payment_success(order, db, db_common)
                return {"success": True, "code": 200, "message": "支付成功（模拟）", "data": {"mock": True}}
            else:
                return {
                    "success": False, 
                    "code": 400, 
                    "message": "微信支付未配置，是否使用模拟支付？", 
                    "data": {
                        "need_confirmation": True,
                        "mock_payment_available": True
                    }
                }
    
    else:
        # 其他支付方式，返回提示
        if use_mock_payment:
            process_payment_success(order, db, db_common)
            return {"success": True, "code": 200, "message": "支付成功（模拟）", "data": {"mock": True}}
        else:
            return {
                "success": False, 
                "code": 400, 
                "message": "支付方式未配置，是否使用模拟支付？", 
                "data": {
                    "need_confirmation": True,
                    "mock_payment_available": True
                }
            }


@router.post("/callback")
async def payment_callback(
    callback: PaymentCallback,
    db: Session = Depends(get_db),
    db_common: Session = Depends(get_db_common)
):
    """支付回调"""
    # 验证回调签名
    # 这里需要根据实际的支付接口实现
    
    # 更新订单状态
    order = db.query(Order).filter(Order.id == callback.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 调用统一的支付成功处理函数
    process_payment_success(order, db, db_common, callback.transaction_id)
    
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


@router.get("/renewal-options")
async def get_renewal_options(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取续费选项（根据用户当前VIP类型推荐对应产品）"""
    # 检查用户是否已经是VIP
    if not current_user.is_vip_active or not current_user.vip_type:
        raise HTTPException(status_code=400, detail="您尚未开通VIP服务，无法续费")
    
    # 根据用户当前的VIP类型获取对应的产品
    products = db.query(Product).filter(Product.type == current_user.vip_type).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="未找到对应的续费产品")
    
    return {"success": True, "code": 200, "message": "获取续费选项成功", "data": products}


@router.post("/renew")
async def renew_subscription(
    payment_method: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    db_common: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """续费订阅"""
    # 检查用户是否已经是VIP
    if not current_user.is_vip_active or not current_user.vip_type:
        raise HTTPException(status_code=400, detail="您尚未开通VIP服务，无法续费")
    
    # 根据用户当前的VIP类型获取对应的产品
    product = db.query(Product).filter(Product.type == current_user.vip_type).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="未找到对应的续费产品")
    
    # 创建续费订单
    db_order = Order(
        order_no=f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}{current_user.id}{product.id}",
        user_id=current_user.id,
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=1,
        total_amount=product.price,
        payment_method=payment_method,
        payment_status=0,
        user_requirements={},
        created_at=datetime.now()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return JSONResponse(content={
        "success": True,
        "code": 200,
        "message": "续费订单创建成功",
        "data": {
            "id": db_order.id,
            "order_no": db_order.order_no,
            "user_id": db_order.user_id,
            "product_id": db_order.product_id,
            "product_name": db_order.product_name,
            "price": db_order.price,
            "total_amount": db_order.total_amount,
            "payment_method": db_order.payment_method,
            "payment_status": db_order.payment_status,
            "created_at": db_order.created_at.isoformat()
        }
    })


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
                user.user_type = 2
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
                    
                    # 从系统配置中获取邮件文案
                    email_config = db_common.query(SystemConfig).filter(
                        SystemConfig.config_key == f"email_{product.type}"
                    ).first()
                    
                    if email_config and email_config.config_value:
                        email_subject = email_config.description or f"【支付成功】您的{service_type}推送服务已开通"
                        email_content = email_config.config_value
                        # 替换模板变量
                        email_content = email_content.replace("{username}", user.username or "")
                        email_content = email_content.replace("{product_name}", product.name or "")
                        email_content = email_content.replace("{service_type}", service_type or "")
                        email_content = email_content.replace("{start_date}", vip_start_time.strftime('%Y-%m-%d'))
                        email_content = email_content.replace("{end_date}", vip_end_time.strftime('%Y-%m-%d'))
                        email_content = email_content.replace("{duration}", str(product.duration))
                    else:
                        # 使用默认文案
                        email_subject = f"【支付成功】您的{service_type}推送服务已开通"
                        email_content = f"尊敬的 {user.username}：\n\n恭喜您支付成功！您的{service_type}推送服务已开通。\n\n服务详情：\n产品名称：{product.name}\n服务类型：{service_type}推送服务\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n服务时长：{product.duration}天\n\n订阅信息：\n您已成功订阅{service_type}推送服务，我们将为您提供以下内容：\n- 最新{service_type}相关资讯和政策变化\n- 个性化的考试信息推送\n- 专业的备考指导和建议\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                    send_email(user.email, email_subject, email_content)
                    
                    # 记录到推送历史记录
                    try:
                        from core.database import get_db_common
                        from models.users import PushLog
                        from datetime import datetime
                        db_common = next(get_db_common())
                        # 修改推送内容，添加"系统"关键词，确保归类到系统通知
                        push_content = f"【系统通知】您的{service_type}推送服务已开通\n\n服务详情：\n产品名称：{product.name}\n服务类型：{service_type}推送服务\n服务开始时间：{vip_start_time.strftime('%Y-%m-%d')}\n服务结束时间：{vip_end_time.strftime('%Y-%m-%d')}\n服务时长：{product.duration}天\n\n订阅信息：\n您已成功订阅{service_type}推送服务，我们将为您提供以下内容：\n- 最新{service_type}相关资讯和政策变化\n- 个性化的考试信息推送\n- 专业的备考指导和建议\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队"
                        push_log = PushLog(
                            user_id=user.id,
                            info_id=db_order.id,
                            category=3,
                            push_type=3,
                            push_status=1,
                            push_content=push_content,
                            is_processed=1,
                            push_time=datetime.now()
                        )
                        db_common.add(push_log)
                        db_common.commit()
                        db_common.close()
                    except Exception as e:
                        log_error(f"记录推送历史失败: {str(e)}")

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
