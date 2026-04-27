#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 礼品兑换API
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi.responses import JSONResponse
from sqlalchemy import desc
import os

from core.database import get_db_common
from core.security import get_current_user, get_current_admin
from models.users import User
from models.sign_in import PointsRecord
from models.gift import Gift, GiftExchange

router = APIRouter(tags=["gift"])


@router.get("/gifts")
async def get_gifts(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取礼品列表（用户端）"""
    try:
        gifts = db.query(Gift).filter(
            Gift.is_active == True,
            Gift.stock > 0
        ).order_by(Gift.sort_order, desc(Gift.created_at)).all()
        
        result = []
        for gift in gifts:
            result.append({
                "id": gift.id,
                "name": gift.name,
                "description": gift.description,
                "image_url": gift.image_url,
                "points_required": gift.points_required,
                "stock": gift.stock,
                "exchanged_count": gift.exchanged_count
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取礼品列表成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取礼品列表失败: {str(e)}", "data": None}
        )


@router.post("/gifts/{gift_id}/exchange")
async def exchange_gift(
    gift_id: int = Path(...),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """兑换礼品"""
    try:
        # 检查用户是否已填写收货地址
        if not current_user.real_name or not current_user.phone or not current_user.address:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False, 
                    "code": 400, 
                    "message": "请先在设置页面填写收货地址",
                    "data": {"need_address": True}
                }
            )
        
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if not gift:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "礼品不存在", "data": None}
            )
        
        if not gift.is_active:
            return JSONResponse(
                status_code=400,
                content={"success": False, "code": 400, "message": "礼品已下架", "data": None}
            )
        
        if gift.stock <= 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "code": 400, "message": "礼品库存不足", "data": None}
            )
        
        if (current_user.points or 0) < gift.points_required:
            return JSONResponse(
                status_code=400,
                content={"success": False, "code": 400, "message": f"积分不足，需要{gift.points_required}积分", "data": None}
            )
        
        current_user.points = (current_user.points or 0) - gift.points_required
        gift.stock -= 1
        gift.exchanged_count += 1
        
        exchange = GiftExchange(
            user_id=current_user.id,
            gift_id=gift.id,
            points_used=gift.points_required,
            status=0
        )
        db.add(exchange)
        
        points_record = PointsRecord(
            user_id=current_user.id,
            points=-gift.points_required,
            balance=current_user.points,
            type=2,
            description=f"兑换礼品: {gift.name}",
            related_id=exchange.id
        )
        db.add(points_record)
        
        db.commit()
        db.refresh(exchange)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "兑换成功",
                "data": {
                    "exchange_id": exchange.id,
                    "gift_name": gift.name,
                    "points_used": gift.points_required,
                    "remaining_points": current_user.points
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"兑换失败: {str(e)}", "data": None}
        )


@router.get("/exchanges")
async def get_my_exchanges(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取我的兑换记录"""
    try:
        query = db.query(GiftExchange).filter(GiftExchange.user_id == current_user.id)
        query = query.order_by(desc(GiftExchange.created_at))
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        status_names = {0: "待处理", 1: "已发货", 2: "已完成", 3: "已取消"}
        
        result = []
        for item in items:
            gift = db.query(Gift).filter(Gift.id == item.gift_id).first()
            result.append({
                "id": item.id,
                "gift_id": item.gift_id,
                "gift_name": gift.name if gift else "未知礼品",
                "gift_image": gift.image_url if gift else None,
                "points_used": item.points_used,
                "status": item.status,
                "status_name": status_names.get(item.status, "未知"),
                "tracking_number": item.tracking_number,
                "remark": item.remark,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取兑换记录成功",
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
            content={"success": False, "code": 500, "message": f"获取兑换记录失败: {str(e)}", "data": None}
        )


@router.get("/admin/gifts")
async def admin_get_gifts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_active: Optional[str] = Query(None),
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """获取礼品列表（管理员）"""
    try:
        query = db.query(Gift)
        
        if is_active is not None and is_active != "":
            if is_active.lower() in ("true", "1", "yes"):
                query = query.filter(Gift.is_active == True)
            elif is_active.lower() in ("false", "0", "no"):
                query = query.filter(Gift.is_active == False)
        
        query = query.order_by(Gift.sort_order, desc(Gift.created_at))
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        result = []
        for gift in items:
            result.append({
                "id": gift.id,
                "name": gift.name,
                "description": gift.description,
                "image_url": gift.image_url,
                "points_required": gift.points_required,
                "stock": gift.stock,
                "exchanged_count": gift.exchanged_count,
                "is_active": gift.is_active,
                "sort_order": gift.sort_order,
                "created_at": gift.created_at.isoformat() if gift.created_at else None
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取礼品列表成功",
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
            content={"success": False, "code": 500, "message": f"获取礼品列表失败: {str(e)}", "data": None}
        )


@router.post("/admin/gifts")
async def admin_create_gift(
    name: str = Form(...),
    description: str = Form(None),
    points_required: int = Form(...),
    stock: int = Form(0),
    is_active: bool = Form(True),
    sort_order: int = Form(0),
    image: UploadFile = File(None),
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """创建礼品（管理员）"""
    try:
        image_url = None
        if image:
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "gifts")
            os.makedirs(upload_dir, exist_ok=True)
            
            import time
            filename = f"{int(time.time())}_{image.filename}"
            file_path = os.path.join(upload_dir, filename)
            
            with open(file_path, "wb") as f:
                content = await image.read()
                f.write(content)
            
            image_url = f"/uploads/gifts/{filename}"
        
        gift = Gift(
            name=name,
            description=description,
            image_url=image_url,
            points_required=points_required,
            stock=stock,
            is_active=is_active,
            sort_order=sort_order
        )
        db.add(gift)
        db.commit()
        db.refresh(gift)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "创建礼品成功",
                "data": {
                    "id": gift.id,
                    "name": gift.name,
                    "image_url": gift.image_url,
                    "points_required": gift.points_required
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"创建礼品失败: {str(e)}", "data": None}
        )


@router.put("/admin/gifts/{gift_id}")
async def admin_update_gift(
    gift_id: int = Path(...),
    name: str = Form(None),
    description: str = Form(None),
    points_required: int = Form(None),
    stock: int = Form(None),
    is_active: bool = Form(None),
    sort_order: int = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """更新礼品（管理员）"""
    try:
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if not gift:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "礼品不存在", "data": None}
            )
        
        if name is not None:
            gift.name = name
        if description is not None:
            gift.description = description
        if points_required is not None:
            gift.points_required = points_required
        if stock is not None:
            gift.stock = stock
        if is_active is not None:
            gift.is_active = is_active
        if sort_order is not None:
            gift.sort_order = sort_order
        
        if image:
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "gifts")
            os.makedirs(upload_dir, exist_ok=True)
            
            import time
            filename = f"{int(time.time())}_{image.filename}"
            file_path = os.path.join(upload_dir, filename)
            
            with open(file_path, "wb") as f:
                content = await image.read()
                f.write(content)
            
            gift.image_url = f"/uploads/gifts/{filename}"
        
        db.commit()
        db.refresh(gift)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新礼品成功",
                "data": {
                    "id": gift.id,
                    "name": gift.name,
                    "image_url": gift.image_url
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新礼品失败: {str(e)}", "data": None}
        )


@router.delete("/admin/gifts/{gift_id}")
async def admin_delete_gift(
    gift_id: int = Path(...),
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """删除礼品（管理员）"""
    try:
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if not gift:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "礼品不存在", "data": None}
            )
        
        db.delete(gift)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除礼品成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除礼品失败: {str(e)}", "data": None}
        )


@router.get("/admin/exchanges")
async def admin_get_exchanges(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[int] = Query(None),
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """获取兑换记录列表（管理员）"""
    try:
        query = db.query(GiftExchange).join(User).filter(User.is_admin == False)
        
        if status is not None:
            query = query.filter(GiftExchange.status == status)
        
        query = query.order_by(desc(GiftExchange.created_at))
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        status_names = {0: "待处理", 1: "已发货", 2: "已完成", 3: "已取消"}
        
        result = []
        for item in items:
            user = db.query(User).filter(User.id == item.user_id).first()
            gift = db.query(Gift).filter(Gift.id == item.gift_id).first()
            result.append({
                "id": item.id,
                "user_id": item.user_id,
                "username": user.username if user else "未知用户",
                "gift_id": item.gift_id,
                "gift_name": gift.name if gift else "未知礼品",
                "points_used": item.points_used,
                "status": item.status,
                "status_name": status_names.get(item.status, "未知"),
                "tracking_number": item.tracking_number,
                "remark": item.remark,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取兑换记录成功",
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
            content={"success": False, "code": 500, "message": f"获取兑换记录失败: {str(e)}", "data": None}
        )


@router.put("/admin/exchanges/{exchange_id}")
async def admin_update_exchange(
    exchange_id: int = Path(...),
    exchange_data: dict = None,
    db: Session = Depends(get_db_common),
    current_admin: User = Depends(get_current_admin)
):
    """更新兑换记录状态（管理员）"""
    try:
        exchange = db.query(GiftExchange).filter(GiftExchange.id == exchange_id).first()
        if not exchange:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "兑换记录不存在", "data": None}
            )
        
        if "status" in exchange_data:
            exchange.status = exchange_data["status"]
        if "tracking_number" in exchange_data:
            exchange.tracking_number = exchange_data["tracking_number"]
        if "remark" in exchange_data:
            exchange.remark = exchange_data["remark"]
        
        db.commit()
        db.refresh(exchange)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新兑换记录成功",
                "data": {
                    "id": exchange.id,
                    "status": exchange.status
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新兑换记录失败: {str(e)}", "data": None}
        )
