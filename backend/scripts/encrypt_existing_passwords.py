#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将现有用户的明文密码转换为哈希存储
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import common_db_engine, BaseCommon, SessionLocalCommon
from core.security import get_password_hash, verify_password
from models.users import User
from sqlalchemy.orm import sessionmaker

session = SessionLocalCommon()

def encrypt_existing_passwords():
    """将