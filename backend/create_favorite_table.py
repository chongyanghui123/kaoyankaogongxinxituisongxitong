#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建用户学习资料收藏表
"""

from core.database import common_db_engine
from models.learning_materials import UserMaterialFavorite
from models.learning_materials import LearningMaterial
from sqlalchemy import MetaData

def main():
    try:
        metadata = MetaData()
        metadata.reflect(bind=common_db_engine)
        
        if 'user_material_favorites' not in metadata.tables:
            UserMaterialFavorite.__table__.create(bind=common_db_engine)
            print('Table created successfully')
        else:
            print('Table already exists')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()