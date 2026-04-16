"""
同步帮助函数，用于解决异步函数在同步上下文中的调用问题
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from models.users import User, UserSubscription, UserKeyword


def sync_get_user_requirements(user_id: int, db: Session, user: User) -> Dict[str, Any]:
    """同步获取用户需求信息（不使用异步函数）"""
    requirements = {
        'kaoyan': {},
        'kaogong': {}
    }
    
    try:
        # 获取用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == 1
        ).first()
        
        # 处理订阅配置
        if subscription and hasattr(subscription, 'config_json'):
            config_json = subscription.config_json
            
            # 处理配置 JSON 数据
            if config_json:
                if isinstance(config_json, str):
                    import json
                    try:
                        config_json = json.loads(config_json)
                    except Exception as e:
                        config_json = {}
                
                if isinstance(config_json, dict):
                    # 处理考研需求
                    if 'kaoyan' in config_json:
                        kaoyan_config = config_json['kaoyan']
                        if isinstance(kaoyan_config, dict):
                            requirements['kaoyan'] = kaoyan_config
                    elif 'kaoyan_requirements' in config_json:
                        kaoyan_config = config_json['kaoyan_requirements']
                        if isinstance(kaoyan_config, dict):
                            requirements['kaoyan'] = kaoyan_config
                    
                    # 处理考公需求
                    if 'kaogong' in config_json:
                        kaogong_config = config_json['kaogong']
                        if isinstance(kaogong_config, dict):
                            requirements['kaogong'] = kaogong_config
                    elif 'kaogong_requirements' in config_json:
                        kaogong_config = config_json['kaogong_requirements']
                        if isinstance(kaogong_config, dict):
                            requirements['kaogong'] = kaogong_config
        
        # 获取用户的关键词
        keywords = db.query(UserKeyword).filter(
            UserKeyword.user_id == user_id,
            UserKeyword.is_active == True
        ).all()
        
        # 处理关键词
        for kw in keywords:
            category = 'kaoyan' if kw.category == 1 else 'kaogong'
            if 'keywords' not in requirements[category] or not requirements[category]['keywords']:
                if 'keywords' not in requirements[category]:
                    requirements[category]['keywords'] = []
                requirements[category]['keywords'].append(kw.keyword)
    
    except Exception as e:
        import traceback
        from core.logger import log_error
        log_error(f"获取用户{user_id}需求信息失败: {str(e)}")
        log_error(f"错误堆栈: {traceback.format_exc()}")
    
    return requirements
