from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import BaseCommon

class School(BaseCommon):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    province = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    has_master = Column(Boolean, default=True, nullable=False)  # 是否有硕士点
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<School(name='{self.name}', province='{self.province}', has_master={self.has_master})>"
