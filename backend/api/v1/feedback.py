from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from core.database import get_db
from core.security import get_current_user
from models.users import User
from models.feedback import Feedback, FeedbackType, FeedbackStatus

router = APIRouter(tags=["feedback"])


# 反馈请求模型
class FeedbackCreate(BaseModel):
    type: int  # 1: 功能建议, 2: 问题反馈, 3: 其他
    content: str
    contact: str = None


# 反馈响应模型
class FeedbackResponse(BaseModel):
    id: int
    type: int
    content: str
    contact: str = None
    status: str
    reply: str = None
    reply_at: str = None
    created_at: str
    user_id: int

    class Config:
        from_attributes = True


# 提交反馈
@router.post("")
async def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 验证反馈类型
    if feedback.type not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的反馈类型"
        )
    
    # 创建反馈
    db_feedback = Feedback(
        user_id=current_user.id,
        type=FeedbackType(feedback.type),
        content=feedback.content,
        contact=feedback.contact,
        status=FeedbackStatus.PENDING
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return {
        "success": True,
        "message": "反馈提交成功",
        "data": {
            "id": db_feedback.id,
            "type": db_feedback.type.value,
            "content": db_feedback.content,
            "contact": db_feedback.contact,
            "status": db_feedback.status.value,
            "created_at": db_feedback.created_at.isoformat(),
            "user_id": db_feedback.user_id
        }
    }


# 获取用户的反馈历史
@router.get("")
async def get_user_feedbacks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    feedbacks = db.query(Feedback).filter(
        Feedback.user_id == current_user.id,
        Feedback.is_deleted_by_user == False
    ).order_by(Feedback.created_at.desc()).all()
    
    return {
        "success": True,
        "message": "获取反馈列表成功",
        "data": [
            {
                "id": fb.id,
                "type": fb.type.value,
                "content": fb.content,
                "contact": fb.contact,
                "status": fb.status.value,
                "reply": fb.reply,
                "reply_at": fb.reply_at.isoformat() if fb.reply_at else None,
                "created_at": fb.created_at.isoformat(),
                "user_id": fb.user_id
            }
            for fb in feedbacks
        ]
    }


# 管理员获取所有反馈
@router.get("/admin")
async def get_all_feedbacks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 验证管理员权限
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限访问"
        )
    
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    
    # 获取所有用户ID
    user_ids = [fb.user_id for fb in feedbacks]
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    user_dict = {user.id: user.username for user in users}
    
    return {
        "success": True,
        "message": "获取反馈列表成功",
        "data": [
            {
                "id": fb.id,
                "type": fb.type.value,
                "content": fb.content,
                "contact": fb.contact,
                "status": fb.status.value,
                "reply": fb.reply,
                "reply_at": fb.reply_at.isoformat() if fb.reply_at else None,
                "created_at": fb.created_at.isoformat(),
                "user_id": fb.user_id,
                "username": user_dict.get(fb.user_id, "未知用户")
            }
            for fb in feedbacks
        ]
    }


# 管理员更新反馈状态
@router.put("/{feedback_id}/status")
async def update_feedback_status(
    feedback_id: int,
    request_body: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 验证管理员权限
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限访问"
        )
    
    # 从请求体中获取状态
    status = request_body.get("status")
    
    # 验证状态值
    if status not in ["pending", "processed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的状态值"
        )
    
    # 查找反馈
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 更新状态
    feedback.status = FeedbackStatus(status)
    db.commit()
    
    return {
        "success": True,
        "message": "状态更新成功",
        "data": {
            "id": feedback.id,
            "status": feedback.status.value
        }
    }


# 管理员回复反馈
@router.put("/{feedback_id}/reply")
async def reply_feedback(
    feedback_id: int,
    request_body: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 验证管理员权限
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限访问"
        )
    
    # 从请求体中获取回复内容
    reply = request_body.get("reply")
    
    if not reply or not reply.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="回复内容不能为空"
        )
    
    # 查找反馈
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 更新回复和状态
    feedback.reply = reply.strip()
    feedback.reply_at = datetime.now()
    feedback.status = FeedbackStatus.PROCESSED
    db.commit()
    
    return {
        "success": True,
        "message": "回复成功",
        "data": {
            "id": feedback.id,
            "reply": feedback.reply,
            "reply_at": feedback.reply_at.isoformat(),
            "status": feedback.status.value
        }
    }


# 用户撤回反馈（仅限待处理状态的反馈）
@router.put("/{feedback_id}/withdraw")
async def withdraw_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 查找反馈
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 验证是否为反馈的所有者
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限撤回此反馈"
        )
    
    # 验证反馈状态是否为待处理
    if feedback.status != FeedbackStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能撤回待处理状态的反馈"
        )
    
    # 删除反馈
    db.delete(feedback)
    db.commit()
    
    return {
        "success": True,
        "message": "反馈撤回成功"
    }


# 删除反馈（用户和管理员都可以使用）
@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 查找反馈
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 验证权限：管理员只能删除已回复的反馈，用户只能删除自己的已处理反馈
    if current_user.is_admin:
        # 管理员只能删除已回复的反馈
        if not feedback.reply:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只能删除已回复的反馈"
            )
        
        # 管理员真正删除反馈
        db.delete(feedback)
        db.commit()
        
        return {
            "success": True,
            "message": "反馈删除成功"
        }
    else:
        # 用户只能删除自己的已处理反馈
        if feedback.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此反馈"
            )
        
        # 用户只能删除已处理的反馈
        if feedback.status != FeedbackStatus.PROCESSED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只能删除已处理的反馈"
            )
        
        # 用户只标记为删除，不真正删除
        feedback.is_deleted_by_user = True
        db.commit()
        
        return {
            "success": True,
            "message": "反馈删除成功"
        }
