#!/usr/bin/env python3

import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db_common
from models.users import User, UserSubscription, UserKeyword

def check_user_kaogong_requirements():
    """检查用户的考公需求配置"""
    db = next(get_db_common())
    try:
        # 获取所有用户的考公订阅配置
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.subscribe_type.in_([2, 3])  # 2-考公, 3-双赛道
        ).all()
        
        for subscription in subscriptions:
            user = db.query(User).filter(User.id == subscription.user_id).first()
            if user:
                # 获取用户的关键词
                keywords = db.query(UserKeyword).filter(
                    UserKeyword.user_id == user.id,
                    UserKeyword.category == 2  # 2-考公关键词
                ).all()
                
                # 解析配置
                config = subscription.config_json or {}
                
                print(f"用户: {user.username}")
                print(f"订阅类型: {'考公' if subscription.subscribe_type == 2 else '双赛道'}")
                print(f"配置: {config}")
                print(f"关键词: {[kw.keyword for kw in keywords]}")
                print("---")
    finally:
        db.close()

def main():
    """主函数"""
    print("开始检查用户的考公需求配置...")
    check_user_kaogong_requirements()
    print("用户考公需求配置检查完成！")

if __name__ == "__main__":
    main()
