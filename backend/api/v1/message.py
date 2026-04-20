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
            # 系统通知
            pass  # 暂时不区分，后续可以根据推送内容或类型区分
        elif tab == "info":
            # 情报推送
            pass
        elif tab == "expiry":
            # 到期提醒
            pass
        
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
            elif "系统" in (log.push_content or ""):
                message_type = "system"
            
            items.append({
                "id": log.id,
                "type": message_type,
                "title": "推送通知" if not log.push_content else log.push_content[:30],
                "content": log.push_content or "",
                "time": log.push_time.strftime("%Y-%m-%d %H:%M:%S"),
                "read": False  # 暂时默认未读，后续可以添加已读状态
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
        # 这里可以添加已读状态的逻辑
        # 暂时返回成功
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
