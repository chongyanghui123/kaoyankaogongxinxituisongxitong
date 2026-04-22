#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 用户路由
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, validator

from config import settings
from core.database import get_db_common
from core.security import get_current_user, get_current_admin, get_password_hash, validate_email, validate_phone
from core.logger import log_user_action, log_error

from models.users import User, UserSubscription, UserKeyword, UserReadInfo, UserFavorite
import asyncio

router = APIRouter()

class UserProfileResponse(BaseModel):
    """用户信息响应模型"""
    user_id: int
    username: str
    email: str
    phone: str
    avatar: Optional[str]
    real_name: Optional[str]
    is_admin: bool
    is_vip: bool
    is_trial: bool
    vip_type: int
    vip_end_time: Optional[str]
    created_at: str

class UpdateProfileRequest(BaseModel):
    """更新用户信息请求模型"""
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    avatar: Optional[str] = Field(None, description="头像URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别: 0-未知, 1-男, 2-女")

class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")

class SubscriptionConfig(BaseModel):
    """订阅配置模型"""
    kaoyan: dict
    kaogong: dict
    push: Optional[dict] = Field({}, description="推送配置")

class UpdateSubscriptionRequest(BaseModel):
    """更新订阅配置请求模型"""
    subscribe_type: int = Field(..., ge=1, le=3, description="订阅类型: 1-考研, 2-考公, 3-双赛道")
    config: SubscriptionConfig = Field(..., description="订阅配置")

class AddKeywordRequest(BaseModel):
    """添加关键词请求模型"""
    keyword: str = Field(..., min_length=1, max_length=100, description="关键词")
    category: int = Field(..., ge=1, le=2, description="分类: 1-考研, 2-考公")

class KeywordResponse(BaseModel):
    """关键词响应模型"""
    id: int
    keyword: str
    category: int
    is_active: bool
    created_at: str

class ReadInfoResponse(BaseModel):
    """已读信息响应模型"""
    id: int
    info_id: int
    category: int
    read_time: str

class FavoriteResponse(BaseModel):
    """收藏信息响应模型"""
    id: int
    info_id: int
    category: int
    created_at: str

class UserStatsResponse(BaseModel):
    """用户统计响应模型"""
    total_read: int
    total_favorites: int
    total_keywords: int
    subscription_status: dict

@router.get("/profile", summary="获取用户信息")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取当前用户信息，包括订阅配置"""
    try:
        # 解析类型值
        def parse_requirement_value(value):
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                # 处理字符串格式的数组，如 "['公务员']" 或 "["公务员"]"
                value = value.strip()
                if value.startswith('[') and value.endswith(']'):
                    # 移除首尾的括号
                    value = value[1:-1]
                    # 分割字符串
                    items = []
                    if value:
                        # 处理带引号的字符串
                        if value.startswith("'") and value.endswith("'") or value.startswith('"') and value.endswith('"'):
                            # 单个带引号的字符串
                            items = [value[1:-1].strip()]
                        else:
                            # 多个字符串，用逗号分隔
                            items = [item.strip().strip("'\"") for item in value.split(',') if item.strip()]
                    return items
                else:
                    return [value] if value else []
            else:
                return []
        
        # 获取用户订阅配置
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        kaoyan_requirements = {}
        kaogong_requirements = {}
        
        if subscription and subscription.config_json:
            kaoyan_requirements = subscription.config_json.get("kaoyan", {})
            kaogong_requirements = subscription.config_json.get("kaogong", {})
        
        # 确保字段名与前端一致
        # 处理kaoyan_requirements为None的情况
        if kaoyan_requirements is None:
            kaoyan_requirements = {}
            
        standardized_kaoyan_requirements = {
            "province": ", ".join([str(p) for p in (kaoyan_requirements.get("provinces", []) or [kaoyan_requirements.get("province", "")]) if p]),
            "school": kaoyan_requirements.get("schools", "") or kaoyan_requirements.get("school", ""),
            "major": kaoyan_requirements.get("majors", "") or kaoyan_requirements.get("major", ""),
            "type": ", ".join([str(t) for t in (
                kaoyan_requirements.get("types", []) or parse_requirement_value(kaoyan_requirements.get("type", ""))
            ) if t and str(t).strip()]),
            "keywords": kaoyan_requirements.get("keywords", "")
        }
        
        # 处理kaogong_requirements为None的情况
        if kaogong_requirements is None:
            kaogong_requirements = {}
            
        standardized_kaogong_requirements = {
            "province": ", ".join([str(p) for p in (kaogong_requirements.get("provinces", []) or [kaogong_requirements.get("province", "")]) if p]),
            "major": kaogong_requirements.get("majors", "") or kaogong_requirements.get("major", ""),
            "type": ", ".join([str(t) for t in (
                kaogong_requirements.get("position_types", []) 
                or kaogong_requirements.get("types", []) 
                or parse_requirement_value(kaogong_requirements.get("type", ""))
            ) if t and str(t).strip()]),
            "keywords": kaogong_requirements.get("keywords", "")
        }
        
        # 如果是考公用户，确保返回考公需求信息，即使是空的
        if current_user.vip_type == 2 or current_user.vip_type == 3:
            # 检查是否有考公需求信息，如果没有，返回默认值
            if not standardized_kaogong_requirements.get("province") and \
               not standardized_kaogong_requirements.get("major") and \
               not standardized_kaogong_requirements.get("type") and \
               not standardized_kaogong_requirements.get("keywords"):
                # 这里可以根据需要设置默认值，或者保持原样
                pass
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取用户信息成功",
                "data": {
                    "user_id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                    "phone": current_user.phone,
                    "avatar": current_user.avatar,
                    "real_name": current_user.real_name,
                    "is_admin": current_user.is_admin,
                    "is_vip": current_user.is_vip_active,
                    "is_trial": current_user.is_trial_active,
                    "vip_type": current_user.vip_type,
                    "vip_end_time": current_user.vip_end_time.isoformat() if current_user.vip_end_time else None,
                    "created_at": current_user.created_at.isoformat(),
                    "kaoyan_requirements": standardized_kaoyan_requirements,
                    "kaogong_requirements": standardized_kaogong_requirements
                }
            }
        )
    except Exception as e:
        log_error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

@router.put("/profile", response_model=UserProfileResponse, summary="更新用户信息")
async def update_profile(
    req: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """更新用户信息"""
    try:
        # 更新用户信息
        if req.real_name is not None:
            current_user.real_name = req.real_name
        if req.avatar is not None:
            current_user.avatar = req.avatar
        if req.gender is not None:
            current_user.gender = req.gender
        
        db.commit()
        db.refresh(current_user)
        
        log_user_action(current_user.id, "update_profile", "更新用户信息")
        
        return UserProfileResponse(
            user_id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
            avatar=current_user.avatar,
            real_name=current_user.real_name,
            is_admin=current_user.is_admin,
            is_vip=current_user.is_vip_active,
            is_trial=current_user.is_trial_active,
            vip_type=current_user.vip_type,
            vip_end_time=current_user.vip_end_time.isoformat() if current_user.vip_end_time else None,
            created_at=current_user.created_at.isoformat()
        )
    except Exception as e:
        log_error(f"更新用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户信息失败"
        )

@router.post("/change-password", summary="修改密码")
async def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """修改密码"""
    try:
        from core.security import verify_password
        
        # 验证旧密码
        if not verify_password(req.old_password, current_user.password_hash):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "旧密码错误",
                    "data": None
                }
            )
        
        # 更新密码
        current_user.password_hash = get_password_hash(req.new_password)
        db.commit()
        
        log_user_action(current_user.id, "change_password", "修改密码")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "密码修改成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"修改密码失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "修改密码失败，请稍后重试",
                "data": None
            }
        )

@router.get("/subscription", summary="获取订阅配置")
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户订阅配置"""
    try:
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        if not subscription:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "订阅配置不存在",
                    "data": None
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取订阅配置成功",
                "data": {
                    "subscribe_type": subscription.subscribe_type,
                    "status": subscription.status,
                    "config": subscription.config_json,
                    "created_at": subscription.created_at.isoformat(),
                    "updated_at": subscription.updated_at.isoformat()
                }
            }
        )
    except Exception as e:
        log_error(f"获取订阅配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取订阅配置失败，请稍后重试",
                "data": None
            }
        )

@router.put("/subscription", summary="更新订阅配置")
async def update_subscription(
    req: UpdateSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """更新用户订阅配置"""
    try:
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        if not subscription:
            # 创建新的订阅配置
            subscription = UserSubscription(
                user_id=current_user.id,
                subscribe_type=req.subscribe_type,
                status=1,
                config_json={
                    "kaoyan": req.config.kaoyan,
                    "kaogong": req.config.kaogong,
                    "push": req.config.push or {}
                }
            )
            db.add(subscription)
        else:
            # 更新现有配置
            subscription.subscribe_type = req.subscribe_type
            # 保留原有的推送配置（如果请求中没有提供）
            existing_push_config = subscription.config_json.get("push", {})
            subscription.config_json = {
                "kaoyan": req.config.kaoyan,
                "kaogong": req.config.kaogong,
                "push": req.config.push or existing_push_config
            }
        
        db.commit()
        db.refresh(subscription)
        

        
        log_user_action(current_user.id, "update_subscription", f"更新订阅配置: 类型{req.subscribe_type}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "更新订阅配置成功",
                "data": {
                    "subscribe_type": subscription.subscribe_type,
                    "status": subscription.status,
                    "config": subscription.config_json,
                    "updated_at": subscription.updated_at.isoformat()
                }
            }
        )
    except Exception as e:
        log_error(f"更新订阅配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "更新订阅配置失败，请稍后重试",
                "data": None
            }
        )

@router.get("/keywords", response_model=List[KeywordResponse], summary="获取关键词列表")
async def get_keywords(
    category: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户关键词列表"""
    try:
        query = db.query(UserKeyword).filter(UserKeyword.user_id == current_user.id)
        
        if category:
            query = query.filter(UserKeyword.category == category)
        
        keywords = query.all()
        
        return [
            KeywordResponse(
                id=kw.id,
                keyword=kw.keyword,
                category=kw.category,
                is_active=kw.is_active,
                created_at=kw.created_at.isoformat()
            )
            for kw in keywords
        ]
    except Exception as e:
        log_error(f"获取关键词列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取关键词列表失败"
        )

@router.post("/keywords", response_model=KeywordResponse, summary="添加关键词")
async def add_keyword(
    req: AddKeywordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """添加用户关键词"""
    try:
        # 检查关键词是否已存在
        existing_keyword = db.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.keyword == req.keyword,
            UserKeyword.category == req.category
        ).first()
        
        if existing_keyword:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "关键词已存在",
                    "data": None
                }
            )
        
        # 创建新关键词
        new_keyword = UserKeyword(
            user_id=current_user.id,
            keyword=req.keyword,
            category=req.category,
            is_active=True
        )
        
        db.add(new_keyword)
        db.commit()
        db.refresh(new_keyword)
        
        log_user_action(current_user.id, "add_keyword", f"添加关键词: {req.keyword}")
        
        return KeywordResponse(
            id=new_keyword.id,
            keyword=new_keyword.keyword,
            category=new_keyword.category,
            is_active=new_keyword.is_active,
            created_at=new_keyword.created_at.isoformat()
        )
    except Exception as e:
        log_error(f"添加关键词失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "添加关键词失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/keywords/{keyword_id}", summary="删除关键词")
async def delete_keyword(
    keyword_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """删除用户关键词"""
    try:
        keyword = db.query(UserKeyword).filter(
            UserKeyword.id == keyword_id,
            UserKeyword.user_id == current_user.id
        ).first()
        
        if not keyword:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "关键词不存在",
                    "data": None
                }
            )
        
        db.delete(keyword)
        db.commit()
        
        log_user_action(current_user.id, "delete_keyword", f"删除关键词: {keyword.keyword}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "删除关键词成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除关键词失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "删除关键词失败，请稍后重试",
                "data": None
            }
        )

@router.get("/read-info", response_model=List[ReadInfoResponse], summary="获取已读信息")
async def get_read_info(
    category: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户已读信息列表"""
    try:
        query = db.query(UserReadInfo).filter(UserReadInfo.user_id == current_user.id)
        
        if category:
            query = query.filter(UserReadInfo.category == category)
        
        read_info = query.order_by(UserReadInfo.read_time.desc()).all()
        
        return [
            ReadInfoResponse(
                id=ri.id,
                info_id=ri.info_id,
                category=ri.category,
                read_time=ri.read_time.isoformat()
            )
            for ri in read_info
        ]
    except Exception as e:
        log_error(f"获取已读信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取已读信息失败"
        )

@router.get("/favorites", summary="获取收藏信息")
async def get_favorites(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户收藏信息列表（根据用户类型自动判断）"""
    try:
        # 确定用户类型
        user_type = None
        if current_user.vip_type == 1:  # 考研VIP
            user_type = 1
        elif current_user.vip_type == 2:  # 考公VIP
            user_type = 2
        else:
            # 非VIP用户或双赛道用户，检查订阅类型
            user_subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == current_user.id
            ).first()
            
            if user_subscription:
                user_type = user_subscription.subscribe_type
            else:
                user_type = 3  # 默认双赛道
        
        # 构建查询
        query = db.query(UserFavorite).filter(UserFavorite.user_id == current_user.id)
        
        # 根据用户类型过滤收藏内容
        if user_type == 1:  # 考研用户只显示考研收藏
            query = query.filter(UserFavorite.category == 1)
        elif user_type == 2:  # 考公用户只显示考公收藏
            query = query.filter(UserFavorite.category == 2)
        # 双赛道用户显示所有收藏
        
        # 计算总数
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        favorites = query.order_by(UserFavorite.created_at.desc()).offset(offset).limit(page_size).all()
        
        # 获取收藏内容的详情
        from models.kaoyan import KaoyanInfo
        from models.kaogong import KaogongInfo
        
        result = []
        for fav in favorites:
            favorite_data = {
                "id": fav.id,
                "info_id": fav.info_id,
                "category": fav.category,
                "created_at": fav.created_at.isoformat()
            }
            
            # 根据分类获取内容详情
            if fav.category == 1:  # 考研
                info = db.query(KaoyanInfo).filter(KaoyanInfo.id == fav.info_id).first()
                if info:
                    favorite_data["title"] = info.title
                    favorite_data["summary"] = info.summary
                    favorite_data["publish_time"] = info.publish_time.isoformat()
            elif fav.category == 2:  # 考公
                info = db.query(KaogongInfo).filter(KaogongInfo.id == fav.info_id).first()
                if info:
                    favorite_data["title"] = info.title
                    favorite_data["summary"] = info.summary
                    favorite_data["publish_time"] = info.publish_time.isoformat()
            
            result.append(favorite_data)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取收藏信息成功",
                "data": {
                    "total": total,
                    "items": result
                }
            }
        )
    except Exception as e:
        log_error(f"获取收藏信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取收藏信息失败"
        )

@router.post("/favorites/{info_id}/{category}", summary="添加收藏")
async def add_favorite(
    info_id: int,
    category: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """添加收藏信息"""
    try:
        # 检查是否已收藏
        existing_favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.info_id == info_id,
            UserFavorite.category == category
        ).first()
        
        if existing_favorite:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "已收藏",
                    "data": None
                }
            )
        
        # 创建收藏
        new_favorite = UserFavorite(
            user_id=current_user.id,
            info_id=info_id,
            category=category
        )
        
        db.add(new_favorite)
        db.commit()
        
        log_user_action(current_user.id, "add_favorite", f"添加收藏: 信息ID={info_id}, 分类={category}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "收藏成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"添加收藏失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "添加收藏失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/favorites/{info_id}/{category}", summary="取消收藏")
async def remove_favorite(
    info_id: int,
    category: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """取消收藏信息"""
    try:
        favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.info_id == info_id,
            UserFavorite.category == category
        ).first()
        
        if not favorite:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "收藏不存在",
                    "data": None
                }
            )
        
        db.delete(favorite)
        db.commit()
        
        log_user_action(current_user.id, "remove_favorite", f"取消收藏: 信息ID={info_id}, 分类={category}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "取消收藏成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"取消收藏失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "取消收藏失败，请稍后重试",
                "data": None
            }
        )

@router.get("/stats", response_model=UserStatsResponse, summary="获取用户统计信息")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户统计信息"""
    try:
        # 统计已读信息数量
        total_read = db.query(UserReadInfo).filter(
            UserReadInfo.user_id == current_user.id
        ).count()
        
        # 统计收藏信息数量
        total_favorites = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id
        ).count()
        
        # 统计关键词数量
        total_keywords = db.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id
        ).count()
        
        # 获取订阅状态
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        subscription_status = {
            "subscribe_type": subscription.subscribe_type if subscription else 0,
            "status": subscription.status if subscription else 0,
            "updated_at": subscription.updated_at.isoformat() if subscription else None
        }
        
        return UserStatsResponse(
            total_read=total_read,
            total_favorites=total_favorites,
            total_keywords=total_keywords,
            subscription_status=subscription_status
        )
    except Exception as e:
        log_error(f"获取用户统计信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户统计信息失败"
        )


@router.get("/{user_id}", dependencies=[Depends(get_current_admin)])
async def get_user(
    user_id: int,
    db: Session = Depends(get_db_common)
):
    """根据用户ID获取用户信息（管理员）"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "用户不存在",
                    "data": None
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取用户信息成功",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "is_admin": user.is_admin,
                    "is_vip": user.is_vip,
                    "vip_start_time": user.vip_start_time.isoformat() if user.vip_start_time else None,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "vip_type": user.vip_type,
                    "created_at": user.created_at.isoformat()
                }
            }
        )
    except Exception as e:
        log_error(f"获取用户信息失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取用户信息失败",
                "data": None
            }
        )