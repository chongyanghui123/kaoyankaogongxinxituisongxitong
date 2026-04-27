from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import BaseCommon
from models.users import User


class MaterialCategory(BaseCommon):
    __tablename__ = "material_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    type = Column(Integer, nullable=True, comment="分类类型")
    description = Column(Text, nullable=True, comment="分类描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    def __repr__(self):
        return f"<MaterialCategory(id={self.id}, name={self.name}, type={self.type})>"


class LearningMaterial(BaseCommon):
    __tablename__ = "learning_materials"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="资料标题")
    description = Column(Text, nullable=True, comment="资料描述")
    type = Column(Integer, nullable=True, comment="资料类型")
    category_id = Column(Integer, ForeignKey("material_categories.id"), comment="分类ID")
    subject = Column(String(100), nullable=True, comment="科目")
    file_path = Column(String(255), nullable=True, comment="文件路径")
    file_url = Column(String(255), nullable=True, comment="文件链接")
    file_size = Column(Integer, nullable=True, comment="文件大小")
    file_extension = Column(String(50), nullable=True, comment="文件扩展名")
    cover_image = Column(String(255), nullable=True, comment="封面图片")
    uploader_id = Column(Integer, nullable=True, comment="上传者ID")
    upload_time = Column(DateTime, nullable=True, comment="上传时间")
    download_count = Column(Integer, default=0, comment="下载次数")
    rating = Column(Float, default=0, comment="评分")
    is_valid = Column(Boolean, default=True, comment="是否有效")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    category = relationship("MaterialCategory", backref="materials")
    
    def __repr__(self):
        return f"<LearningMaterial(id={self.id}, title={self.title})>"


class UserDownload(BaseCommon):
    __tablename__ = "user_downloads"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), comment="资料ID")
    download_time = Column(DateTime, default=datetime.now, comment="下载时间")
    ip_address = Column(String(50), nullable=True, comment="IP地址")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    user = relationship("User", backref="downloads")
    material = relationship("LearningMaterial", backref="downloads")
    
    def __repr__(self):
        return f"<UserDownload(id={self.id}, user_id={self.user_id}, material_id={self.material_id})>"


class MaterialRating(BaseCommon):
    __tablename__ = "material_ratings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), comment="资料ID")
    rating = Column(Integer, nullable=False, comment="评分")
    created_at = Column(DateTime, default=datetime.now, comment="评分时间")
    
    user = relationship("User", backref="ratings")
    material = relationship("LearningMaterial", backref="ratings")
    
    def __repr__(self):
        return f"<MaterialRating(id={self.id}, user_id={self.user_id}, material_id={self.material_id}, rating={self.rating})>"


class MaterialComment(BaseCommon):
    __tablename__ = "material_comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    material_id = Column(Integer, ForeignKey("learning_materials.id"), comment="资料ID")
    parent_comment_id = Column(Integer, nullable=True, comment="父评论ID")
    comment = Column(Text, nullable=False, comment="评论内容")
    created_at = Column(DateTime, default=datetime.now, comment="评论时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    user = relationship("User", backref="comments")
    material = relationship("LearningMaterial", backref="comments")
    
    def __repr__(self):
        return f"<MaterialComment(id={self.id}, user_id={self.user_id}, material_id={self.material_id})>"


class ExamSchedule(BaseCommon):
    __tablename__ = "exam_schedules"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="考试名称")
    exam_type = Column(Integer, nullable=False, comment="考试类型: 1-考研, 2-考公")
    exam_date = Column(DateTime, nullable=False, comment="考试日期")
    description = Column(Text, nullable=True, comment="考试描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<ExamSchedule(id={self.id}, name={self.name}, exam_date={self.exam_date})>"


class Carousel(BaseCommon):
    __tablename__ = "carousels"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="轮播图标题")
    subtitle = Column(String(500), nullable=True, comment="轮播图副标题")
    image_url = Column(String(500), nullable=True, comment="轮播图图片URL")
    link_url = Column(String(500), nullable=True, comment="跳转链接URL")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<Carousel(id={self.id}, title={self.title}, sort_order={self.sort_order})>"
