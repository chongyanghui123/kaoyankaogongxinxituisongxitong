#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 用户路由
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
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

@router.get("/profile", response_model=UserProfileResponse, summary="获取用户信息")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    try:
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
                    "kaogong": req.config.kaogong
                }
            )
            db.add(subscription)
        else:
            # 更新现有配置
            subscription.subscribe_type = req.subscribe_type
            subscription.config_json = {
                "kaoyan": req.config.kaoyan,
                "kaogong": req.config.kaogong
            }
        
        db.commit()
        db.refresh(subscription)
        
        # 异步分析用户需求并生成爬虫配置
        async def analyze_user_demand_and_generate_configs(user_id, kaoyan_config, kaogong_config):
            """分析用户需求并生成爬虫配置"""
            try:
                # 处理考研需求
                if kaoyan_config and (kaoyan_config.get('provinces') or kaoyan_config.get('schools')):
                    # 构造需求文本
                    demand_parts = []
                    if kaoyan_config.get('provinces'):
                        demand_parts.append(f"关注{','.join(kaoyan_config.get('provinces'))}地区")
                    if kaoyan_config.get('schools'):
                        demand_parts.append(f"关注{','.join(kaoyan_config.get('schools'))}")
                    if kaoyan_config.get('majors'):
                        demand_parts.append(f"关注{kaoyan_config.get('majors')}专业")
                    if kaoyan_config.get('types'):
                        demand_parts.append(f"关注{','.join(kaoyan_config.get('types'))}")
                    
                    demand_text = f"考研 {' '.join(demand_parts)}"
                    
                    # 调用AI分析需求
                    demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, {})
                    
                    # 生成相关链接
                    crawler_configs = []
                    
                    # 学校相关链接和爬虫配置
                    for school in kaoyan_config.get('schools', []):
                        # 清理学校名称
                        clean_school = school.split('（')[0].split('(')[0]
                        
                        # 学校URL映射
                        school_url_map = {
                            '中山大学': 'https://graduate.sysu.edu.cn/',
                            '北京大学': 'https://admission.pku.edu.cn/',
                            '清华大学': 'https://yz.tsinghua.edu.cn/',
                            '复旦大学': 'https://gs.fudan.edu.cn/',
                            '上海交通大学': 'https://yzb.sjtu.edu.cn/'
                        }
                        
                        if clean_school in school_url_map:
                            url = school_url_map[clean_school]
                            
                            # 生成爬虫配置
                            crawler_config = {
                                'name': f"AI增强-kaoyan-{datetime.now().strftime('%Y%m%d%H%M')}-{clean_school}-研究生招生网",
                                'url': url,
                                'selector': '.news-list li, .article-list li, .list-item, .news-item',
                                'interval': 60,
                                'priority': 3,
                                'status': 1,
                                'user_id': user_id,
                                'ai_enhanced': True,
                                'match_score': 0.9,
                                'personalized': True
                            }
                            
                            # 添加到数据库
                            _add_crawler_config_to_db(crawler_config)
                            crawler_configs.append(crawler_config)
                    
                    # 省份相关链接和爬虫配置
                    for province in kaoyan_config.get('provinces', []):
                        # 生成爬虫配置
                        crawler_config = {
                            'name': f"AI增强-kaoyan-{datetime.now().strftime('%Y%m%d%H%M')}-{province}-教育考试院",
                            'url': f'https://www.{province}jyksy.cn/',
                            'selector': '.news-list li, .article-list li, .list-item, .news-item',
                            'interval': 45,
                            'priority': 2,
                            'status': 1,
                            'user_id': user_id,
                            'ai_enhanced': True,
                            'match_score': 0.8,
                            'personalized': True
                        }
                        
                        # 添加到数据库
                        _add_crawler_config_to_db(crawler_config)
                        crawler_configs.append(crawler_config)
                    
                    # 通用链接和爬虫配置
                    general_links = [
                        {
                            'title': '研招网-考研政策',
                            'url': 'https://yz.chsi.com.cn/kyzx/',
                            'relevance': 0.9
                        },
                        {
                            'title': '中国教育在线-考研资讯',
                            'url': 'https://kaoyan.eol.cn/',
                            'relevance': 0.8
                        }
                    ]
                    
                    for link in general_links:
                        # 生成爬虫配置
                        crawler_config = {
                            'name': f"AI增强-kaoyan-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                            'url': link['url'],
                            'selector': '.news-list li',
                            'interval': 30,
                            'priority': 2,
                            'status': 1,
                            'user_id': user_id,
                            'ai_enhanced': True,
                            'match_score': link['relevance'],
                            'personalized': False
                        }
                        
                        # 添加到数据库
                        _add_crawler_config_to_db(crawler_config)
                        crawler_configs.append(crawler_config)
                    
                    log_user_action(user_id, "analyze_demand", f"为用户生成考研爬虫配置: {len(crawler_configs)}个")
                
                # 处理考公需求
                if kaogong_config and (kaogong_config.get('provinces') or kaogong_config.get('position_types')):
                    # 构造需求文本
                    demand_parts = []
                    if kaogong_config.get('provinces'):
                        demand_parts.append(f"关注{','.join(kaogong_config.get('provinces'))}地区")
                    if kaogong_config.get('position_types'):
                        demand_parts.append(f"关注{','.join(kaogong_config.get('position_types'))}")
                    if kaogong_config.get('majors'):
                        demand_parts.append(f"关注{kaogong_config.get('majors')}专业")
                    
                    demand_text = f"考公 {' '.join(demand_parts)}"
                    
                    # 调用AI分析需求
                    demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, {})
                    
                    # 生成爬虫配置
                    crawler_configs = []
                    
                    # 省份相关链接和爬虫配置
                    for province in kaogong_config.get('provinces', []):
                        # 生成爬虫配置
                        crawler_config = {
                            'name': f"AI增强-kaogong-{datetime.now().strftime('%Y%m%d%H%M')}-{province}-公务员考试网",
                            'url': f'https://www.{province}gwy.org/',
                            'selector': '.news-list li, .article-list li, .list-item, .news-item',
                            'interval': 45,
                            'priority': 2,
                            'status': 1,
                            'user_id': user_id,
                            'ai_enhanced': True,
                            'match_score': 0.8,
                            'personalized': True
                        }
                        
                        # 添加到数据库
                        _add_crawler_config_to_db(crawler_config)
                        crawler_configs.append(crawler_config)
                    
                    # 通用链接和爬虫配置
                    general_links = [
                        {
                            'title': '国家公务员局-考试录用',
                            'url': 'http://bm.scs.gov.cn/pp/gkweb/core/web/ui/business/home/gkhome.html',
                            'relevance': 0.9
                        },
                        {
                            'title': '中国人事考试网',
                            'url': 'https://www.cpta.com.cn/',
                            'relevance': 0.8
                        }
                    ]
                    
                    for link in general_links:
                        # 生成爬虫配置
                        crawler_config = {
                            'name': f"AI增强-kaogong-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                            'url': link['url'],
                            'selector': '.news-list li',
                            'interval': 30,
                            'priority': 2,
                            'status': 1,
                            'user_id': user_id,
                            'ai_enhanced': True,
                            'match_score': link['relevance'],
                            'personalized': False
                        }
                        
                        # 添加到数据库
                        _add_crawler_config_to_db(crawler_config)
                        crawler_configs.append(crawler_config)
                    
                    log_user_action(user_id, "analyze_demand", f"为用户生成考公爬虫配置: {len(crawler_configs)}个")
                    
            except Exception as e:
                log_error(f"分析用户需求失败: {str(e)}")
        
        # 启动异步任务分析需求
        asyncio.create_task(analyze_user_demand_and_generate_configs(
            current_user.id, 
            req.config.kaoyan, 
            req.config.kaogong
        ))
        
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

@router.get("/favorites", response_model=List[FavoriteResponse], summary="获取收藏信息")
async def get_favorites(
    category: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取用户收藏信息列表"""
    try:
        query = db.query(UserFavorite).filter(UserFavorite.user_id == current_user.id)
        
        if category:
            query = query.filter(UserFavorite.category == category)
        
        favorites = query.order_by(UserFavorite.created_at.desc()).all()
        
        return [
            FavoriteResponse(
                id=fav.id,
                info_id=fav.info_id,
                category=fav.category,
                created_at=fav.created_at.isoformat()
            )
            for fav in favorites
        ]
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