#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from core.database import get_db
from models.users import UserSubscription

db = next(get_db(database="common"))
try:
    subscriptions = db.query(UserSubscription).all()
    print('用户订阅配置详情:')
    for sub in subscriptions:
        print(f'ID: {sub.id}, User ID: {sub.user_id}, Status: {sub.status}, Config: {sub.config_json}')
finally:
    db.close()
