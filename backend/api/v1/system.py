from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.users import SystemConfig, User
from schemas.system import SystemConfigCreate, SystemConfigUpdate, SystemConfigResponse, SystemStatsResponse

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/configs", response_model=List[SystemConfigResponse])
async def get_system_configs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    key: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取系统配置列表"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看系统配置")
    
    query = db.query(SystemConfig)
    
    if key:
        query = query.filter(SystemConfig.key == key)
    
    configs = query.offset(skip).limit(limit).all()
    return configs


@router.get("/configs/{config_id}", response_model=SystemConfigResponse)
async def get_system_config(
    config_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取系统配置详情"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看系统配置")
    
    config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="系统配置不存在")
    return config


@router.post("/configs", response_model=SystemConfigResponse, dependencies=[Depends(get_current_admin)])
async def create_system_config(
    config: SystemConfigCreate,
    db: Session = Depends(get_db)
):
    """创建系统配置"""
    # 检查键是否已存在
    existing_config = db.query(SystemConfig).filter(SystemConfig.key == config.key).first()
    if existing_config:
        raise HTTPException(status_code=400, detail="配置键已存在")
    
    db_config = SystemConfig(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


@router.put("/configs/{config_id}", response_model=SystemConfigResponse, dependencies=[Depends(get_current_admin)])
async def update_system_config(
    config: SystemConfigUpdate,
    config_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """更新系统配置"""
    db_config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="系统配置不存在")
    
    # 如果更新键，检查新键是否已存在
    if config.key and config.key != db_config.key:
        existing_config = db.query(SystemConfig).filter(SystemConfig.key == config.key).first()
        if existing_config:
            raise HTTPException(status_code=400, detail="配置键已存在")
    
    for key, value in config.dict(exclude_unset=True).items():
        setattr(db_config, key, value)
    
    db.commit()
    db.refresh(db_config)
    return db_config


@router.delete("/configs/{config_id}", dependencies=[Depends(get_current_admin)])
async def delete_system_config(
    config_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """删除系统配置"""
    db_config = db.query(SystemConfig).filter(SystemConfig.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="系统配置不存在")
    
    db.delete(db_config)
    db.commit()
    return {"message": "系统配置删除成功"}


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取系统统计信息"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看系统统计")
    
    # 计算用户数
    user_count = db.query(User).count()
    
    # 计算考研信息数
    from models.kaoyan import KaoyanInfo
    kaoyan_count = db.query(KaoyanInfo).count()
    
    # 计算考公信息数
    from models.kaogong import KaogongInfo
    kaogong_count = db.query(KaogongInfo).count()
    
    # 计算订单数
    from models.users import Order
    order_count = db.query(Order).count()
    
    # 计算推送数
    from models.users import PushLog
    push_count = db.query(PushLog).count()
    
    return {
        "user_count": user_count,
        "kaoyan_count": kaoyan_count,
        "kaogong_count": kaogong_count,
        "order_count": order_count,
        "push_count": push_count,
        "timestamp": datetime.utcnow()
    }


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}
