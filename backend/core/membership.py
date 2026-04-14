import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.users import User, UserSubscription, Product, Order

logger = logging.getLogger(__name__)


class MembershipManager:
    """会员管理类"""
    
    @staticmethod
    def get_user_subscription(db: Session, user_id: int) -> UserSubscription:
        """获取用户订阅信息"""
        return db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).first()
    
    @staticmethod
    def create_subscription(db: Session, user_id: int, product_id: int) -> UserSubscription:
        """创建用户订阅"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("产品不存在")
        
        # 计算订阅结束时间
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=product.duration)
        
        # 先将用户的其他订阅设置为非活跃
        db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).update({"status": 0})
        
        # 创建新的订阅
        subscription = UserSubscription(
            user_id=user_id,
            subscribe_type=product.type,
            status=1
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        return subscription
    
    @staticmethod
    def check_subscription_status(db: Session, user_id: int) -> bool:
        """检查用户订阅状态"""
        subscription = MembershipManager.get_user_subscription(db, user_id)
        if not subscription:
            return False
        
        return True
    
    @staticmethod
    def get_subscription_type(db: Session, user_id: int) -> str:
        """获取用户订阅类型"""
        subscription = MembershipManager.get_user_subscription(db, user_id)
        if not subscription:
            return "free"
        
        return subscription.subscribe_type
    
    @staticmethod
    def get_subscription_end_date(db: Session, user_id: int) -> datetime:
        """获取用户订阅结束日期"""
        return None
    
    @staticmethod
    def renew_subscription(db: Session, user_id: int, product_id: int) -> UserSubscription:
        """续费订阅"""
        return MembershipManager.create_subscription(db, user_id, product_id)
    
    @staticmethod
    def cancel_subscription(db: Session, user_id: int) -> bool:
        """取消订阅"""
        subscription = MembershipManager.get_user_subscription(db, user_id)
        if not subscription:
            return False
        
        subscription.status = 0
        db.commit()
        return True
    
    @staticmethod
    def get_user_products(db: Session) -> list[Product]:
        """获取所有产品"""
        return db.query(Product).filter(Product.status == 1).all()
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        """根据ID获取产品"""
        return db.query(Product).filter(Product.id == product_id).first()
