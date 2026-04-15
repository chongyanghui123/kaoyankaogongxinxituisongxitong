from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db_common
from core.security import get_current_user, get_current_admin
from core.push_manager import send_payment_users_notifications
from models.users import PushTemplate, PushLog, User
from schemas.push import PushTemplateCreate, PushTemplateUpdate, PushTemplateResponse, PushLogResponse, PushRequest

router = APIRouter(tags=["push"])


@router.post("/send", response_model=PushLogResponse)
async def send_push(
    push: PushRequest,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """发送推送通知"""
    # 检查用户是否有发送推送的权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限发送推送")
    
    # 检查模板是否存在
    template = db.query(PushTemplate).filter(PushTemplate.id == push.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="推送模板不存在")
    
    # 发送推送
    # 这里需要根据实际的推送接口实现
    
    # 记录推送日志
    push_log = PushLog(
        template_id=push.template_id,
        user_id=push.user_id,
        content=push.content,
        status="sent",
        created_at=datetime.utcnow()
    )
    db.add(push_log)
    db.commit()
    db.refresh(push_log)
    
    return push_log


@router.get("/templates", response_model=List[PushTemplateResponse])
async def get_push_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取推送模板列表"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看推送模板")
    
    templates = db.query(PushTemplate).offset(skip).limit(limit).all()
    return templates


@router.get("/templates/{template_id}", response_model=PushTemplateResponse)
async def get_push_template(
    template_id: int = Path(..., ge=1),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取推送模板详情"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看推送模板")
    
    template = db.query(PushTemplate).filter(PushTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="推送模板不存在")
    return template


@router.post("/templates", response_model=PushTemplateResponse, dependencies=[Depends(get_current_admin)])
async def create_push_template(
    template: PushTemplateCreate,
    db: Session = Depends(get_db_common)
):
    """创建推送模板"""
    db_template = PushTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.put("/templates/{template_id}", response_model=PushTemplateResponse, dependencies=[Depends(get_current_admin)])
async def update_push_template(
    template: PushTemplateUpdate,
    template_id: int = Path(..., ge=1),
    db: Session = Depends(get_db_common)
):
    """更新推送模板"""
    db_template = db.query(PushTemplate).filter(PushTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="推送模板不存在")
    
    for key, value in template.dict(exclude_unset=True).items():
        setattr(db_template, key, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template


@router.delete("/templates/{template_id}", dependencies=[Depends(get_current_admin)])
async def delete_push_template(
    template_id: int = Path(..., ge=1),
    db: Session = Depends(get_db_common)
):
    """删除推送模板"""
    db_template = db.query(PushTemplate).filter(PushTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="推送模板不存在")
    
    db.delete(db_template)
    db.commit()
    return {"message": "推送模板删除成功"}


@router.get("/logs", response_model=List[PushLogResponse])
async def get_push_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取推送日志"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看推送日志")
    
    query = db.query(PushLog)
    
    if status:
        query = query.filter(PushLog.status == status)
    if user_id:
        query = query.filter(PushLog.user_id == user_id)
    
    logs = query.offset(skip).limit(limit).all()
    return logs


@router.get("/logs/{log_id}", response_model=PushLogResponse)
async def get_push_log(
    log_id: int = Path(..., ge=1),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取推送日志详情"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权限查看推送日志")
    
    log = db.query(PushLog).filter(PushLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="推送日志不存在")
    return log


@router.post("/send-to-payment-users")
async def send_to_payment_users(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_admin)
):
    """给已经支付订单的用户推送消息"""
    try:
        # 调用推送函数
        send_payment_users_notifications()
        return {"message": "推送任务已启动，正在处理"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推送失败: {str(e)}")
