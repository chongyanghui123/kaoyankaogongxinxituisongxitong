#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据库更新功能
"""

import sys
import os
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from core.database import SessionLocalCommon
from models.users import User, UserSubscription

def test_update_user_subscription():
    """测试更新用户订阅配置"""
    print("=" * 60)
    print("测试数据库更新功能")
    print("=" * 60)
    
    db = SessionLocalCommon()
    
    try:
        # 获取第一个用户
        user = db.query(User).first()
        if not user:
            print("没有找到用户！")
            return
        
        print(f"找到用户: {user.username} (ID: {user.id})")
        
        # 获取用户的订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == 1
        ).first()
        
        if subscription:
            print(f"\n当前订阅配置 (config_json):")
            print(json.dumps(subscription.config_json, indent=2, ensure_ascii=False))
            
            # 尝试更新配置
            new_config = subscription.config_json.copy() if subscription.config_json else {}
            
            if 'kaoyan' not in new_config:
                new_config['kaoyan'] = {}
            
            # 更新考研省份
            new_config['kaoyan']['provinces'] = ['四川', '重庆', '云南']
            new_config['kaoyan']['schools'] = ['西南大学']
            new_config['kaoyan']['majors'] = ['计算机科学']
            
            print(f"\n新的配置:")
            print(json.dumps(new_config, indent=2, ensure_ascii=False))
            
            # 更新数据库
            subscription.config_json = new_config
            db.commit()
            db.refresh(subscription)
            
            print(f"\n更新成功！")
            print(f"更新后的配置:")
            print(json.dumps(subscription.config_json, indent=2, ensure_ascii=False))
            
        else:
            print("\n没有找到用户订阅配置！")
            
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_update_user_subscription()
