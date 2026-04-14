from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db, get_db_kaoyan, get_db_kaogong
from core.security import get_current_admin
from core.crawler_manager import generate_dynamic_crawler_configs
from models.users import User, Order, Product, SystemConfig, PushTemplate, PushLog, UserSubscription, UserKeyword, UserReadInfo, UserFavorite
from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog
from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog
from schemas.users import UserResponse, UserUpdate
from schemas.kaoyan import KaoyanInfoResponse, KaoyanCrawlerConfigResponse
from schemas.kaogong import KaogongInfoResponse, KaogongCrawlerConfigResponse
from schemas.payments import OrderResponse, ProductResponse
from schemas.push import PushTemplateResponse, PushLogResponse
from schemas.system import SystemConfigResponse, SystemStatsResponse

router = APIRouter(tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    is_admin: Optional[bool] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取用户列表（管理员）"""
    query = db.query(User)
    
    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    users = query.offset(skip).limit(limit).all()
    
    # 为每个用户添加类型信息
    for user in users:
        # 查询用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        if subscription:
            if subscription.subscribe_type == 1:
                user.user_type = "考研"
            elif subscription.subscribe_type == 2:
                user.user_type = "考公"
            elif subscription.subscribe_type == 3:
                user.user_type = "双赛道"
        else:
            user.user_type = "未订阅"
    
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """获取用户详情（管理员）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 添加用户类型信息
    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == user.id,
        UserSubscription.status == 1
    ).first()
    
    if subscription:
        if subscription.subscribe_type == 1:
            user.user_type = "考研"
        elif subscription.subscribe_type == 2:
            user.user_type = "考公"
        elif subscription.subscribe_type == 3:
            user.user_type = "双赛道"
    else:
        user.user_type = "未订阅"
    
    return user


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
        if key != 'user_type':  # 排除user_type字段，因为它不是User模型的直接字段
            setattr(user, key, value)
    
    # 处理user_type字段更新
    if 'user_type' in update_data:
        # 获取用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        if subscription:
            # 根据user_type更新subscribe_type
            if update_data['user_type'] == "考研":
                subscription.subscribe_type = 1
            elif update_data['user_type'] == "考公":
                subscription.subscribe_type = 2
            elif update_data['user_type'] == "双赛道":
                subscription.subscribe_type = 3
    
    db.commit()
    db.refresh(user)
    
    # 重新获取用户信息，确保包含user_type字段
    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == user.id,
        UserSubscription.status == 1
    ).first()
    
    if subscription:
        if subscription.subscribe_type == 1:
            user.user_type = "考研"
        elif subscription.subscribe_type == 2:
            user.user_type = "考公"
        elif subscription.subscribe_type == 3:
            user.user_type = "双赛道"
    else:
        user.user_type = "未订阅"
    
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
        
        # 删除用户的订单
        orders = db.query(Order).filter(Order.user_id == user_id).all()
        for order in orders:
            db.delete(order)
        
        # 删除用户的推送日志
        push_logs = db.query(PushLog).filter(PushLog.user_id == user_id).all()
        for log in push_logs:
            db.delete(log)
        
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
        
        # 获取用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).first()
        
        requirements = {
            'kaoyan': {},
            'kaogong': {}
        }
        
        if subscription and subscription.config_json:
            config_json = subscription.config_json
            # 如果config_json是字符串，解析它
            if isinstance(config_json, str):
                import json
                config_json = json.loads(config_json)
            
            # 直接返回数据库中的数据
        if 'kaoyan' in config_json:
            kaoyan_config = config_json['kaoyan']
            # 确保keywords是列表
            if 'keywords' in kaoyan_config and not isinstance(kaoyan_config['keywords'], list):
                kaoyan_config['keywords'] = []
            requirements['kaoyan'] = kaoyan_config
        if 'kaogong' in config_json:
            kaogong_config = config_json['kaogong']
            # 确保keywords是列表
            if 'keywords' in kaogong_config and not isinstance(kaogong_config['keywords'], list):
                kaogong_config['keywords'] = []
            requirements['kaogong'] = kaogong_config
        
        # 获取用户的关键词
        keywords = db.query(UserKeyword).filter(
            UserKeyword.user_id == user_id,
            UserKeyword.is_active == True
        ).all()
        
        for kw in keywords:
            category = 'kaoyan' if kw.category == 1 else 'kaogong'
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
    db_common: Session = Depends(get_db),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_admin: User = Depends(get_current_admin)
):
    """获取系统统计信息（管理员）"""
    # 计算用户数
    user_count = db_common.query(User).count()
    
    # 计算考研信息数
    kaoyan_count = db_kaoyan.query(KaoyanInfo).count()
    
    # 计算考公信息数
    kaogong_count = db_kaogong.query(KaogongInfo).count()
    
    # 计算订单数
    order_count = db_common.query(Order).count()
    
    # 计算推送数
    push_count = db_common.query(PushLog).count()
    
    # 计算用户类型分布
    user_type_distribution = {
        "未订阅": 0,
        "考研": 0,
        "考公": 0,
        "双赛道": 0
    }
    
    # 获取所有用户
    users = db_common.query(User).all()
    
    for user in users:
        # 获取用户的订阅配置（状态为1的有效订阅）
        subscription = db_common.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        user_type = "未订阅"
        if subscription:
            if subscription.subscribe_type == 1:
                user_type = "考研"
            elif subscription.subscribe_type == 2:
                user_type = "考公"
            elif subscription.subscribe_type == 3:
                user_type = "双赛道"
        
        user_type_distribution[user_type] += 1
    
    return {
        "user_count": user_count,
        "kaoyan_count": kaoyan_count,
        "kaogong_count": kaogong_count,
        "order_count": order_count,
        "push_count": push_count,
        "user_type_distribution": user_type_distribution,
        "timestamp": datetime.utcnow()
    }


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
        
        # 收集用户的爬虫配置 - 只返回 AI 生成的链接，在 AI 没有生成链接之前，不显示任何链接
        user_crawlers = []
        
        # 从数据库中获取 AI 生成的爬虫配置
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
            'status': user.is_active
        })
    
    return student_crawlers_list


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
