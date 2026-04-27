#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 签到API
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import desc, and_

from core.database import get_db_common
from core.security import get_current_user
from models.users import User
from models.sign_in import SignInRecord, PointsRecord

router = APIRouter(tags=["sign_in"])


@router.post("/sign-in")
async def sign_in(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """用户签到"""
    try:
        today = date.today()
        
        existing_record = db.query(SignInRecord).filter(
            SignInRecord.user_id == current_user.id,
            SignInRecord.sign_date == today
        ).first()
        
        if existing_record:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "今日已签到",
                    "data": {
                        "points_earned": existing_record.points_earned,
                        "continuous_days": existing_record.continuous_days,
                        "sign_date": existing_record.sign_date.isoformat()
                    }
                }
            )
        
        continuous_days = 1
        yesterday = today - timedelta(days=1)
        
        if current_user.last_sign_date:
            last_sign = current_user.last_sign_date.date() if isinstance(current_user.last_sign_date, datetime) else current_user.last_sign_date
            if last_sign == yesterday:
                continuous_days = (current_user.continuous_sign_days or 0) + 1
        
        points_earned = 10
        
        sign_record = SignInRecord(
            user_id=current_user.id,
            sign_date=today,
            points_earned=points_earned,
            continuous_days=continuous_days
        )
        db.add(sign_record)
        
        current_user.points = (current_user.points or 0) + points_earned
        current_user.continuous_sign_days = continuous_days
        current_user.last_sign_date = datetime.now()
        
        points_record = PointsRecord(
            user_id=current_user.id,
            points=points_earned,
            balance=current_user.points,
            type=1,
            description=f"签到获得{points_earned}积分",
            related_id=None
        )
        db.add(points_record)
        
        db.commit()
        db.refresh(sign_record)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "签到成功",
                "data": {
                    "points_earned": points_earned,
                    "continuous_days": continuous_days,
                    "total_points": current_user.points,
                    "sign_date": today.isoformat()
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"签到失败: {str(e)}", "data": None}
        )


@router.get("/sign-in/status")
async def get_sign_in_status(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取签到状态"""
    try:
        today = date.today()
        
        today_record = db.query(SignInRecord).filter(
            SignInRecord.user_id == current_user.id,
            SignInRecord.sign_date == today
        ).first()
        
        total_sign_days = db.query(SignInRecord).filter(
            SignInRecord.user_id == current_user.id
        ).count()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取签到状态成功",
                "data": {
                    "has_signed_today": today_record is not None,
                    "continuous_days": current_user.continuous_sign_days or 0,
                    "total_points": current_user.points or 0,
                    "total_sign_days": total_sign_days,
                    "last_sign_date": current_user.last_sign_date.isoformat() if current_user.last_sign_date else None
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取签到状态失败: {str(e)}", "data": None}
        )


@router.get("/sign-in/records")
async def get_sign_in_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取签到记录"""
    try:
        query = db.query(SignInRecord).filter(SignInRecord.user_id == current_user.id)
        query = query.order_by(desc(SignInRecord.sign_date))
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "sign_date": item.sign_date.isoformat(),
                "points_earned": item.points_earned,
                "continuous_days": item.continuous_days,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取签到记录成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取签到记录失败: {str(e)}", "data": None}
        )


@router.get("/points/records")
async def get_points_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    type: int = Query(None),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取积分记录"""
    try:
        query = db.query(PointsRecord).filter(PointsRecord.user_id == current_user.id)
        
        if type:
            query = query.filter(PointsRecord.type == type)
        
        query = query.order_by(desc(PointsRecord.created_at))
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        type_names = {1: "签到", 2: "兑换", 3: "系统赠送", 4: "消费", 5: "其他"}
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "points": item.points,
                "balance": item.balance,
                "type": item.type,
                "type_name": type_names.get(item.type, "未知"),
                "description": item.description,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取积分记录成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取积分记录失败: {str(e)}", "data": None}
        )
