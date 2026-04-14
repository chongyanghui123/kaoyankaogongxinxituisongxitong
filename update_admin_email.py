#!/usr/bin/env python3
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath('backend'))

from core.database import get_db_common
from sqlalchemy import text

def update_admin_email():
    """更新管理员邮箱地址"""
    db = next(get_db_common())
    try:
        print('更新管理员邮箱地址...')
        
        # 执行更新
        result = db.execute(
            text('UPDATE users SET email = :email WHERE username = :username'),
            {'email': 'admin@shuangsai.com', 'username': 'admin'}
        )
        db.commit()
        
        print(f'影响的行数: {result.rowcount}')
        
        # 验证
        user = db.execute(
            text('SELECT username, email FROM users WHERE username = :username'),
            {'username': 'admin'}
        ).fetchone()
        
        if user:
            print(f'更新后 - 用户名: {user.username}, 邮箱: {user.email}')
            if user.email == 'admin@shuangsai.com':
                print('✅ 邮箱地址更新成功！')
            else:
                print('❌ 邮箱地址更新失败')
        else:
            print('❌ 未找到管理员用户')
            
    except Exception as e:
        print(f'❌ 发生错误: {str(e)}')
    finally:
        db.close()

if __name__ == '__main__':
    update_admin_email()
