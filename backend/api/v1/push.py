from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.database import get_db_common, get_db_kaoyan, get_db_kaogong
from core.security import get_current_user, get_current_admin
from core.logger import log_user_action, log_error
from core.push_manager import send_email, send_payment_users_notifications, send_kaoyan_notifications, send_kaogong_notifications, send_expiry_notifications
from models.users import PushTemplate, PushLog, User, UserSubscription, UserKeyword
from models.kaoyan import KaoyanInfo
from models.kaogong import KaogongInfo
from schemas.push import PushTemplateCreate, PushTemplateUpdate, PushTemplateResponse, PushLogResponse, PushRequest

router = APIRouter(tags=["push"])

# 推送设置请求模型
class PushSettingsRequest(BaseModel):
    frequency: str
    time: Optional[str] = None

# 推送设置响应模型
class PushSettingsResponse(BaseModel):
    frequency: str
    time: Optional[str] = None

@router.get("/settings", summary="获取推送设置", response_model=PushSettingsResponse)
async def get_push_settings(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_admin)
):
    """获取推送设置"""
    try:
        from models.users import SystemConfig
        
        # 获取系统配置
        config = db.query(SystemConfig).filter(SystemConfig.config_key == "push_settings").first()
        
        if config:
            settings = eval(config.config_value)
            return PushSettingsResponse(
                frequency=settings.get("frequency", "daily"),
                time=settings.get("time", "09:00")
            )
        else:
            # 默认设置
            return PushSettingsResponse(
                frequency="daily",
                time="09:00"
            )
            
    except Exception as e:
        log_error(f"获取推送设置失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取推送设置失败"
        )

@router.post("/settings", summary="保存推送设置")
async def save_push_settings(
    request: PushSettingsRequest,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_admin)
):
    """保存推送设置"""
    try:
        from models.users import SystemConfig
        
        # 检查系统配置是否存在
        config = db.query(SystemConfig).filter(SystemConfig.config_key == "push_settings").first()
        
        # 格式化时间
        time_str = request.time
        if time_str and isinstance(time_str, datetime):
            time_str = time_str.strftime("%H:%M")
        
        settings = {
            "frequency": request.frequency,
            "time": time_str
        }
        
        if config:
            config.config_value = str(settings)
        else:
            config = SystemConfig(
                config_key="push_settings",
                config_value=str(settings),
                config_type=3,  # JSON类型
                description="推送设置",
                is_system=True,
                status=1
            )
            db.add(config)
            
        db.commit()
        db.refresh(config)
        
        log_user_action(current_user.id, "save_push_settings", f"保存推送设置: {str(settings)}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "保存推送设置成功",
                "data": settings
            }
        )
        
    except Exception as e:
        log_error(f"保存推送设置失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="保存推送设置失败"
        )


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


@router.post("/trigger/kaoyan", summary="触发考研情报推送")
async def trigger_kaoyan_push(
    current_user: Session = Depends(get_current_admin),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_common: Session = Depends(get_db_common)
):
    """触发考研情报推送"""
    try:
        # 获取所有活跃用户
        active_users = db_common.query(User).filter(User.is_active == True).all()
        
        push_count = 0
        for user in active_users:
            # 检查用户的订阅类型
            subscription = db_common.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
            if subscription and (subscription.subscribe_type == 1 or subscription.subscribe_type == 3):
                send_kaoyan_notifications(db_kaoyan, user, subscription)
                push_count += 1
        
        log_user_action(current_user.id, "trigger_kaoyan_push", f"触发考研情报推送，涉及用户数: {push_count}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": f"推送任务已触发，涉及 {push_count} 个用户",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"触发考研情报推送失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="触发推送失败"
        )


@router.post("/trigger/kaogong", summary="触发考公情报推送")
async def trigger_kaogong_push(
    current_user: Session = Depends(get_current_admin),
    db_kaogong: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common)
):
    """触发考公情报推送"""
    try:
        # 获取所有活跃用户
        active_users = db_common.query(User).filter(User.is_active == True).all()
        
        push_count = 0
        for user in active_users:
            # 检查用户的订阅类型
            subscription = db_common.query(UserSubscription).filter(UserSubscription.user_id == user.id).first()
            if subscription and (subscription.subscribe_type == 2 or subscription.subscribe_type == 3):
                send_kaogong_notifications(db_kaogong, user, subscription)
                push_count += 1
        
        log_user_action(current_user.id, "trigger_kaogong_push", f"触发考公情报推送，涉及用户数: {push_count}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": f"推送任务已触发，涉及 {push_count} 个用户",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"触发考公情报推送失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="触发推送失败"
        )


@router.post("/trigger/expiry", summary="触发到期提醒推送")
async def trigger_expiry_push(
    current_user: Session = Depends(get_current_admin)
):
    """触发到期提醒推送"""
    try:
        send_expiry_notifications()
        
        log_user_action(current_user.id, "trigger_expiry_push", "触发到期提醒推送")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "到期提醒推送任务已触发",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"触发到期提醒推送失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="触发推送失败"
        )


@router.get("/history", summary="获取推送历史")
async def get_push_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[int] = Query(None, ge=1, le=3, description="分类: 1-考研, 2-考公, 3-系统通知"),
    user_id: Optional[int] = Query(None, description="用户ID"),
    push_type: Optional[int] = Query(None, ge=1, le=3, description="推送类型: 1-微信, 2-企业微信, 3-邮件"),
    push_status: Optional[int] = Query(None, ge=0, le=1, description="推送状态: 0-失败, 1-成功"),
    start_time: Optional[str] = Query(None, description="开始时间"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    current_user: Session = Depends(get_current_admin),
    db_common: Session = Depends(get_db_common)
):
    """获取推送历史"""
    try:
        # 构建查询
        query = db_common.query(PushLog)
        
        # 过滤条件
        if category:
            query = query.filter(PushLog.category == category)
        if user_id:
            query = query.filter(PushLog.user_id == user_id)
        if push_type:
            query = query.filter(PushLog.push_type == push_type)
        if push_status is not None:
            query = query.filter(PushLog.push_status == push_status)
        if start_time:
            start_dt = datetime.fromisoformat(start_time)
            query = query.filter(PushLog.push_time >= start_dt)
        if end_time:
            end_dt = datetime.fromisoformat(end_time)
            query = query.filter(PushLog.push_time <= end_dt)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        push_logs = query.order_by(PushLog.push_time.desc()).offset(offset).limit(page_size).all()
        
        # 构建响应
        items = []
        for log in push_logs:
            # 获取用户信息
            user = db_common.query(User).filter(User.id == log.user_id).first()
            user_info = {
                "id": user.id,
                "username": user.username,
                "email": user.email
            } if user else None
            
            items.append({
                "id": log.id,
                "user_id": log.user_id,
                "user_info": user_info,
                "info_id": log.info_id,
                "category": log.category,
                "category_text": "考研" if log.category == 1 else "考公" if log.category == 2 else "系统通知",
                "push_type": log.push_type,
                "push_type_text": "微信" if log.push_type == 1 else "企业微信" if log.push_type == 2 else "邮件",
                "push_status": log.push_status,
                "push_status_text": "成功" if log.push_status == 1 else "失败",
                "push_content": log.push_content,
                "error_msg": log.error_msg,
                "is_processed": log.is_processed,
                "push_time": log.push_time.isoformat()
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取推送历史成功",
                "data": {
                    "total": total,
                    "items": items
                }
            }
        )
    except Exception as e:
        log_error(f"获取推送历史失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取推送历史失败"
        )


@router.get("/stats", summary="获取推送统计")
async def get_push_stats(
    current_user: Session = Depends(get_current_admin),
    db_common: Session = Depends(get_db_common)
):
    """获取推送统计"""
    try:
        # 统计推送总数
        total_push = db_common.query(PushLog).count()
        
        # 统计成功推送数
        success_push = db_common.query(PushLog).filter(
            PushLog.push_status == 1
        ).count()
        
        # 统计失败推送数
        failed_push = db_common.query(PushLog).filter(
            PushLog.push_status == 0
        ).count()
        
        # 统计最近7天推送数
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_push = db_common.query(PushLog).filter(
            PushLog.push_time >= seven_days_ago
        ).count()
        
        # 按类型统计
        category_stats = [
            {
                "category": 1,
                "category_text": "考研",
                "count": db_common.query(PushLog).filter(PushLog.category == 1).count()
            },
            {
                "category": 2,
                "category_text": "考公",
                "count": db_common.query(PushLog).filter(PushLog.category == 2).count()
            },
            {
                "category": 3,
                "category_text": "系统通知",
                "count": db_common.query(PushLog).filter(PushLog.category == 3).count()
            }
        ]
        
        # 按推送渠道统计
        channel_stats = [
            {
                "push_type": 1,
                "push_type_text": "微信",
                "count": db_common.query(PushLog).filter(PushLog.push_type == 1).count()
            },
            {
                "push_type": 2,
                "push_type_text": "企业微信",
                "count": db_common.query(PushLog).filter(PushLog.push_type == 2).count()
            },
            {
                "push_type": 3,
                "push_type_text": "邮件",
                "count": db_common.query(PushLog).filter(PushLog.push_type == 3).count()
            }
        ]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取推送统计成功",
                "data": {
                    "total_push": total_push,
                    "success_push": success_push,
                    "failed_push": failed_push,
                    "recent_push": recent_push,
                    "success_rate": success_push / total_push * 100 if total_push > 0 else 0,
                    "category_stats": category_stats,
                    "channel_stats": channel_stats
                }
            }
        )
    except Exception as e:
        log_error(f"获取推送统计失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取推送统计失败"
        )





@router.get("/trend", summary="获取推送趋势")
async def get_push_trend(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    current_user: Session = Depends(get_current_admin),
    db_common: Session = Depends(get_db_common)
):
    """获取推送趋势"""
    try:
        # 计算开始日期
        start_date = datetime.now() - timedelta(days=days-1)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 生成日期列表
        date_list = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_list.append(date)
        
        # 按日期统计推送数量
        trend_data = []
        for date in date_list:
            next_date = date + timedelta(days=1)
            push_count = db_common.query(PushLog).filter(
                PushLog.push_time >= date,
                PushLog.push_time < next_date
            ).count()
            trend_data.append({
                "date": date.strftime("%m-%d"),
                "count": push_count
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取推送趋势成功",
                "data": trend_data
            }
        )
    except Exception as e:
        log_error(f"获取推送趋势失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取推送趋势失败"
        )


@router.delete("/history/{history_id}", summary="删除单条推送记录")
async def delete_push_history(
    history_id: int = Path(..., ge=1, description="推送记录ID"),
    current_user: Session = Depends(get_current_admin),
    db_common: Session = Depends(get_db_common)
):
    """删除单条推送记录"""
    try:
        # 查找推送记录
        push_log = db_common.query(PushLog).filter(PushLog.id == history_id).first()
        if not push_log:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "推送记录不存在",
                    "data": None
                }
            )
        
        # 删除推送记录
        db_common.delete(push_log)
        db_common.commit()
        
        log_user_action(current_user.id, "delete_push_history", f"删除推送记录 ID: {history_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除推送记录失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除失败"
        )


@router.delete("/history", summary="删除全部推送记录")
async def delete_all_push_history(
    current_user: Session = Depends(get_current_admin),
    db_common: Session = Depends(get_db_common)
):
    """删除全部推送记录"""
    try:
        # 删除所有推送记录
        db_common.query(PushLog).delete()
        db_common.commit()
        
        log_user_action(current_user.id, "delete_all_push_history", "删除全部推送记录")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "全部删除成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除全部推送记录失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除失败"
        )




