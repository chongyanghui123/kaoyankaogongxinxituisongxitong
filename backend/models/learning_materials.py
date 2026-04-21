#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习资料模型
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import BaseCommon as Base
from models.users import User


class MaterialCategory(Base):
    """资料分类模型"""
    __tablename__ = "material_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    type = Column(Integer, nullable=False, comment="适用类型：1-考研，2-考公，3-通用")
    description = Column(Text, comment="分类描述")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关系
    materials = relationship("LearningMaterial", back_populates="category")


class LearningMaterial(Base):
    """学习资料模型"""
    __tablename__ = "learning_materials"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="资料标题")
    description = Column(Text, nullable=False, comment="资料描述")
    type = Column(Integer, nullable=False, index=True, comment="资料类型：1-考研，2-考公")
    category_id = Column(Integer, ForeignKey("material_categories.id"), nullable=False, index=True, comment="资料分类ID")
    subject = Column(String(100), nullable=False, index=True, comment="科目：如数学、英语、政治等")
    file_path = Column(String(255), nullable=False, comment="文件存储路径")
    file_url = Column(String(255), nullable=False, comment="文件下载URL")
    file_size = Column(Integer, nullable=False, comment="文件大小，单位：字节")
    file_extension = Column(String(50), nullable=False, comment="文件扩展名")
    cover_image = Column(String(255), comment="封面图片URL")
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="上传者ID")
    upload_time = Column(DateTime, nullable=False, comment="上传时间")
    download_count = Column(Integer, default=0, comment="下载次数")
    rating = Column(Float, default=0, comment="评分")
    is_valid = Column(Boolean, default=True, comment="是否有效")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    category = relationship("MaterialCategory", back_populates="materials")
    uploader = relationship("User", backref="uploaded_materials")
    downloads = relationship("UserDownload", back_populates="material")
    ratings = relationship("MaterialRating", back_populates="material")
    comments = relationship("MaterialComment", back_populates="material")
    favorites = relationship("UserMaterialFavorite", back_populates="material")


class UserDownload(Base):
    """用户下载记录模型"""
    __tablename__ = "user_downloads"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), nullable=False, index=True, comment="资料ID")
    download_time = Column(DateTime, nullable=False, comment="下载时间")
    ip_address = Column(String(50), comment="下载IP地址")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关系
    user = relationship("User", backref="downloads")
    material = relationship("LearningMaterial", back_populates="downloads")


class MaterialRating(Base):
    """资料评分模型"""
    __tablename__ = "material_ratings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), nullable=False, comment="资料ID")
    rating = Column(Integer, nullable=False, comment="评分，1-5星")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    
    # 关系
    user = relationship("User", backref="ratings")
    material = relationship("LearningMaterial", back_populates="ratings")


class MaterialComment(Base):
    """资料评论模型"""
    __tablename__ = "material_comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), nullable=False, comment="资料ID")
    parent_comment_id = Column(Integer, ForeignKey("material_comments.id"), nullable=True, comment="父评论ID（回复功能）")
    comment = Column(Text, nullable=False, comment="评论内容")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    user = relationship("User", backref="comments")
    material = relationship("LearningMaterial", back_populates="comments")
    parent_comment = relationship("MaterialComment", remote_side=[id], backref="replies")


class UserMaterialFavorite(Base):
    """用户学习资料收藏模型"""
    __tablename__ = "user_material_favorites"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), nullable=False, index=True, comment="资料ID")
    created_at = Column(DateTime, default=func.now(), comment="收藏时间")
    
    # 关系
    user = relationship("User", backref="material_favorites")
    material = relationship("LearningMaterial", back_populates="favorites")
