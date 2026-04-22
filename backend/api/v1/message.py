from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.responses import JSONResponse

from core.database import get_db_common
from core.security import get_current_user
from models.users import PushLog, User
from schemas.message import MessageResponse

router = APIRouter(tags=["message"])


@router.get("/list", response_model=dict)
async def get_message_list(
    tab: str = Query(..., description="消息类型: all, system, info, expiry"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取消息列表"""
    try:
        # 构建查询
        query = db.query(PushLog).filter(PushLog.user_id == current_user.id)
        
        # 根据tab筛选
        if tab == "system":
            # 系统通知：包含系统通知和学习资料上传通知
            query = query.filter(
                PushLog.push_content.contains("系统") | 
                PushLog.push_content.contains("学习资料")
            )
        elif tab == "info":
            # 情报推送：排除系统通知和到期提醒
            query = query.filter(
                ~PushLog.push_content.contains("系统") & 
                ~PushLog.push_content.contains("学习资料") & 
                ~PushLog.push_content.contains("到期")
            )
        elif tab == "expiry":
            # 到期提醒：只包含到期相关的通知
            query = query.filter(PushLog.push_content.contains("到期"))
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        push_logs = query.order_by(PushLog.push_time.desc()).offset(offset).limit(page_size).all()
        
        # 转换为响应格式
        items = []
        for log in push_logs:
            # 简单判断消息类型
            message_type = "info"
            if "到期" in (log.push_content or ""):
                message_type = "expiry"
            elif "系统" in (log.push_content or "") or "学习资料" in (log.push_content or ""):
                message_type = "system"
            
            items.append({
                "id": log.id,
                "type": message_type,
                "title": "服务到期提醒" if "到期" in (log.push_content or "") else ("系统通知" if message_type == "system" else "推送通知"),
                "content": log.push_content or "",
                "time": log.push_time.strftime("%Y-%m-%d %H:%M:%S"),
                "read": log.read  # 返回数据库中存储的已读状态
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取消息列表成功",
                "data": {
                    "total": total,
                    "items": items
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取消息列表失败"
        )


@router.post("/read/{message_id}", response_model=dict)
async def mark_message_as_read(
    message_id: int = Path(..., description="消息ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """标记消息为已读"""
    try:
        # 查找该消息
        push_log = db.query(PushLog).filter(
            PushLog.id == message_id,
            PushLog.user_id == current_user.id
        ).first()
        
        if not push_log:
            raise HTTPException(
                status_code=404,
                detail="消息未找到"
            )
        
        # 标记为已读
        push_log.read = True
        db.commit()
        db.refresh(push_log)
        
        # 同时标记所有未读消息为已读（实现用户需求：点击一个消息，所有小红点消失）
        unread_logs = db.query(PushLog).filter(
            PushLog.user_id == current_user.id,
            PushLog.read == False
        ).all()
        
        for log in unread_logs:
            log.read = True
        
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "标记已读成功",
                "data": None
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="标记已读失败"
        )
