from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from core.database import get_db, get_db_kaoyan, get_db_kaogong
from core.security import get_current_admin

from models.users import User, Order, Product, SystemConfig, PushTemplate, PushLog, UserSubscription, UserKeyword, UserReadInfo, UserFavorite, UserLoginRecord
from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog
from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog
from models.sign_in import SignInRecord, PointsRecord
from models.gift import GiftExchange
from models.community import Group, GroupMember, GroupPost, GroupPostComment, Question, Answer, AnswerComment, Like, Report
from models.learning_materials import LearningMaterial, MaterialRating, MaterialComment
from schemas.users import UserResponse, UserUpdate
from schemas.kaoyan import KaoyanInfoResponse, KaoyanCrawlerConfigResponse
from schemas.kaogong import KaogongInfoResponse, KaogongCrawlerConfigResponse
from schemas.payments import OrderResponse, ProductResponse
from schemas.push import PushTemplateResponse, PushLogResponse
from schemas.system import SystemConfigResponse, SystemStatsResponse, SystemConfigBase, SystemConfigCreate, SystemConfigUpdate
from schemas.community import GroupResponse, QuestionResponse, AnswerResponse

router = APIRouter(tags=["admin"])


class SendNotificationRequest(BaseModel):
    """发送通知请求"""
    user_type: int = Field(..., description="用户类型：1-考研用户，2-考公用户，3-全部用户")
    title: str = Field(..., description="通知标题")
    content: str = Field(..., description="通知内容")


@router.get("/notification/history")
async def get_notification_history(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None, description="搜索通知内容")
):
    """获取通知历史记录"""
    try:
        query = db.query(PushLog).filter(PushLog.push_type == 4)
        
        if search:
            query = query.filter(PushLog.push_content.contains(search))
            
        query = query.order_by(PushLog.push_time.desc())
        
        total = query.count()
        offset = (page - 1) * page_size
        history = query.offset(offset).limit(page_size).all()
        
        # 计算每个通知的接收人数
        history_with_count = []
        for log in history:
            # 获取发送给了多少用户（通过内容和时间匹配）
            count = db.query(PushLog).filter(
                PushLog.push_type == 4,
                PushLog.push_content == log.push_content,
                PushLog.push_time == log.push_time
            ).count()
            
            history_with_count.append({
                "id": log.id,
                "title": log.push_content.split("\n")[0],
                "content": log.push_content,
                "send_time": log.push_time.strftime("%Y-%m-%d %H:%M:%S"),
                "receiver_count": count,
                "push_status": log.push_status,
                "category": log.category
            })
            
        return {
            "success": True,
            "code": 200,
            "message": "获取通知历史记录成功",
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": history_with_count
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取通知历史记录失败: {str(e)}")


@router.delete("/notification/history/{history_id}")
async def delete_notification_history(
    history_id: int = Path(..., description="通知历史记录ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除通知历史记录"""
    try:
        log = db.query(PushLog).filter(PushLog.id == history_id, PushLog.push_type == 4).first()
        if not log:
            raise HTTPException(status_code=404, detail="通知历史记录不存在")
            
        # 删除所有内容和时间相同的记录
        db.query(PushLog).filter(
            PushLog.push_type == 4,
            PushLog.push_content == log.push_content,
            PushLog.push_time == log.push_time
        ).delete()
        
        db.commit()
        
        return {
            "success": True,
            "code": 200,
            "message": "删除通知历史记录成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除通知历史记录失败: {str(e)}")


@router.post("/notification/send")
async def send_notification(
    request: SendNotificationRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """给指定类型的用户发送系统通知"""
    try:
        # 获取目标用户
        if request.user_type == 1:
            # 考研用户：已支付考研产品的用户
            query = db.query(User).select_from(User).join(Order, User.id == Order.user_id).join(Product, Order.product_id == Product.id).filter(
                User.is_active == True,
                Order.payment_status == 1,
                Product.type == 1
            ).distinct()
        elif request.user_type == 2:
            # 考公用户：已支付考公产品的用户
            query = db.query(User).select_from(User).join(Order, User.id == Order.user_id).join(Product, Order.product_id == Product.id).filter(
                User.is_active == True,
                Order.payment_status == 1,
                Product.type == 2
            ).distinct()
        elif request.user_type == 3:
            # 全部用户：已支付任何产品的用户
            query = db.query(User).select_from(User).join(Order, User.id == Order.user_id).filter(
                User.is_active == True,
                Order.payment_status == 1
            ).distinct()
        
        target_users = query.all()
        
        # 给每个用户发送通知
        for user in target_users:
            push_log = PushLog(
                user_id=user.id,
                info_id=0,  # 系统通知，无具体信息ID
                category=3,  # 系统通知（默认）
                push_type=4,  # 小程序推送（根据push_manager.py中的注释）
                push_status=1,  # 成功
                push_content=f"{request.title}\n{request.content}",
                is_processed=True,
                push_time=datetime.now(),
                read=False
            )
            db.add(push_log)
        
        db.commit()
        
        return {
            "success": True,
            "code": 200,
            "message": f"成功发送通知给 {len(target_users)} 个用户",
            "data": {"user_count": len(target_users)}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"发送通知失败：{str(e)}")


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    is_admin: Optional[bool] = Query(None),
    is_active: Optional[bool] = Query(None, description="是否今日活跃"),
    keyword: Optional[str] = Query(None, description="搜索关键词（用户名、邮箱、手机号）"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取用户列表（管理员）"""
    query = db.query(User)
    
    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)
    
    # 今日活跃筛选：基于UserLoginRecord
    today = date.today()
    if is_active is not None:
        if is_active:
            active_user_ids = db.query(UserLoginRecord.user_id).filter(
                UserLoginRecord.login_date == today
            ).distinct()
            query = query.filter(User.id.in_(active_user_ids))
        else:
            active_user_ids = db.query(UserLoginRecord.user_id).filter(
                UserLoginRecord.login_date == today
            ).distinct()
            query = query.filter(~User.id.in_(active_user_ids))
    
    # 关键词搜索
    if keyword and keyword.strip():
        query = query.filter(
            (User.username.contains(keyword)) |
            (User.email.contains(keyword)) |
            (User.phone != None, User.phone.contains(keyword))
        )
    
    users = query.offset(skip).limit(limit).all()
    
    # 批量查询今日活跃用户
    today_active_ids = set(
        r[0] for r in db.query(UserLoginRecord.user_id).filter(
            UserLoginRecord.login_date == today
        ).distinct().all()
    )
    
    # 为每个用户添加VIP信息
    for user in users:
        # 动态判断今日是否活跃
        user.is_active = user.id in today_active_ids
        
        # 确保VIP相关字段正确设置
        if hasattr(user, 'is_vip'):
            user.is_vip = user.is_vip
        else:
            user.is_vip = False
            
        if hasattr(user, 'vip_type'):
            user.vip_type = user.vip_type
        else:
            user.vip_type = 0
            
        if hasattr(user, 'vip_start_time'):
            user.vip_start_time = user.vip_start_time
        else:
            user.vip_start_time = None
            
        if hasattr(user, 'vip_end_time'):
            user.vip_end_time = user.vip_end_time
        else:
            user.vip_end_time = None
            
        # 计算登录次数
        login_count = db.query(UserLoginRecord).filter(UserLoginRecord.user_id == user.id).count()
        user.login_count = login_count
    
    return users


@router.get("/orders")
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    payment_status: Optional[int] = Query(None),
    keyword: Optional[str] = Query(None, description="搜索关键词（订单号、用户名、邮箱）"),
    user_id: Optional[int] = Query(None, description="用户ID筛选"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取所有订单列表（管理员）"""
    query = db.query(Order)
    
    if payment_status is not None:
        query = query.filter(Order.payment_status == payment_status)
    
    # 关键词搜索
    if keyword:
        from sqlalchemy.orm import aliased
        UserAlias = aliased(User)
        query = query.join(UserAlias, Order.user_id == UserAlias.id)\
            .filter(
                (Order.order_no.contains(keyword)) |
                (UserAlias.username.contains(keyword)) |
                (UserAlias.email.contains(keyword))
            )
    
    # 用户ID筛选
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    orders = query.offset(skip).limit(limit).all()
    
    # 返回订单信息，包含用户信息
    order_list = []
    for order in orders:
        user = db.query(User).filter(User.id == order.user_id).first()
        order_info = {
            "id": order.id,
            "order_no": order.order_no,
            "user_id": order.user_id,
            "username": user.username if user else "未知用户",
            "email": user.email if user else "未知邮箱",
            "product_id": order.product_id,
            "product_name": order.product_name,
            "price": order.price,
            "quantity": order.quantity,
            "total_amount": order.total_amount,
            "payment_method": order.payment_method,
            "payment_status": order.payment_status,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "payment_time": order.payment_time  # 添加支付时间字段
        }
        order_list.append(order_info)
    
    # 获取总记录数
    total_count = query.count()
    
    return {"success": True, "code": 200, "message": "获取订单列表成功", "data": order_list, "total": total_count}


@router.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取用户详情（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"success": False, "code": 404, "message": "用户不存在", "data": None}
    
    # 添加VIP相关信息
    user.is_vip = user.is_vip
    user.vip_type = user.vip_type
    user.vip_start_time = user.vip_start_time
    user.vip_end_time = user.vip_end_time
    
    return {"success": True, "code": 200, "message": "获取用户信息成功", "data": user}


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新用户信息（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 处理普通字段更新
    update_data = user_update.dict(exclude_unset=True)
    
    # 检查手机号是否重复
    if 'phone' in update_data:
        if not update_data['phone']:
            raise HTTPException(status_code=400, detail="手机号不能为空")
        existing_user = db.query(User).filter(
            User.phone == update_data['phone'],
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="手机号已被其他用户使用")
    
    # 检查邮箱是否重复
    if 'email' in update_data:
        if not update_data['email']:
            raise HTTPException(status_code=400, detail="邮箱不能为空")
        existing_user = db.query(User).filter(
            User.email == update_data['email'],
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已被其他用户使用")
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    # 添加VIP相关信息
    user.is_vip = user.is_vip
    user.vip_type = user.vip_type
    user.vip_start_time = user.vip_start_time
    user.vip_end_time = user.vip_end_time
    
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_admin: User = Depends(get_current_admin)
):
    """删除用户（管理员）"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 防止删除管理员自己
        if user.id == current_admin.id:
            raise HTTPException(status_code=400, detail="不能删除自己")
        
        # 删除用户的订阅配置
        subscriptions = db.query(UserSubscription).filter(UserSubscription.user_id == user_id).all()
        for subscription in subscriptions:
            db.delete(subscription)
        
        # 删除用户的关键词
        keywords = db.query(UserKeyword).filter(UserKeyword.user_id == user_id).all()
        for keyword in keywords:
            db.delete(keyword)
        
        # 删除用户的已读信息
        read_info = db.query(UserReadInfo).filter(UserReadInfo.user_id == user_id).all()
        for info in read_info:
            db.delete(info)
        
        # 删除用户的收藏信息
        favorites = db.query(UserFavorite).filter(UserFavorite.user_id == user_id).all()
        for favorite in favorites:
            db.delete(favorite)
        
        # 保留用户的订单信息
        # 不删除订单，以便后续查询和统计
        
        # 删除用户的推送日志
        push_logs = db.query(PushLog).filter(PushLog.user_id == user_id).all()
        for log in push_logs:
            db.delete(log)
        
        # 删除用户的积分记录
        points_records = db.query(PointsRecord).filter(PointsRecord.user_id == user_id).all()
        for record in points_records:
            db.delete(record)
        
        # 删除用户的签到记录
        sign_in_records = db.query(SignInRecord).filter(SignInRecord.user_id == user_id).all()
        for record in sign_in_records:
            db.delete(record)
        
        # 首先删除用户登录记录（使用查询后删除的方法）
        login_records = db.query(UserLoginRecord).filter(UserLoginRecord.user_id == user_id).all()
        for record in login_records:
            db.delete(record)
        
        # 确保删除操作立即提交（防止外键约束错误）
        db.commit()
        
        # 删除用户的礼品兑换记录
        db.query(GiftExchange).filter(GiftExchange.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的学习资料评分记录
        db.query(LearningMaterialRating).filter(LearningMaterialRating.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的学习资料评论记录
        db.query(LearningMaterialComment).filter(LearningMaterialComment.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的学习资料记录
        db.query(LearningMaterial).filter(LearningMaterial.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区评论记录
        db.query(GroupPostComment).filter(GroupPostComment.user_id == user_id).delete(synchronize_session=False)
        db.query(AnswerComment).filter(AnswerComment.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区点赞记录
        db.query(Like).filter(Like.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区举报记录
        db.query(Report).filter(Report.reporter_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区小组消息记录
        db.query(GroupMessage).filter(GroupMessage.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区成员记录
        db.query(GroupMember).filter(GroupMember.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户的社区话题记录
        db.query(GroupPost).filter(GroupPost.user_id == user_id).delete(synchronize_session=False)
        db.query(Question).filter(Question.user_id == user_id).delete(synchronize_session=False)
        db.query(Answer).filter(Answer.user_id == user_id).delete(synchronize_session=False)
        
        # 删除用户
        db.delete(user)
        db.commit()
        
        return {"message": "用户删除成功"}
    except Exception as e:
        db.rollback()
        db_kaoyan.rollback()
        db_kaogong.rollback()
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"删除用户失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除用户失败，请稍后重试")


@router.get("/users/{user_id}/requirements")
async def get_user_requirements(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取用户需求配置（管理员）"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 初始化需求结果
        requirements = {
            'kaoyan': {},
            'kaogong': {},
            'push': {}
        }
        
        # 获取用户的订阅配置
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.info(f"获取用户订阅配置: user_id={user_id}")
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).first()
        logger.info(f"subscription: {subscription}")
        
        # 处理订阅配置
        if subscription:
            # 确保subscription.config_json不是None
            from core.logger import get_logger
            logger = get_logger(__name__)
            logger.info(f"subscription: {subscription}")
            logger.info(f"hasattr(subscription, 'config_json'): {hasattr(subscription, 'config_json')}")
            if hasattr(subscription, 'config_json'):
                config_json = subscription.config_json
                logger.info(f"config_json: {config_json}")
                logger.info(f"type(config_json): {type(config_json)}")
                # 确保config_json不是None
                if config_json is not None:
                    # 如果config_json是字符串，解析它
                    if isinstance(config_json, str):
                        try:
                            import json
                            config_json = json.loads(config_json)
                            # 确保解析后不是None
                            if config_json is None:
                                config_json = {}
                        except:
                            config_json = {}
                    # 确保config_json是字典
                    if isinstance(config_json, dict):
                        logger.info(f"config_json is dict: {config_json}")
                        # 处理考研需求 - 支持两种数据结构
                        if 'kaoyan' in config_json:
                            kaoyan_config = config_json['kaoyan']
                            logger.info(f"kaoyan_config: {kaoyan_config}")
                            logger.info(f"type(kaoyan_config): {type(kaoyan_config)}")
                            if kaoyan_config is not None and isinstance(kaoyan_config, dict):
                                requirements['kaoyan'] = kaoyan_config
                                logger.info(f"requirements['kaoyan']: {requirements['kaoyan']}")
                        elif 'kaoyan_requirements' in config_json:
                            kaoyan_config = config_json['kaoyan_requirements']
                            if kaoyan_config is not None and isinstance(kaoyan_config, dict):
                                requirements['kaoyan'] = kaoyan_config
                        # 处理考公需求 - 支持两种数据结构
                        if 'kaogong' in config_json:
                            kaogong_config = config_json['kaogong']
                            if kaogong_config is not None and isinstance(kaogong_config, dict):
                                requirements['kaogong'] = kaogong_config
                        elif 'kaogong_requirements' in config_json:
                            kaogong_config = config_json['kaogong_requirements']
                            if kaogong_config is not None and isinstance(kaogong_config, dict):
                                requirements['kaogong'] = kaogong_config
                        # 处理推送设置
                        if 'push' in config_json:
                            push_config = config_json['push']
                            if push_config is not None and isinstance(push_config, dict):
                                requirements['push'] = push_config
        
        # 获取用户的关键词
        keywords = db.query(UserKeyword).filter(
            UserKeyword.user_id == user_id,
            UserKeyword.is_active == True
        ).all()
        
        # 处理关键词 - 只在订阅配置中没有关键词时添加
        for kw in keywords:
            category = 'kaoyan' if kw.category == 1 else 'kaogong'
            if 'keywords' not in requirements[category] or not requirements[category]['keywords']:
                if 'keywords' not in requirements[category]:
                    requirements[category]['keywords'] = []
                requirements[category]['keywords'].append(kw.keyword)
        
        return requirements
    except Exception as e:
        db.rollback()
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"获取用户需求失败: {str(e)}")
        import traceback
        logger.error(f"堆栈信息: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="获取用户需求失败，请稍后重试")


@router.put("/users/{user_id}/requirements")
async def update_user_requirements(
    user_id: int = Path(..., ge=1),
    requirements: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新用户需求配置（管理员）"""
    try:
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.info(f"更新用户需求: user_id={user_id}, requirements={requirements}")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 获取用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).first()
        
        if not subscription:
            # 如果没有订阅配置，创建一个
            logger.info(f"创建新的订阅配置: user_id={user_id}")
            subscription = UserSubscription(
                user_id=user_id,
                subscribe_type=3,
                status=1,
                config_json={}
            )
            db.add(subscription)
            db.flush()
        
        # 直接使用前端传递的数据，不做任何转换
        subscription.config_json = requirements
        
        logger.info(f"设置config_json为: {subscription.config_json}")
        
        # 更新用户关键词
        # 先删除旧的关键词
        db.query(UserKeyword).filter(UserKeyword.user_id == user_id).delete()
        
        # 添加新的关键词
        if 'kaoyan' in requirements and 'keywords' in requirements['kaoyan']:
            kaoyan_keywords = requirements['kaoyan']['keywords']
            if kaoyan_keywords:
                if isinstance(kaoyan_keywords, str):
                    kaoyan_keywords = [k.strip() for k in kaoyan_keywords.split(',') if k.strip()]
                # 去重
                unique_kaoyan_keywords = list(set(kaoyan_keywords))
                for keyword in unique_kaoyan_keywords:
                    db.add(UserKeyword(
                        user_id=user_id,
                        keyword=keyword,
                        category=1,
                        is_active=True
                    ))
        
        if 'kaogong' in requirements and 'keywords' in requirements['kaogong']:
            kaogong_keywords = requirements['kaogong']['keywords']
            if kaogong_keywords:
                if isinstance(kaogong_keywords, str):
                    kaogong_keywords = [k.strip() for k in kaogong_keywords.split(',') if k.strip()]
                # 去重
                unique_kaogong_keywords = list(set(kaogong_keywords))
                for keyword in unique_kaogong_keywords:
                    db.add(UserKeyword(
                        user_id=user_id,
                        keyword=keyword,
                        category=2,
                        is_active=True
                    ))
        
        db.commit()
        db.refresh(subscription)
        
        logger.info(f"用户需求更新成功: user_id={user_id}")
        
        return {"message": "用户需求更新成功"}
    except Exception as e:
        db.rollback()
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"更新用户需求失败: {str(e)}")
        import traceback
        logger.error(f"堆栈信息: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="更新用户需求失败，请稍后重试")


@router.get("/kaoyan/info", response_model=List[KaoyanInfoResponse])
async def get_kaoyan_info(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    province: Optional[str] = Query(None),
    school: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    current_admin: User = Depends(get_current_admin)
):
    """获取考研信息列表（管理员）"""
    query = db_kaoyan.query(KaoyanInfo)
    
    if province:
        query = query.filter(KaoyanInfo.province == province)
    if school:
        query = query.filter(KaoyanInfo.school == school)
    if category:
        query = query.filter(KaoyanInfo.category == category)
    
    info_list = query.offset(skip).limit(limit).all()
    return info_list


@router.get("/kaogong/info", response_model=List[KaogongInfoResponse])
async def get_kaogong_info(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    province: Optional[str] = Query(None),
    position_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_admin: User = Depends(get_current_admin)
):
    """获取考公信息列表（管理员）"""
    query = db_kaogong.query(KaogongInfo)
    
    if province:
        query = query.filter(KaogongInfo.province == province)
    if position_type:
        query = query.filter(KaogongInfo.position_type == position_type)
    if category:
        query = query.filter(KaogongInfo.category == category)
    
    info_list = query.offset(skip).limit(limit).all()
    return info_list


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取系统统计信息（管理员）"""
    from core.database import get_db_kaoyan, get_db_kaogong
    
    # 手动获取其他数据库会话
    db_kaoyan = next(get_db_kaoyan())
    db_kaogong = next(get_db_kaogong())
    
    try:
        # 计算用户数
        user_count = db.query(User).count()
        
        # 计算考研信息数
        kaoyan_count = db_kaoyan.query(KaoyanInfo).count()
        
        # 计算考公信息数
        kaogong_count = db_kaogong.query(KaogongInfo).count()
        
        # 计算订单数
        order_count = db.query(Order).count()
        
        # 计算推送数
        push_count = db.query(PushLog).count()
        
        # 计算用户类型分布
        user_type_distribution = {
            "考研": 0,
            "考公": 0,
            "双赛道": 0
        }
        
        # 获取所有用户
        users = db.query(User).all()
        
        for user in users:
            # 获取用户的订阅配置（状态为1的有效订阅）
            subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == user.id,
                UserSubscription.status == 1
            ).first()
            
            if subscription:
                if subscription.subscribe_type == 1:
                    user_type_distribution["考研"] += 1
                elif subscription.subscribe_type == 2:
                    user_type_distribution["考公"] += 1
                elif subscription.subscribe_type == 3:
                    user_type_distribution["双赛道"] += 1
        
        # 积分分布统计
        points_distribution = {
            "0分": 0,
            "1-50分": 0,
            "51-100分": 0,
            "101-200分": 0,
            "201-500分": 0,
            "500分以上": 0
        }
        for user in users:
            points = user.points or 0
            if points == 0:
                points_distribution["0分"] += 1
            elif points <= 50:
                points_distribution["1-50分"] += 1
            elif points <= 100:
                points_distribution["51-100分"] += 1
            elif points <= 200:
                points_distribution["101-200分"] += 1
            elif points <= 500:
                points_distribution["201-500分"] += 1
            else:
                points_distribution["500分以上"] += 1
        
        # VIP用户分布
        vip_distribution = {
            "普通用户": 0,
            "考研VIP": 0,
            "考公VIP": 0,
            "双赛道VIP": 0
        }
        for user in users:
            if not user.is_vip:
                vip_distribution["普通用户"] += 1
            elif user.vip_type == 1:
                vip_distribution["考研VIP"] += 1
            elif user.vip_type == 2:
                vip_distribution["考公VIP"] += 1
            elif user.vip_type == 3:
                vip_distribution["双赛道VIP"] += 1
            else:
                vip_distribution["普通用户"] += 1
        
        # 最近7天用户注册趋势
        from datetime import timedelta
        user_growth_trend = []
        for i in range(6, -1, -1):
            day = date.today() - timedelta(days=i)
            count = db.query(User).filter(
                User.created_at >= datetime.combine(day, datetime.min.time()),
                User.created_at < datetime.combine(day + timedelta(days=1), datetime.min.time())
            ).count()
            user_growth_trend.append({
                "date": day.strftime("%m-%d"),
                "count": count
            })
        
        return {
            "user_count": user_count,
            "kaoyan_count": kaoyan_count,
            "kaogong_count": kaogong_count,
            "order_count": order_count,
            "push_count": push_count,
            "user_type_distribution": user_type_distribution,
            "points_distribution": points_distribution,
            "vip_distribution": vip_distribution,
            "user_growth_trend": user_growth_trend,
            "timestamp": datetime.utcnow()
        }
    finally:
        # 关闭手动创建的会话
        db_kaoyan.close()
        db_kaogong.close()


@router.get("/configs", response_model=List[SystemConfigResponse])
async def get_system_configs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取系统配置列表（管理员）"""
    query = db.query(SystemConfig)
    
    if is_active is not None:
        query = query.filter(SystemConfig.status == (1 if is_active else 0))
    
    configs = query.offset(skip).limit(limit).all()
    
    # 转换为 SystemConfigResponse 格式
    result = []
    for config in configs:
        result.append(SystemConfigResponse(
            id=config.id,
            key=config.config_key,
            value=config.config_value,
            description=config.description,
            is_active=config.status == 1,
            created_at=config.created_at,
            updated_at=config.updated_at
        ))
    
    return result


@router.get("/configs/{config_id}", response_model=SystemConfigResponse)
async def get_system_config(
    config_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取系统配置详情（管理员）"""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    # 转换为 SystemConfigResponse 格式
    return SystemConfigResponse(
        id=config.id,
        key=config.config_key,
        value=config.config_value,
        description=config.description,
        is_active=config.status == 1,
        created_at=config.created_at,
        updated_at=config.updated_at
    )


@router.post("/configs", response_model=SystemConfigResponse)
async def create_system_config(
    config_create: SystemConfigBase = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """创建系统配置（管理员）"""
    # 检查键是否已存在
    existing_config = db.query(SystemConfig).filter(SystemConfig.config_key == config_create.key).first()
    if existing_config:
        raise HTTPException(status_code=400, detail="配置键已存在")
    
    # 创建新配置
    config = SystemConfig(
        config_key=config_create.key,
        config_value=config_create.value,
        description=config_create.description,
        status=1 if config_create.is_active else 0
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    
    # 转换为 SystemConfigResponse 格式
    return SystemConfigResponse(
        id=config.id,
        key=config.config_key,
        value=config.config_value,
        description=config.description,
        is_active=config.status == 1,
        created_at=config.created_at,
        updated_at=config.updated_at
    )


@router.put("/configs/{config_id}", response_model=SystemConfigResponse)
async def update_system_config(
    config_id: int = Path(..., ge=1),
    config_update: SystemConfigUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新系统配置（管理员）"""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    # 更新字段
    if config_update.value:
        config.config_value = config_update.value
    if config_update.description:
        config.description = config_update.description
    if config_update.is_active is not None:
        config.status = 1 if config_update.is_active else 0
    
    db.commit()
    db.refresh(config)
    
    # 转换为 SystemConfigResponse 格式
    return SystemConfigResponse(
        id=config.id,
        key=config.config_key,
        value=config.config_value,
        description=config.description,
        is_active=config.status == 1,
        created_at=config.created_at,
        updated_at=config.updated_at
    )


@router.delete("/configs/{config_id}")
async def delete_system_config(
    config_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除系统配置（管理员）"""
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    db.delete(config)
    db.commit()
    
    return {"message": "系统配置删除成功"}


@router.get("/student-crawlers")
async def get_student_crawlers(
    db: Session = Depends(get_db),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_admin: User = Depends(get_current_admin)
):
    """获取按学生分类的爬虫数据（管理员）"""
    from core.logger import get_logger
    logger = get_logger(__name__)
    
    # 获取所有非admin用户
    users = db.query(User).filter(User.is_admin == False).all()
    
    student_crawlers_list = []
    
    for user in users:
        # 获取用户的订阅配置（不限制状态，只要存在就获取）
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id
        ).all()
        
        logger.info(f"用户 {user.id} ({user.username}) 的订阅数量: {len(subscriptions)}")
        for sub in subscriptions:
            logger.info(f"  订阅 ID: {sub.id}, 类型: {sub.subscribe_type}, 状态: {sub.status}")
        
        # 收集用户的爬虫配置
        user_crawlers = []
        
        # 从数据库中获取爬虫配置
        from models.kaoyan import KaoyanCrawlerConfig
        from models.kaogong import KaogongCrawlerConfig
        
        # 获取考研爬虫配置（筛选属于该用户的）
        kaoyan_configs = db_kaoyan.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.user_id == user.id
        ).all()
        
        for config in kaoyan_configs:
            crawler = {
                'id': len(user_crawlers) + 1,
                'name': config.name,
                'url': config.url
            }
            user_crawlers.append(crawler)
        
        # 获取考公爬虫配置（筛选属于该用户的）
        kaogong_configs = db_kaogong.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.user_id == user.id
        ).all()
        
        for config in kaogong_configs:
            crawler = {
                'id': len(user_crawlers) + 1,
                'name': config.name,
                'url': config.url
            }
            user_crawlers.append(crawler)
        
        # 添加用户类型信息（和用户管理接口保持一致的逻辑）
        user_type = "未订阅"
        # 查询用户的订阅配置（只查询状态为1的）
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        logger.info(f"用户 {user.id} ({user.username}) 的有效订阅: {subscription}")
        
        if subscription:
            if subscription.subscribe_type == 1:
                user_type = "考研"
            elif subscription.subscribe_type == 2:
                user_type = "考公"
            elif subscription.subscribe_type == 3:
                user_type = "双赛道"
        
        logger.info(f"用户 {user.id} ({user.username}) 的最终用户类型: {user_type}")
        
        # 添加学生爬虫数据
        student_crawlers_list.append({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user_type,
            'crawlers': user_crawlers,
            'is_active_today': db.query(UserLoginRecord).filter(
                UserLoginRecord.user_id == user.id,
                UserLoginRecord.login_date == date.today()
            ).first() is not None
        })
    
    return student_crawlers_list


@router.get("/student-websites")
async def get_student_websites(
    db: Session = Depends(get_db),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_admin: User = Depends(get_current_admin)
):
    """获取按学生分类的网站数据（管理员）"""
    from core.logger import get_logger
    logger = get_logger(__name__)
    
    # 获取所有非admin用户
    users = db.query(User).filter(User.is_admin == False).all()
    
    student_websites_list = []
    
    for user in users:
        # 获取用户的订阅配置（不限制状态，只要存在就获取）
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id
        ).all()
        
        logger.info(f"用户 {user.id} ({user.username}) 的订阅数量: {len(subscriptions)}")
        for sub in subscriptions:
            logger.info(f"  订阅 ID: {sub.id}, 类型: {sub.subscribe_type}, 状态: {sub.status}")
        
        # 收集用户的网站配置
        user_websites = []
        
        # 从数据库中获取爬虫配置（网站配置）
        from models.kaoyan import KaoyanCrawlerConfig
        from models.kaogong import KaogongCrawlerConfig
        
        # 获取考研网站配置（筛选属于该用户的）
        kaoyan_configs = db_kaoyan.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.user_id == user.id
        ).all()
        
        for config in kaoyan_configs:
            website = {
                'id': len(user_websites) + 1,
                'name': config.name,
                'url': config.url
            }
            user_websites.append(website)
        
        # 获取考公网站配置（筛选属于该用户的）
        kaogong_configs = db_kaogong.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.user_id == user.id
        ).all()
        
        for config in kaogong_configs:
            website = {
                'id': len(user_websites) + 1,
                'name': config.name,
                'url': config.url
            }
            user_websites.append(website)
        
        # 添加用户类型信息（和用户管理接口保持一致的逻辑）
        user_type = "未订阅"
        # 查询用户的订阅配置（只查询状态为1的）
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        logger.info(f"用户 {user.id} ({user.username}) 的有效订阅: {subscription}")
        
        if subscription:
            if subscription.subscribe_type == 1:
                user_type = "考研"
            elif subscription.subscribe_type == 2:
                user_type = "考公"
            elif subscription.subscribe_type == 3:
                user_type = "双赛道"
        
        logger.info(f"用户 {user.id} ({user.username}) 的最终用户类型: {user_type}")
        
        # 添加学生网站数据
        student_websites_list.append({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user_type,
            'websites': user_websites,
            'is_active_today': db.query(UserLoginRecord).filter(
                UserLoginRecord.user_id == user.id,
                UserLoginRecord.login_date == date.today()
            ).first() is not None
        })
    
    return student_websites_list


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    keyword: Optional[str] = Query(None),
    type: Optional[int] = Query(None),
    status: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取产品列表（管理员）"""
    query = db.query(Product)
    
    if keyword:
        query = query.filter(Product.name.contains(keyword))
    if type:
        query = query.filter(Product.type == type)
    if status:
        query = query.filter(Product.status == status)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取产品详情（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """创建产品（管理员）"""
    # 检查产品名称是否已存在
    existing_product = db.query(Product).filter(Product.name == product.get("name")).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="产品名称已存在")
    
    db_product = Product(**product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product: dict = Body(...),
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新产品（管理员）"""
    from core.logger import get_logger
    logger = get_logger(__name__)
    
    logger.info(f"更新产品请求: product_id={product_id}, data={product}")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        logger.error(f"产品不存在: product_id={product_id}")
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 检查产品名称是否已被其他产品使用
    if "name" in product and product["name"] != db_product.name:
        existing_product = db.query(Product).filter(Product.name == product["name"], Product.id != product_id).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="产品名称已存在")
    
    # 记录更新前的状态
    logger.info(f"更新前状态: product_id={product_id}, status={db_product.status}")
    
    for key, value in product.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    
    # 记录更新后的状态
    logger.info(f"更新后状态: product_id={product_id}, status={db_product.status}")
    
    return db_product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除产品（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    
    # 检查是否有关联的订单
    orders = db.query(Order).filter(Order.product_id == product_id).count()
    if orders > 0:
        raise HTTPException(status_code=400, detail="该产品已被订单使用，无法删除")
    
    db.delete(product)
    db.commit()
    return {"message": "产品删除成功"}


@router.delete("/products")
async def delete_all_products(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除所有产品（管理员）"""
    # 检查是否有关联的订单
    products_with_orders = db.query(Product).join(Order, Product.id == Order.product_id).distinct().all()
    if products_with_orders:
        product_names = [product.name for product in products_with_orders]
        raise HTTPException(status_code=400, detail=f"以下产品已被订单使用，无法删除: {', '.join(product_names)}")
    
    # 删除所有产品
    db.query(Product).delete()
    db.commit()
    return {"message": "所有产品删除成功"}


@router.get("/sign-in/records")
async def get_sign_in_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取签到记录列表（管理员）- 排除管理员"""
    from fastapi.responses import JSONResponse
    from sqlalchemy import desc
    from datetime import datetime as dt
    
    query = db.query(SignInRecord).join(User).filter(User.is_admin == False)
    
    if user_id:
        query = query.filter(SignInRecord.user_id == user_id)
    
    if start_date:
        try:
            start = dt.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(SignInRecord.sign_date >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = dt.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(SignInRecord.sign_date <= end)
        except ValueError:
            pass
    
    query = query.order_by(desc(SignInRecord.sign_date))
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for item in items:
        user = db.query(User).filter(User.id == item.user_id).first()
        result.append({
            "id": item.id,
            "user_id": item.user_id,
            "username": user.username if user else "未知用户",
            "sign_date": item.sign_date.isoformat() if item.sign_date else None,
            "points_earned": item.points_earned,
            "continuous_days": item.continuous_days,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": "获取签到记录成功",
            "data": {
                "total": total,
                "items": result,
                "page": page,
                "page_size": page_size
            }
        }
    )


@router.get("/points/records")
async def get_points_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    type: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取积分记录列表（管理员）- 排除管理员"""
    from fastapi.responses import JSONResponse
    from sqlalchemy import desc
    
    query = db.query(PointsRecord).join(User).filter(User.is_admin == False)
    
    if user_id:
        query = query.filter(PointsRecord.user_id == user_id)
    
    if type:
        query = query.filter(PointsRecord.type == type)
    
    query = query.order_by(desc(PointsRecord.created_at))
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    type_names = {1: "签到", 2: "兑换", 3: "系统赠送", 4: "消费", 5: "其他"}
    
    result = []
    for item in items:
        user = db.query(User).filter(User.id == item.user_id).first()
        result.append({
            "id": item.id,
            "user_id": item.user_id,
            "username": user.username if user else "未知用户",
            "points": item.points,
            "balance": item.balance,
            "type": item.type,
            "type_name": type_names.get(item.type, "未知"),
            "description": item.description,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": "获取积分记录成功",
            "data": {
                "total": total,
                "items": result,
                "page": page,
                "page_size": page_size
            }
        }
    )


@router.get("/sign-in/stats")
async def get_sign_in_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取签到统计（管理员）- 排除管理员"""
    from fastapi.responses import JSONResponse
    from datetime import date, timedelta
    from sqlalchemy import and_
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    today_count = db.query(SignInRecord).join(User).filter(
        and_(SignInRecord.sign_date == today, User.is_admin == False)
    ).count()
    
    yesterday_count = db.query(SignInRecord).join(User).filter(
        and_(SignInRecord.sign_date == yesterday, User.is_admin == False)
    ).count()
    
    total_count = db.query(SignInRecord).join(User).filter(
        User.is_admin == False
    ).count()
    
    total_points = db.query(User).filter(User.is_admin == False).all()
    total_points_sum = sum(u.points or 0 for u in total_points)
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": "获取签到统计成功",
            "data": {
                "today_count": today_count,
                "yesterday_count": yesterday_count,
                "total_count": total_count,
                "total_points": total_points_sum
            }
        }
    )


@router.get("/community/groups")
async def get_community_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取社区小组列表（管理员）"""
    query = db.query(Group)
    
    if status is not None:
        query = query.filter(Group.status == status)
    
    if search:
        query = query.filter(Group.name.contains(search))
    
    groups = query.offset(skip).limit(limit).all()
    
    # 实时计算成员数
    result = []
    for group in groups:
        member_count = db.query(GroupMember).filter(
            GroupMember.group_id == group.id,
            GroupMember.status == 1
        ).count()
        
        group_data = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "avatar": group.avatar,
            "cover": group.cover,
            "creator_id": group.creator_id,
            "join_type": group.join_type,
            "status": group.status,
            "member_count": member_count,
            "tags": group.tags,
            "created_at": group.created_at.isoformat() if group.created_at else None,
            "updated_at": group.updated_at.isoformat() if group.updated_at else None
        }
        result.append(group_data)
    
    return result


class StatusUpdate(BaseModel):
    status: int = Field(..., ge=0, le=1, description="状态: 0-禁用, 1-正常")


@router.put("/community/groups/{group_id}/status")
async def update_group_status(
    group_id: int = Path(..., ge=1),
    update_data: StatusUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新小组状态（管理员）"""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    group.status = update_data.status
    db.commit()
    db.refresh(group)
    return {"success": True, "message": "状态更新成功"}


@router.delete("/community/groups/{group_id}")
async def delete_group(
    group_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除小组（管理员）"""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 先删除关联的成员记录
    db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()
    
    # 再删除小组
    db.delete(group)
    db.commit()
    return {"success": True, "message": "删除成功"}


@router.get("/community/questions", response_model=List[QuestionResponse])
async def get_community_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取社区问题列表（管理员）"""
    query = db.query(Question)
    
    if status is not None:
        query = query.filter(Question.status == status)
    if category:
        query = query.filter(Question.category == category)
    if search:
        query = query.filter(Question.title.contains(search))
    
    questions = query.offset(skip).limit(limit).all()
    return questions


@router.put("/community/questions/{question_id}/approve")
async def approve_question(
    question_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """审核通过问题（管理员）"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    question.status = 1
    db.commit()
    db.refresh(question)
    return {"success": True, "message": "审核通过"}


@router.put("/community/questions/{question_id}/reject")
async def reject_question(
    question_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """拒绝问题（管理员）"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    question.status = 2
    db.commit()
    db.refresh(question)
    return {"success": True, "message": "已拒绝"}


@router.delete("/community/questions/{question_id}")
async def delete_question(
    question_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除问题（管理员）"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    db.delete(question)
    db.commit()
    return {"success": True, "message": "删除成功"}


@router.get("/community/answers", response_model=List[AnswerResponse])
async def get_community_answers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[int] = Query(None),
    question_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取社区回答列表（管理员）"""
    query = db.query(Answer)
    
    if status is not None:
        query = query.filter(Answer.status == status)
    if question_id:
        query = query.filter(Answer.question_id == question_id)
    
    answers = query.offset(skip).limit(limit).all()
    return answers


@router.get("/community/reports")
async def get_community_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[int] = Query(None),
    target_type: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取社区举报列表（管理员）"""
    query = db.query(Report)
    
    if status is not None:
        query = query.filter(Report.status == status)
    if target_type is not None:
        query = query.filter(Report.target_type == target_type)
    
    reports = query.offset(skip).limit(limit).all()
    
    # 构建返回数据
    result = []
    for report in reports:
        # 获取举报者信息
        reporter = db.query(User).filter(User.id == report.reporter_id).first()
        # 获取处理者信息
        handler = db.query(User).filter(User.id == report.handler_id).first()
        
        report_info = {
            "id": report.id,
            "reporter_id": report.reporter_id,
            "reporter_name": reporter.username if reporter else "未知用户",
            "target_type": report.target_type,
            "target_id": report.target_id,
            "reason": report.reason,
            "status": report.status,
            "handler_id": report.handler_id,
            "handler_name": handler.username if handler else None,
            "handle_time": report.handle_time,
            "handle_note": report.handle_note,
            "created_at": report.created_at
        }
        result.append(report_info)
    
    return result


@router.put("/community/reports/{report_id}")
async def handle_community_report(
    report_id: int = Path(..., ge=1),
    status: int = Body(..., ge=0, le=2, description="处理状态: 0-待处理, 1-已处理, 2-已驳回"),
    handler_note: Optional[str] = Body(None, description="处理备注"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """处理社区举报（管理员）"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="举报不存在")
    
    # 更新举报状态
    report.status = status
    report.handler_id = current_admin.id
    report.handle_time = datetime.now()
    if handler_note:
        report.handle_note = handler_note
    
    db.commit()
    db.refresh(report)
    
    return {"success": True, "message": "举报处理成功"}


# ==================== 每日一练管理 ====================

from models.learning_materials import DailyPractice
import json

class DailyPracticeCreate(BaseModel):
    category: str = Field(..., description="题目分类")
    question: str = Field(..., description="题目内容")
    options: str = Field(..., description="选项JSON")
    answer: str = Field(..., description="正确答案")
    analysis: str = Field(None, description="答案解析")
    difficulty: int = Field(1, description="难度")
    is_active: bool = Field(True, description="是否启用")
    show_date: datetime = Field(None, description="指定显示日期")

class DailyPracticeUpdate(BaseModel):
    category: str = Field(None, description="题目分类")
    question: str = Field(None, description="题目内容")
    options: str = Field(None, description="选项JSON")
    answer: str = Field(None, description="正确答案")
    analysis: str = Field(None, description="答案解析")
    difficulty: int = Field(None, description="难度")
    is_active: bool = Field(None, description="是否启用")
    show_date: datetime = Field(None, description="指定显示日期")

class DailyPracticeResponse(BaseModel):
    id: int
    category: str
    question: str
    options: str
    answer: str
    analysis: str = None
    difficulty: int
    is_active: bool
    show_date: datetime = None
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/daily-practices")
async def get_daily_practices(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str = Query(None, description="题目分类"),
    is_active: bool = Query(None, description="是否启用")
):
    """获取每日一练列表"""
    query = db.query(DailyPractice)
    
    if category:
        query = query.filter(DailyPractice.category == category)
    if is_active is not None:
        query = query.filter(DailyPractice.is_active == is_active)
    
    query = query.order_by(DailyPractice.created_at.desc())
    total = query.count()
    practices = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "code": 200,
        "message": "获取每日一练列表成功",
        "data": practices,
        "total": total
    }

@router.post("/daily-practices", response_model=DailyPracticeResponse)
async def create_daily_practice(
    practice_data: DailyPracticeCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """创建每日一练题目"""
    try:
        json.loads(practice_data.options)
    except:
        raise HTTPException(status_code=400, detail="选项格式错误，必须是有效的JSON")
    
    practice = DailyPractice(
        category=practice_data.category,
        question=practice_data.question,
        options=practice_data.options,
        answer=practice_data.answer,
        analysis=practice_data.analysis,
        difficulty=practice_data.difficulty,
        is_active=practice_data.is_active,
        show_date=practice_data.show_date
    )
    
    db.add(practice)
    db.commit()
    db.refresh(practice)
    
    return practice

@router.put("/daily-practices/{practice_id}", response_model=DailyPracticeResponse)
async def update_daily_practice(
    practice_id: int = Path(..., description="题目ID"),
    practice_data: DailyPracticeUpdate = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新每日一练题目"""
    practice = db.query(DailyPractice).filter(DailyPractice.id == practice_id).first()
    if not practice:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    if practice_data.category is not None:
        practice.category = practice_data.category
    if practice_data.question is not None:
        practice.question = practice_data.question
    if practice_data.options is not None:
        try:
            json.loads(practice_data.options)
        except:
            raise HTTPException(status_code=400, detail="选项格式错误，必须是有效的JSON")
        practice.options = practice_data.options
    if practice_data.answer is not None:
        practice.answer = practice_data.answer
    if practice_data.analysis is not None:
        practice.analysis = practice_data.analysis
    if practice_data.difficulty is not None:
        practice.difficulty = practice_data.difficulty
    if practice_data.is_active is not None:
        practice.is_active = practice_data.is_active
    if practice_data.show_date is not None:
        practice.show_date = practice_data.show_date
    
    db.commit()
    db.refresh(practice)
    
    return practice

@router.delete("/daily-practices/{practice_id}")
async def delete_daily_practice(
    practice_id: int = Path(..., description="题目ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除每日一练题目"""
    practice = db.query(DailyPractice).filter(DailyPractice.id == practice_id).first()
    if not practice:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    # 先删除关联的答题记录
    from models.learning_materials import DailyPracticeRecord
    db.query(DailyPracticeRecord).filter(DailyPracticeRecord.practice_id == practice_id).delete()
    # 再删除题目
    db.delete(practice)
    db.commit()
    
    return {"success": True, "message": "删除成功"}

@router.get("/daily-practices/categories")
async def get_practice_categories(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取题目分类列表"""
    categories = db.query(DailyPractice.category).distinct().all()
    return [c[0] for c in categories]

@router.get("/daily-practices/{practice_id}", response_model=DailyPracticeResponse)
async def get_daily_practice(
    practice_id: int = Path(..., description="题目ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取单个每日一练题目"""
    practice = db.query(DailyPractice).filter(DailyPractice.id == practice_id).first()
    if not practice:
        raise HTTPException(status_code=404, detail="题目不存在")
    return practice


# ==================== 热点管理 ====================

from models.learning_materials import HotTopic

class HotTopicCreate(BaseModel):
    title: str = Field(..., description="热点标题")
    content: str = Field(None, description="热点内容")
    cover_image: str = Field(None, description="封面图片URL")
    link_url: str = Field(None, description="跳转链接URL")
    category: str = Field(None, description="分类: 考研/考公/通用")
    source: str = Field(None, description="来源")
    sort_order: int = Field(0, description="排序顺序")
    is_active: bool = Field(True, description="是否启用")
    publish_time: datetime = Field(None, description="发布时间")

class HotTopicUpdate(BaseModel):
    title: str = Field(None, description="热点标题")
    content: str = Field(None, description="热点内容")
    cover_image: str = Field(None, description="封面图片URL")
    link_url: str = Field(None, description="跳转链接URL")
    category: str = Field(None, description="分类: 考研/考公/通用")
    source: str = Field(None, description="来源")
    sort_order: int = Field(None, description="排序顺序")
    is_active: bool = Field(None, description="是否启用")
    publish_time: datetime = Field(None, description="发布时间")

class HotTopicResponse(BaseModel):
    id: int
    title: str
    content: str = None
    cover_image: str = None
    link_url: str = None
    category: str = None
    source: str = None
    views: int
    sort_order: int
    is_active: bool
    publish_time: datetime = None
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/hot-topics")
async def get_hot_topics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: str = Query(None, description="分类"),
    is_active: bool = Query(None, description="是否启用")
):
    """获取热点列表"""
    query = db.query(HotTopic)
    
    if category:
        query = query.filter(HotTopic.category == category)
    if is_active is not None:
        query = query.filter(HotTopic.is_active == is_active)
    
    query = query.order_by(HotTopic.sort_order.desc(), HotTopic.created_at.desc())
    total = query.count()
    topics = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "code": 200,
        "message": "获取热点列表成功",
        "data": topics,
        "total": total
    }

@router.post("/hot-topics", response_model=HotTopicResponse)
async def create_hot_topic(
    topic_data: HotTopicCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """创建热点"""
    topic = HotTopic(
        title=topic_data.title,
        content=topic_data.content,
        cover_image=topic_data.cover_image,
        link_url=topic_data.link_url,
        category=topic_data.category,
        source=topic_data.source,
        sort_order=topic_data.sort_order,
        is_active=topic_data.is_active,
        publish_time=topic_data.publish_time
    )
    
    db.add(topic)
    db.commit()
    db.refresh(topic)
    
    return topic

@router.put("/hot-topics/{topic_id}", response_model=HotTopicResponse)
async def update_hot_topic(
    topic_id: int = Path(..., description="热点ID"),
    topic_data: HotTopicUpdate = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """更新热点"""
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="热点不存在")
    
    if topic_data.title is not None:
        topic.title = topic_data.title
    if topic_data.content is not None:
        topic.content = topic_data.content
    if topic_data.cover_image is not None:
        topic.cover_image = topic_data.cover_image
    if topic_data.link_url is not None:
        topic.link_url = topic_data.link_url
    if topic_data.category is not None:
        topic.category = topic_data.category
    if topic_data.source is not None:
        topic.source = topic_data.source
    if topic_data.sort_order is not None:
        topic.sort_order = topic_data.sort_order
    if topic_data.is_active is not None:
        topic.is_active = topic_data.is_active
    if topic_data.publish_time is not None:
        topic.publish_time = topic_data.publish_time
    
    db.commit()
    db.refresh(topic)
    
    return topic

@router.delete("/hot-topics/{topic_id}")
async def delete_hot_topic(
    topic_id: int = Path(..., description="热点ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """删除热点"""
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="热点不存在")
    
    db.delete(topic)
    db.commit()
    
    return {"success": True, "message": "删除成功"}

@router.get("/hot-topics/{topic_id}", response_model=HotTopicResponse)
async def get_hot_topic(
    topic_id: int = Path(..., description="热点ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取单个热点"""
    topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="热点不存在")
    return topic

@router.post("/check-vip-expiration")
async def check_vip_expiration(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """手动检查VIP过期状态"""
    from datetime import datetime
    
    vip_users = db.query(User).filter(User.is_vip == True).all()
    
    expired_count = 0
    expiring_soon_count = 0
    
    for user in vip_users:
        if user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                user.is_vip = False
                expired_count += 1
            elif (user.vip_end_time - datetime.now()).days <= 7:
                expiring_soon_count += 1
    
    if expired_count > 0:
        db.commit()
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": f"VIP状态检查完成，{expired_count}个用户已过期，{expiring_soon_count}个用户即将过期",
            "data": {
                "expired_count": expired_count,
                "expiring_soon_count": expiring_soon_count,
                "total_vip_users": len(vip_users)
            }
        }
    )

@router.post("/check-exam-expiration")
async def check_exam_expiration(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """手动检查考试日程过期状态"""
    from datetime import datetime
    from models.learning_materials import ExamSchedule
    
    expired_exams = db.query(ExamSchedule).filter(
        ExamSchedule.exam_date < datetime.now(),
        ExamSchedule.is_active == True
    ).all()
    
    expired_count = len(expired_exams)
    
    for exam in expired_exams:
        exam.is_active = False
    
    if expired_count > 0:
        db.commit()
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": f"考试日程检查完成，{expired_count}个考试已过期",
            "data": {
                "expired_count": expired_count
            }
        }
    )
