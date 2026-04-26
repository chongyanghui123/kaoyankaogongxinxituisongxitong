#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 考公路由
"""

from datetime import datetime
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from pydantic import BaseModel, Field

from config import settings
from core.database import get_db_kaogong, get_db_common
from core.security import get_current_user
from core.logger import log_user_action, log_error
from models.kaogong import KaogongInfo
from models.users import UserReadInfo, UserFavorite, PushLog, User, UserSubscription, UserKeyword
from api.v1.sync_helpers import sync_get_user_requirements

router = APIRouter()

def get_info_user_requirements(info_id: int, category: int, db_common: Session):
    """获取情报对应的用户需求信息"""
    try:
        # 暂时返回空列表，避免查询所有活跃用户导致的性能问题
        return []
    except Exception as e:
        log_error(f"获取情报{info_id}用户需求信息失败: {str(e)}")
        return []

class KaogongInfoResponse(BaseModel):
    """考公信息响应模型"""
    id: int
    title: str
    source: str
    source_url: Optional[str]
    publish_time: str
    content: Optional[str]
    url: str
    tags: Optional[str]
    urgency_level: int
    urgency_text: str
    category: int
    category_text: str
    province: Optional[str]
    position_type: Optional[str]
    major: Optional[str]
    education: Optional[str]
    is_fresh_graduate: Optional[bool]
    is_fresh_graduate_text: str
    is_unlimited: Optional[bool]
    is_unlimited_text: str
    competition_ratio: Optional[float]
    is_valid: bool
    is_top: bool
    is_excellent: bool
    view_count: int
    like_count: int
    is_processed: bool
    created_at: str
    is_read: bool = False
    is_favorite: bool = False
    user_requirements: Optional[List[Dict]] = []

class KaogongInfoListResponse(BaseModel):
    """考公信息列表响应模型"""
    total: int
    items: List[KaogongInfoResponse]

@router.get("/info/list", response_model=KaogongInfoListResponse, summary="获取考公信息列表")
async def get_kaogong_info_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[int] = Query(None, ge=0, le=7, description="分类"),
    province: Optional[str] = Query(None, description="省份"),
    position_type: Optional[str] = Query(None, description="岗位类别"),
    major: Optional[str] = Query(None, description="专业"),
    education: Optional[str] = Query(None, description="学历要求"),
    is_fresh_graduate: Optional[bool] = Query(None, description="是否应届生岗"),
    is_unlimited: Optional[bool] = Query(None, description="是否三不限"),
    urgency_level: Optional[int] = Query(None, ge=0, le=3, description="紧急度"),
    keyword: Optional[str] = Query(None, description="关键词"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common)
):
    """获取考公信息列表"""
    try:
        # 构建查询
        query = db.query(KaogongInfo).filter(KaogongInfo.is_valid == True)
        
        # 过滤条件
        if category is not None:
            query = query.filter(KaogongInfo.category == category)
        if province:
            query = query.filter(KaogongInfo.province == province)
        if position_type:
            query = query.filter(KaogongInfo.position_type.like(f"%{position_type}%"))
        if major:
            query = query.filter(KaogongInfo.major.like(f"%{major}%"))
        if education:
            query = query.filter(KaogongInfo.education.like(f"%{education}%"))
        if is_fresh_graduate is not None:
            query = query.filter(KaogongInfo.is_fresh_graduate == is_fresh_graduate)
        if is_unlimited is not None:
            query = query.filter(KaogongInfo.is_unlimited == is_unlimited)
        if urgency_level is not None:
            query = query.filter(KaogongInfo.urgency_level == urgency_level)
        if keyword:
            query = query.filter(
                or_(
                    KaogongInfo.title.like(f"%{keyword}%"),
                    KaogongInfo.content.like(f"%{keyword}%"),
                    KaogongInfo.tags.like(f"%{keyword}%")
                )
            )
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        info_list = query.order_by(
            desc(KaogongInfo.is_top),
            desc(KaogongInfo.is_excellent),
            desc(KaogongInfo.publish_time)
        ).offset(offset).limit(page_size).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 2  # 2-考公
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 2  # 2-考公
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in info_list:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 2, db_common)
            
            items.append(KaogongInfoResponse(
                id=info.id,
                title=info.title,
                source=info.source,
                source_url=info.source_url,
                publish_time=info.publish_time.isoformat(),
                content=info.content,
                url=info.url,
                tags=info.tags,
                urgency_level=info.urgency_level,
                urgency_text=info.urgency_text,
                category=info.category,
                category_text=info.category_text,
                province=info.province,
                position_type=info.position_type,
                major=info.major,
                education=info.education,
                is_fresh_graduate=info.is_fresh_graduate,
                is_fresh_graduate_text=info.is_fresh_graduate_text,
                is_unlimited=info.is_unlimited,
                is_unlimited_text=info.is_unlimited_text,
                competition_ratio=info.competition_ratio,
                is_valid=info.is_valid,
                is_top=info.is_top,
                is_excellent=info.is_excellent,
                view_count=info.view_count,
                like_count=info.like_count,
                is_processed=info.is_processed,
                created_at=info.created_at.isoformat(),
                is_read=info.id in user_read_ids,
                is_favorite=info.id in user_favorite_ids,
                user_requirements=user_requirements
            ))
        
        return KaogongInfoListResponse(total=total, items=items)
    except Exception as e:
        log_error(f"获取考公信息列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考公信息列表失败"
        )

@router.get("/info/detail/{info_id}", response_model=KaogongInfoResponse, summary="获取考公信息详情")
async def get_kaogong_info_detail(
    info_id: int,
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common)
):
    """获取考公信息详情"""
    try:
        # 获取信息
        info = db.query(KaogongInfo).filter(
            KaogongInfo.id == info_id,
            KaogongInfo.is_valid == True
        ).first()
        
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="信息不存在"
            )
        
        # 增加浏览次数
        info.view_count += 1
        db.commit()
        
        # 标记为已读
        if current_user:
            existing_read = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.info_id == info_id,
                UserReadInfo.category == 2  # 2-考公
            ).first()
            
            if not existing_read:
                new_read = UserReadInfo(
                    user_id=current_user.id,
                    info_id=info_id,
                    category=2
                )
                db_common.add(new_read)
                db_common.commit()
        
        # 检查是否收藏
        is_favorite = False
        if current_user:
            favorite = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.info_id == info_id,
                UserFavorite.category == 2  # 2-考公
            ).first()
            is_favorite = favorite is not None
        
        # 获取用户需求信息
        user_requirements = get_info_user_requirements(info.id, 2, db_common)
        
        return KaogongInfoResponse(
            id=info.id,
            title=info.title,
            source=info.source,
            source_url=info.source_url,
            publish_time=info.publish_time.isoformat(),
            content=info.content,
            url=info.url,
            tags=info.tags,
            urgency_level=info.urgency_level,
            urgency_text=info.urgency_text,
            category=info.category,
            category_text=info.category_text,
            province=info.province,
            position_type=info.position_type,
            major=info.major,
            education=info.education,
            is_fresh_graduate=info.is_fresh_graduate,
            is_fresh_graduate_text=info.is_fresh_graduate_text,
            is_unlimited=info.is_unlimited,
            is_unlimited_text=info.is_unlimited_text,
            competition_ratio=info.competition_ratio,
            is_valid=info.is_valid,
            is_top=info.is_top,
            is_excellent=info.is_excellent,
            view_count=info.view_count,
            like_count=info.like_count,
            is_processed=info.is_processed,
            created_at=info.created_at.isoformat(),
            is_read=True,
            is_favorite=is_favorite,
            user_requirements=user_requirements
        )
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"获取考公信息详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考公信息详情失败"
        )

@router.post("/info/like/{info_id}", summary="点赞考公信息")
async def like_kaogong_info(
    info_id: int,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong)
):
    """点赞考公信息"""
    try:
        info = db.query(KaogongInfo).filter(
            KaogongInfo.id == info_id,
            KaogongInfo.is_valid == True
        ).first()
        
        if not info:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "信息不存在",
                    "data": None
                }
            )
        
        # 增加点赞次数
        info.like_count += 1
        db.commit()
        
        log_user_action(current_user.id, "like_kaogong_info", f"点赞考公信息: ID={info_id}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "点赞成功",
                "data": {
                    "like_count": info.like_count
                }
            }
        )
    except Exception as e:
        log_error(f"点赞考公信息失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "点赞失败，请稍后重试",
                "data": None
            }
        )

@router.get("/info/hot", response_model=List[KaogongInfoResponse], summary="获取热门考公信息")
async def get_hot_kaogong_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common)
):
    """获取热门考公信息（按浏览量排序）"""
    try:
        # 获取热门信息
        hot_info = db.query(KaogongInfo).filter(
            KaogongInfo.is_valid == True
        ).order_by(
            desc(KaogongInfo.view_count),
            desc(KaogongInfo.publish_time)
        ).limit(limit).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 2  # 2-考公
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 2  # 2-考公
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in hot_info:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 2, db_common)
            
            items.append(KaogongInfoResponse(
                id=info.id,
                title=info.title,
                source=info.source,
                source_url=info.source_url,
                publish_time=info.publish_time.isoformat(),
                content=info.content,
                url=info.url,
                tags=info.tags,
                urgency_level=info.urgency_level,
                urgency_text=info.urgency_text,
                category=info.category,
                category_text=info.category_text,
                province=info.province,
                position_type=info.position_type,
                major=info.major,
                education=info.education,
                is_fresh_graduate=info.is_fresh_graduate,
                is_fresh_graduate_text=info.is_fresh_graduate_text,
                is_unlimited=info.is_unlimited,
                is_unlimited_text=info.is_unlimited_text,
                competition_ratio=info.competition_ratio,
                is_valid=info.is_valid,
                is_top=info.is_top,
                is_excellent=info.is_excellent,
                view_count=info.view_count,
                like_count=info.like_count,
                is_processed=info.is_processed,
                created_at=info.created_at.isoformat(),
                is_read=info.id in user_read_ids,
                is_favorite=info.id in user_favorite_ids,
                user_requirements=user_requirements
            ))
        
        return items
    except Exception as e:
        log_error(f"获取热门考公信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取热门考公信息失败"
        )

class DeleteAllKaogongInfoRequest(BaseModel):
    """删除所有考公信息请求模型"""
    pass

@router.delete("/delete-all", summary="删除所有考公信息")
async def delete_all_kaogong_info(
    request: DeleteAllKaogongInfoRequest,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong)
):
    """删除所有考公信息"""
    try:
        # 删除所有考公信息
        db.query(KaogongInfo).delete()
        db.commit()
        
        log_user_action(current_user.id, "delete_all_kaogong_info", "删除所有考公信息")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "所有考公信息删除成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除所有考公信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除所有考公信息失败，请稍后重试"
        )

@router.get("/info/latest", response_model=List[KaogongInfoResponse], summary="获取最新考公信息")
async def get_latest_kaogong_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common)
):
    """获取最新考公信息"""
    try:
        # 获取最新信息
        latest_info = db.query(KaogongInfo).filter(
            KaogongInfo.is_valid == True
        ).order_by(
            desc(KaogongInfo.publish_time)
        ).limit(limit).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 2  # 2-考公
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 2  # 2-考公
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in latest_info:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 2, db_common)
            
            items.append(KaogongInfoResponse(
                id=info.id,
                title=info.title,
                source=info.source,
                source_url=info.source_url,
                publish_time=info.publish_time.isoformat(),
                content=info.content,
                url=info.url,
                tags=info.tags,
                urgency_level=info.urgency_level,
                urgency_text=info.urgency_text,
                category=info.category,
                category_text=info.category_text,
                province=info.province,
                position_type=info.position_type,
                major=info.major,
                education=info.education,
                is_fresh_graduate=info.is_fresh_graduate,
                is_fresh_graduate_text=info.is_fresh_graduate_text,
                is_unlimited=info.is_unlimited,
                is_unlimited_text=info.is_unlimited_text,
                competition_ratio=info.competition_ratio,
                is_valid=info.is_valid,
                is_top=info.is_top,
                is_excellent=info.is_excellent,
                view_count=info.view_count,
                like_count=info.like_count,
                is_processed=info.is_processed,
                created_at=info.created_at.isoformat(),
                is_read=info.id in user_read_ids,
                is_favorite=info.id in user_favorite_ids,
                user_requirements=user_requirements
            ))
        
        return items
    except Exception as e:
        log_error(f"获取最新考公信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取最新考公信息失败"
        )

@router.get("/provinces", summary="获取考公省份列表")
async def get_kaogong_provinces(
    db: Session = Depends(get_db_kaogong)
):
    """获取考公省份列表"""
    try:
        provinces = db.query(KaogongInfo.province).filter(
            KaogongInfo.province.isnot(None),
            KaogongInfo.province != ""
        ).distinct().order_by(KaogongInfo.province).all()
        
        province_list = [p[0] for p in provinces]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取省份列表成功",
                "data": {
                    "provinces": province_list
                }
            }
        )
    except Exception as e:
        log_error(f"获取考公省份列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取省份列表失败，请稍后重试",
                "data": None
            }
        )

@router.get("/position-types", summary="获取考公岗位类别列表")
async def get_kaogong_position_types(
    db: Session = Depends(get_db_kaogong)
):
    """获取考公岗位类别列表"""
    try:
        position_types = db.query(KaogongInfo.position_type).filter(
            KaogongInfo.position_type.isnot(None),
            KaogongInfo.position_type != ""
        ).distinct().order_by(KaogongInfo.position_type).all()
        
        position_type_list = [pt[0] for pt in position_types]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取岗位类别列表成功",
                "data": {
                    "position_types": position_type_list
                }
            }
        )
    except Exception as e:
        log_error(f"获取考公岗位类别列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取岗位类别列表失败，请稍后重试",
                "data": None
            }
        )

@router.get("/majors", summary="获取考公专业列表")
async def get_kaogong_majors(
    db: Session = Depends(get_db_kaogong)
):
    """获取考公专业列表"""
    try:
        majors = db.query(KaogongInfo.major).filter(
            KaogongInfo.major.isnot(None),
            KaogongInfo.major != ""
        ).distinct().order_by(KaogongInfo.major).all()
        
        major_list = [m[0] for m in majors]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取专业列表成功",
                "data": {
                    "majors": major_list
                }
            }
        )
    except Exception as e:
        log_error(f"获取考公专业列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取专业列表失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/info/{info_id}", summary="删除考公信息")
async def delete_kaogong_info(
    info_id: int,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaogong)
):
    """删除考公信息"""
    try:
        # 检查信息是否存在
        info = db.query(KaogongInfo).filter(KaogongInfo.id == info_id).first()
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="信息不存在"
            )
        
        # 删除信息
        db.delete(info)
        db.commit()
        
        log_user_action(current_user.id, "delete_kaogong_info", f"删除考公信息: ID={info_id}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "删除成功",
                "data": None
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"删除考公信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除失败，请稍后重试"
        )

@router.get("/education", summary="获取考公学历要求列表")
async def get_kaogong_education(
    db: Session = Depends(get_db_kaogong)
):
    """获取考公学历要求列表"""
    try:
        education_list = db.query(KaogongInfo.education).filter(
            KaogongInfo.education.isnot(None),
            KaogongInfo.education != ""
        ).distinct().order_by(KaogongInfo.education).all()
        
        education_options = [e[0] for e in education_list]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取学历要求列表成功",
                "data": {
                    "education": education_options
                }
            }
        )
    except Exception as e:
        log_error(f"获取考公学历要求列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取学历要求列表失败，请稍后重试",
                "data": None
            }
        )