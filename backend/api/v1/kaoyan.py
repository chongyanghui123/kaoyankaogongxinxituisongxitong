#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 考研路由
"""

from datetime import datetime
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from pydantic import BaseModel, Field

from config import settings
from core.database import get_db_kaoyan, get_db_common
from core.security import get_current_user
from core.logger import log_user_action, log_error
from models.kaoyan import KaoyanInfo
from models.users import UserReadInfo, UserFavorite, PushLog, User, UserSubscription, UserKeyword
from api.v1.sync_helpers import sync_get_user_requirements

router = APIRouter()

def get_info_user_requirements(info_id: int, category: int, db_common: Session):
    """获取情报对应的用户需求信息"""
    try:
        # 获取情报信息
        from models.kaoyan import KaoyanInfo
        from core.database import get_db_kaoyan
        db_kaoyan = next(get_db_kaoyan())
        info = db_kaoyan.query(KaoyanInfo).filter(KaoyanInfo.id == info_id).first()
        db_kaoyan.close()
        if not info:
            return []
        
        # 获取所有活跃用户
        active_users = db_common.query(User).filter(User.is_active == True).all()
        
        # 筛选符合需求的用户
        user_requirements = []
        
        for user in active_users:
            try:
                # 获取用户需求
                requirements = sync_get_user_requirements(user.id, db_common, user)
                
                # 检查用户是否符合情报需求
                match = False
                
                if category == 1:  # 考研
                    kaoyan_requirements = requirements.get('kaoyan', {})
                    
                    # 检查省份
                    provinces = kaoyan_requirements.get('provinces', [])
                    if provinces and info.province and info.province not in provinces:
                        continue
                    
                    # 检查学校
                    schools = kaoyan_requirements.get('schools', [])
                    if isinstance(schools, str):
                        schools = [schools]
                    if schools and info.school and info.school not in schools:
                        continue
                    
                    # 检查专业
                    majors = kaoyan_requirements.get('majors', [])
                    if isinstance(majors, str):
                        majors = [majors]
                    if majors and info.major and info.major not in majors:
                        continue
                    
                    # 检查关键词
                    keywords = kaoyan_requirements.get('keywords', [])
                    if isinstance(keywords, str):
                        keywords = [keywords]
                    if keywords:
                        info_text = f"{info.title} {info.content or ''}"
                        if not any(keyword in info_text for keyword in keywords):
                            continue
                    
                    match = True
                
                if match:
                    user_requirements.append({
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'requirements': requirements
                    })
            except Exception as e:
                log_error(f"获取用户{user.id}需求信息失败: {str(e)}")
                continue
        
        return user_requirements
    except Exception as e:
        log_error(f"获取情报{info_id}用户需求信息失败: {str(e)}")
        return []

class KaoyanInfoResponse(BaseModel):
    """考研信息响应模型"""
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
    school: Optional[str]
    major: Optional[str]
    degree_type: Optional[int]
    degree_type_text: str
    study_type: Optional[int]
    study_type_text: str
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

class KaoyanInfoListResponse(BaseModel):
    """考研信息列表响应模型"""
    total: int
    items: List[KaoyanInfoResponse]

class KaoyanInfoDetailRequest(BaseModel):
    """考研信息详情请求模型"""
    id: int

@router.get("/info/list", response_model=KaoyanInfoListResponse, summary="获取考研信息列表")
async def get_kaoyan_info_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[int] = Query(None, ge=0, le=5, description="分类"),
    province: Optional[str] = Query(None, description="省份"),
    school: Optional[str] = Query(None, description="院校"),
    major: Optional[str] = Query(None, description="专业"),
    urgency_level: Optional[int] = Query(None, ge=0, le=3, description="紧急度"),
    keyword: Optional[str] = Query(None, description="关键词"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan),
    db_common: Session = Depends(get_db_common)
):
    """获取考研信息列表"""
    try:
        # 构建查询
        query = db.query(KaoyanInfo).filter(KaoyanInfo.is_valid == True)
        
        # 过滤条件
        if category is not None:
            query = query.filter(KaoyanInfo.category == category)
        if province:
            query = query.filter(KaoyanInfo.province == province)
        if school:
            query = query.filter(KaoyanInfo.school.like(f"%{school}%"))
        if major:
            query = query.filter(KaoyanInfo.major.like(f"%{major}%"))
        if urgency_level is not None:
            query = query.filter(KaoyanInfo.urgency_level == urgency_level)
        if keyword:
            query = query.filter(
                or_(
                    KaoyanInfo.title.like(f"%{keyword}%"),
                    KaoyanInfo.content.like(f"%{keyword}%"),
                    KaoyanInfo.tags.like(f"%{keyword}%")
                )
            )
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        info_list = query.order_by(
            desc(KaoyanInfo.is_top),
            desc(KaoyanInfo.is_excellent),
            desc(KaoyanInfo.publish_time)
        ).offset(offset).limit(page_size).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 1  # 1-考研
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 1  # 1-考研
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in info_list:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 1, db_common)
            
            items.append(KaoyanInfoResponse(
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
                school=info.school,
                major=info.major,
                degree_type=info.degree_type,
                degree_type_text=info.degree_type_text,
                study_type=info.study_type,
                study_type_text=info.study_type_text,
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
        
        return KaoyanInfoListResponse(total=total, items=items)
    except Exception as e:
        log_error(f"获取考研信息列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考研信息列表失败"
        )

@router.get("/info/detail/{info_id}", response_model=KaoyanInfoResponse, summary="获取考研信息详情")
async def get_kaoyan_info_detail(
    info_id: int,
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan),
    db_common: Session = Depends(get_db_common)
):
    """获取考研信息详情"""
    try:
        # 获取信息
        info = db.query(KaoyanInfo).filter(
            KaoyanInfo.id == info_id,
            KaoyanInfo.is_valid == True
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
                UserReadInfo.category == 1  # 1-考研
            ).first()
            
            if not existing_read:
                new_read = UserReadInfo(
                    user_id=current_user.id,
                    info_id=info_id,
                    category=1
                )
                db_common.add(new_read)
                db_common.commit()
        
        # 检查是否收藏
        is_favorite = False
        if current_user:
            favorite = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.info_id == info_id,
                UserFavorite.category == 1  # 1-考研
            ).first()
            is_favorite = favorite is not None
        
        # 获取用户需求信息
        user_requirements = get_info_user_requirements(info.id, 1, db_common)
        
        return KaoyanInfoResponse(
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
            school=info.school,
            major=info.major,
            degree_type=info.degree_type,
            degree_type_text=info.degree_type_text,
            study_type=info.study_type,
            study_type_text=info.study_type_text,
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
        log_error(f"获取考研信息详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考研信息详情失败"
        )

@router.post("/info/like/{info_id}", summary="点赞考研信息")
async def like_kaoyan_info(
    info_id: int,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan)
):
    """点赞考研信息"""
    try:
        info = db.query(KaoyanInfo).filter(
            KaoyanInfo.id == info_id,
            KaoyanInfo.is_valid == True
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
        
        log_user_action(current_user.id, "like_kaoyan_info", f"点赞考研信息: ID={info_id}")
        
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
        log_error(f"点赞考研信息失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "点赞失败，请稍后重试",
                "data": None
            }
        )

@router.get("/info/hot", response_model=List[KaoyanInfoResponse], summary="获取热门考研信息")
async def get_hot_kaoyan_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan),
    db_common: Session = Depends(get_db_common)
):
    """获取热门考研信息（按浏览量排序）"""
    try:
        # 获取热门信息
        hot_info = db.query(KaoyanInfo).filter(
            KaoyanInfo.is_valid == True
        ).order_by(
            desc(KaoyanInfo.view_count),
            desc(KaoyanInfo.publish_time)
        ).limit(limit).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 1  # 1-考研
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 1  # 1-考研
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in hot_info:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 1, db_common)
            
            items.append(KaoyanInfoResponse(
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
                school=info.school,
                major=info.major,
                degree_type=info.degree_type,
                degree_type_text=info.degree_type_text,
                study_type=info.study_type,
                study_type_text=info.study_type_text,
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
        log_error(f"获取热门考研信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取热门考研信息失败"
        )

class DeleteAllKaoyanInfoRequest(BaseModel):
    """删除所有考研信息请求模型"""
    pass

@router.delete("/delete-all", summary="删除所有考研信息")
async def delete_all_kaoyan_info(
    request: DeleteAllKaoyanInfoRequest,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan)
):
    """删除所有考研信息"""
    try:
        # 删除所有考研信息
        db.query(KaoyanInfo).delete()
        db.commit()
        
        log_user_action(current_user.id, "delete_all_kaoyan_info", "删除所有考研信息")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "所有考研信息删除成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除所有考研信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除所有考研信息失败，请稍后重试"
        )

@router.get("/info/latest", response_model=List[KaoyanInfoResponse], summary="获取最新考研信息")
async def get_latest_kaoyan_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    current_user: Optional[Session] = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan),
    db_common: Session = Depends(get_db_common)
):
    """获取最新考研信息"""
    try:
        # 获取最新信息
        latest_info = db.query(KaoyanInfo).filter(
            KaoyanInfo.is_valid == True
        ).order_by(
            desc(KaoyanInfo.publish_time)
        ).limit(limit).all()
        
        # 获取用户已读和收藏状态
        user_read_ids = set()
        user_favorite_ids = set()
        
        if current_user:
            # 获取已读信息
            read_info = db_common.query(UserReadInfo).filter(
                UserReadInfo.user_id == current_user.id,
                UserReadInfo.category == 1  # 1-考研
            ).all()
            user_read_ids = {ri.info_id for ri in read_info}
            
            # 获取收藏信息
            favorites = db_common.query(UserFavorite).filter(
                UserFavorite.user_id == current_user.id,
                UserFavorite.category == 1  # 1-考研
            ).all()
            user_favorite_ids = {fav.info_id for fav in favorites}
        
        # 构建响应
        items = []
        for info in latest_info:
            # 获取用户需求信息
            user_requirements = get_info_user_requirements(info.id, 1, db_common)
            
            items.append(KaoyanInfoResponse(
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
                school=info.school,
                major=info.major,
                degree_type=info.degree_type,
                degree_type_text=info.degree_type_text,
                study_type=info.study_type,
                study_type_text=info.study_type_text,
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
        log_error(f"获取最新考研信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取最新考研信息失败"
        )

@router.get("/provinces", summary="获取考研省份列表")
async def get_kaoyan_provinces(
    db: Session = Depends(get_db_kaoyan)
):
    """获取考研省份列表"""
    try:
        provinces = db.query(KaoyanInfo.province).filter(
            KaoyanInfo.province.isnot(None),
            KaoyanInfo.province != ""
        ).distinct().order_by(KaoyanInfo.province).all()
        
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
        log_error(f"获取考研省份列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取省份列表失败，请稍后重试",
                "data": None
            }
        )

@router.get("/schools", summary="获取考研院校列表")
async def get_kaoyan_schools(
    province: Optional[str] = Query(None, description="省份"),
    db: Session = Depends(get_db_kaoyan)
):
    """获取考研院校列表"""
    try:
        query = db.query(KaoyanInfo.school).filter(
            KaoyanInfo.school.isnot(None),
            KaoyanInfo.school != ""
        )
        
        if province:
            query = query.filter(KaoyanInfo.province == province)
        
        schools = query.distinct().order_by(KaoyanInfo.school).all()
        school_list = [s[0] for s in schools]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "获取院校列表成功",
                "data": {
                    "schools": school_list
                }
            }
        )
    except Exception as e:
        log_error(f"获取考研院校列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取院校列表失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/info/{info_id}", summary="删除考研信息")
async def delete_kaoyan_info(
    info_id: int,
    current_user: Session = Depends(get_current_user),
    db: Session = Depends(get_db_kaoyan)
):
    """删除考研信息"""
    try:
        # 检查信息是否存在
        info = db.query(KaoyanInfo).filter(KaoyanInfo.id == info_id).first()
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="信息不存在"
            )
        
        # 删除信息
        db.delete(info)
        db.commit()
        
        log_user_action(current_user.id, "delete_kaoyan_info", f"删除考研信息: ID={info_id}")
        
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
        log_error(f"删除考研信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除失败，请稍后重试"
        )

@router.get("/majors", summary="获取考研专业列表")
async def get_kaoyan_majors(
    school: Optional[str] = Query(None, description="院校"),
    db: Session = Depends(get_db_kaoyan)
):
    """获取考研专业列表"""
    try:
        query = db.query(KaoyanInfo.major).filter(
            KaoyanInfo.major.isnot(None),
            KaoyanInfo.major != ""
        )
        
        if school:
            query = query.filter(KaoyanInfo.school == school)
        
        majors = query.distinct().order_by(KaoyanInfo.major).all()
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
        log_error(f"获取考研专业列表失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "获取专业列表失败，请稍后重试",
                "data": None
            }
        )