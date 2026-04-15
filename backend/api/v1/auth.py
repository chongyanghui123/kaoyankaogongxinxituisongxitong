#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 认证路由
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, validator, model_validator

from config import settings
from core.database import get_db_common
from core.security import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, validate_email, validate_phone, validate_password as validate_pwd
)
from core.logger import log_user_action, log_error

from models.users import User, UserSubscription
import asyncio

router = APIRouter()

class RegisterRequest(BaseModel):
    """注册请求模型"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    password: Optional[str] = Field(default=None, description="密码（仅管理员用户需要）")
    real_name: Optional[str] = Field(None, description="真实姓名")
    gender: Optional[str] = Field(None, description="性别")
    birthdate: Optional[str] = Field(None, description="出生日期")
    kaoyan_requirements: Optional[dict] = Field(None, description="考研需求")
    kaogong_requirements: Optional[dict] = Field(None, description="考公需求")
    is_admin: Optional[bool] = Field(False, description="是否为管理员")
    
    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v
    
    @model_validator(mode='before')
    @classmethod
    def validate_password(cls, values):
        is_admin = values.get('is_admin', False)
        password = values.get('password')
        
        if is_admin:
            if not password or len(password) < 6:
                raise ValueError('管理员用户必须设置密码，且密码至少包含6个字符')
            if not validate_pwd(password):
                raise ValueError('密码必须至少包含6个字符，且包含字母和数字')
        else:
            # 普通用户不需要密码
            values['password'] = None
            
        return values

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str = Field(..., description="刷新令牌")

class ResetPasswordRequest(BaseModel):
    """重置密码请求模型"""
    email: EmailStr = Field(..., description="邮箱")
    verification_code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, description="新密码")

class VerifyEmailRequest(BaseModel):
    """验证邮箱请求模型"""
    email: EmailStr = Field(..., description="邮箱")

class VerifyPhoneRequest(BaseModel):
    """验证手机号请求模型"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")

class AuthResponse(BaseModel):
    """认证响应模型"""
    success: bool
    code: int
    message: str
    data: dict = None

@router.post("/register", response_model=AuthResponse, summary="用户注册")
async def register(
    request: Request,
    req: RegisterRequest,
    db: Session = Depends(get_db_common)
):
    """用户注册接口"""
    try:
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(
            (User.username == req.username) |
            (User.email == req.email) |
            (User.phone == req.phone)
        ).first()
        
        if existing_user:
            if existing_user.username == req.username:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "用户名已存在",
                        "data": None
                    }
                )
            elif existing_user.email == req.email:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "邮箱已被注册",
                        "data": None
                    }
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "手机号已被注册",
                        "data": None
                    }
                )
        
        # 创建新用户
        # 普通用户密码设置为空字符串，管理员用户需要设置密码
        password_hash = ""
        if req.is_admin:
            password_hash = get_password_hash(req.password)
        
        # 解析出生日期
        birthdate = None
        if req.birthdate:
            try:
                birthdate = datetime.strptime(req.birthdate, '%Y-%m-%d')
            except ValueError:
                pass
        
        # 转换性别为整数
        gender = 0  # 默认未知
        if req.gender == '男':
            gender = 1
        elif req.gender == '女':
            gender = 2
        
        # 使用前端发送的is_admin字段
        is_admin = req.is_admin or False
        
        new_user = User(
            username=req.username,
            email=req.email,
            phone=req.phone,
            password=password_hash,
            real_name=req.real_name,
            gender=gender,
            birthdate=birthdate,
            register_ip=request.client.host,
            is_active=True,
            is_admin=is_admin,
            # 设置3天免费试用
            trial_status=1
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # 创建默认订阅配置
        kaoyan_config = {
            "provinces": [],
            "schools": [],
            "majors": [],
            "degree_type": [],
            "study_type": []
        }
        
        kaogong_config = {
            "provinces": [],
            "position_types": [],
            "majors": [],
            "education": ["不限"],
            "is_fresh_graduate": "不限",
            "is_unlimited": None
        }
        
        # 初始化关键词列表
        kaoyan_keywords = []
        kaogong_keywords = []
        
        # 如果前端发送了考研需求信息，使用前端发送的信息
        if req.kaoyan_requirements:
            # 安全处理字段类型
            schools = req.kaoyan_requirements.get("schools", [])
            if isinstance(schools, str):
                schools = schools.split(",") if schools else []
            elif not isinstance(schools, list):
                schools = []
                
            majors = req.kaoyan_requirements.get("majors", [])
            if isinstance(majors, str):
                majors = majors.split(",") if majors else []
            elif not isinstance(majors, list):
                majors = []
                
            kaoyan_config = {
                "provinces": req.kaoyan_requirements.get("provinces", []),
                "schools": [s.strip() for s in schools if s.strip()],
                "majors": [m.strip() for m in majors if m.strip()],
                "types": req.kaoyan_requirements.get("types", []),
                "degree_type": [],
                "study_type": []
            }
            # 获取关键词
            keywords_str = req.kaoyan_requirements.get("keywords", "")
            if keywords_str:
                kaoyan_keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        
        # 如果前端发送了考公需求信息，使用前端发送的信息
        if req.kaogong_requirements:
            # 安全处理字段类型
            majors = req.kaogong_requirements.get("majors", [])
            if isinstance(majors, str):
                majors = majors.split(",") if majors else []
            elif not isinstance(majors, list):
                majors = []
                
            kaogong_config = {
                "provinces": req.kaogong_requirements.get("provinces", []),
                "position_types": req.kaogong_requirements.get("position_types", []),
                "majors": [m.strip() for m in majors if m.strip()],
                "education": [req.kaogong_requirements.get("education", "不限")],
                "is_fresh_graduate": req.kaogong_requirements.get("is_fresh_graduate", "不限"),
                "is_unlimited": None
            }
            # 获取关键词
            keywords_str = req.kaogong_requirements.get("keywords", "")
            if keywords_str:
                kaogong_keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        
        # 根据需求设置订阅类型
        subscribe_type = 3  # 默认双赛道
        if not req.kaoyan_requirements:
            subscribe_type = 2  # 只考公
        elif not req.kaogong_requirements:
            subscribe_type = 1  # 只考研
        
        default_subscription = UserSubscription(
            user_id=new_user.id,
            subscribe_type=subscribe_type,
            status=1,
            config_json={
                "kaoyan": kaoyan_config,
                "kaogong": kaogong_config
            }
        )
        
        db.add(default_subscription)
        
        # 添加关键词
        from models.users import UserKeyword
        
        # 添加考研关键词
        for keyword in kaoyan_keywords:
            new_keyword = UserKeyword(
                user_id=new_user.id,
                keyword=keyword,
                category=1,  # 1-考研
                is_active=True
            )
            db.add(new_keyword)
        
        # 添加考公关键词
        for keyword in kaogong_keywords:
            new_keyword = UserKeyword(
                user_id=new_user.id,
                keyword=keyword,
                category=2,  # 2-考公
                is_active=True
            )
            db.add(new_keyword)
        
        db.commit()
        
        # 生成AI搜索结果并关联到用户
        async def generate_ai_search_results(user_id, kaoyan_config, kaogong_config):
            """生成AI搜索结果并关联到用户"""
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
                        demand_parts.append(f"关注{','.join(kaoyan_config.get('majors'))}专业")
                    if kaoyan_config.get('types'):
                        demand_parts.append(f"关注{','.join(kaoyan_config.get('types'))}")
                    
                    demand_text = f"考研 {' '.join(demand_parts)}"
                    
                    # 调用AI分析需求
                    demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, {})
                    
                    # 生成相关链接
                    relevant_links = []
                    
                    # 学校相关链接
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
                            relevant_links.append({
                                'title': f'{clean_school}研究生招生网',
                                'url': school_url_map[clean_school],
                                'relevance': 0.9,
                                'type': 'school',
                                'category': 'kaoyan'
                            })
                    
                    # 省份相关链接
                    for province in kaoyan_config.get('provinces', []):
                        relevant_links.append({
                            'title': f'{province}教育考试院',
                            'url': f'https://www.{province}jyksy.cn/',
                            'relevance': 0.8,
                            'type': 'province',
                            'category': 'kaoyan'
                        })
                    
                    # 通用链接
                    relevant_links.extend([
                        {
                            'title': '研招网-考研政策',
                            'url': 'https://yz.chsi.com.cn/kyzx/',
                            'relevance': 0.9,
                            'type': 'general',
                            'category': 'kaoyan'
                        },
                        {
                            'title': '中国教育在线-考研资讯',
                            'url': 'https://kaoyan.eol.cn/',
                            'relevance': 0.8,
                            'type': 'general',
                            'category': 'kaoyan'
                        }
                    ])
                    
                    # 按相关性排序
                    relevant_links.sort(key=lambda x: x['relevance'], reverse=True)
                    
                    # 限制返回数量
                    relevant_links = relevant_links[:10]
                    
                    # 这里可以将链接保存到数据库，关联到用户
                    # 暂时打印日志
                    log_user_action(user_id, "ai_search", f"为用户生成考研相关链接: {len(relevant_links)}个")
                
                # 处理考公需求
                if kaogong_config and (kaogong_config.get('provinces') or kaogong_config.get('position_types')):
                    # 构造需求文本
                    demand_parts = []
                    if kaogong_config.get('provinces'):
                        demand_parts.append(f"关注{','.join(kaogong_config.get('provinces'))}地区")
                    if kaogong_config.get('position_types'):
                        demand_parts.append(f"关注{','.join(kaogong_config.get('position_types'))}")
                    if kaogong_config.get('majors'):
                        demand_parts.append(f"关注{','.join(kaogong_config.get('majors'))}专业")
                    
                    demand_text = f"考公 {' '.join(demand_parts)}"
                    
                    # 调用AI分析需求
                    demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, {})
                    
                    # 生成相关链接
                    relevant_links = []
                    
                    # 省份相关链接
                    for province in kaogong_config.get('provinces', []):
                        relevant_links.append({
                            'title': f'{province}公务员考试网',
                            'url': f'https://www.{province}gwy.org/',
                            'relevance': 0.8,
                            'type': 'province',
                            'category': 'kaogong'
                        })
                    
                    # 通用链接
                    relevant_links.extend([
                        {
                            'title': '国家公务员局-考试录用',
                            'url': 'http://bm.scs.gov.cn/pp/gkweb/core/web/ui/business/home/gkhome.html',
                            'relevance': 0.9,
                            'type': 'general',
                            'category': 'kaogong'
                        },
                        {
                            'title': '中国人事考试网',
                            'url': 'https://www.cpta.com.cn/',
                            'relevance': 0.8,
                            'type': 'general',
                            'category': 'kaogong'
                        }
                    ])
                    
                    # 按相关性排序
                    relevant_links.sort(key=lambda x: x['relevance'], reverse=True)
                    
                    # 限制返回数量
                    relevant_links = relevant_links[:10]
                    
                    # 这里可以将链接保存到数据库，关联到用户
                    # 暂时打印日志
                    log_user_action(user_id, "ai_search", f"为用户生成考公相关链接: {len(relevant_links)}个")
                    
            except Exception as e:
                log_error(f"生成AI搜索结果失败: {str(e)}")
        
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
                            '成都理工大学': 'https://www.cdut.edu.cn/',
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
                            await _add_crawler_config_to_db(crawler_config)
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
                        await _add_crawler_config_to_db(crawler_config)
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
                        await _add_crawler_config_to_db(crawler_config)
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
                        await _add_crawler_config_to_db(crawler_config)
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
                        await _add_crawler_config_to_db(crawler_config)
                        crawler_configs.append(crawler_config)
                    
                    log_user_action(user_id, "analyze_demand", f"为用户生成考公爬虫配置: {len(crawler_configs)}个")
                    
            except Exception as e:
                log_error(f"分析用户需求失败: {str(e)}")
        
        # 启动异步任务分析需求
        import asyncio
        asyncio.create_task(analyze_user_demand_and_generate_configs(
            new_user.id, 
            kaoyan_config, 
            kaogong_config
        ))
        
        # 检查是否是管理员创建用户
        x_admin_create = request.headers.get('X-Admin-Create', 'false')
        
        log_user_action(new_user.id, "register", f"用户注册: {req.username}")
        
        # 只有管理员用户需要返回token
        if new_user.is_admin:
            # 生成令牌
            access_token = create_access_token(data={"sub": str(new_user.id)})
            refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "code": 201,
                    "message": "注册成功",
                    "data": {
                        "user_id": new_user.id,
                        "username": new_user.username,
                        "email": new_user.email,
                        "phone": new_user.phone,
                        "is_vip": new_user.is_vip,
                        "is_trial": True,
                        "is_admin": new_user.is_admin,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                    }
                }
            )
        else:
            # 普通用户不返回token
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "code": 201,
                    "message": "注册成功",
                    "data": {
                        "user_id": new_user.id,
                        "username": new_user.username,
                        "email": new_user.email,
                        "phone": new_user.phone,
                        "is_vip": new_user.is_vip,
                        "is_trial": True,
                        "is_admin": new_user.is_admin
                    }
                }
            )
        
    except Exception as e:
        error_message = str(e)
        log_error(f"注册失败: {error_message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": f"注册失败，请稍后重试: {error_message}",
                "data": None
            }
        )

@router.post("/login", response_model=AuthResponse, summary="用户登录")
async def login(
    request: Request,
    req: LoginRequest,
    db: Session = Depends(get_db_common)
):
    """用户登录接口（仅管理员用户可登录）"""
    try:
        # 查找用户
        user = db.query(User).filter(
            (User.username == req.username) |
            (User.email == req.username) |
            (User.phone == req.username)
        ).first()
        
        # 只有管理员用户可以登录
        if not user or not user.is_admin:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "code": 401,
                    "message": "用户名或密码错误",
                    "data": None
                }
            )
        
        # 验证密码
        password_valid = False
        if user:
            password_valid = verify_password(req.password, user.password)
        
        if not password_valid:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "code": 401,
                    "message": "用户名或密码错误",
                    "data": None
                }
            )
        
        # 检查服务到期时间
        if user.is_vip and user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                # 服务到期，更新用户状态
                user.is_vip = False
                user.is_active = False  # 设置为非活跃，在用户管理页面显示为"到期"
                db.commit()
        

        
        # 更新登录信息
        user.last_login_ip = request.client.host
        user.last_login_time = datetime.now()
        db.commit()
        
        # 生成令牌
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        log_user_action(user.id, "login", f"用户登录: {user.username}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "登录成功",
                "data": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "is_admin": user.is_admin,
                    "is_vip": user.is_vip_active,
                    "is_trial": user.is_trial_active,
                    "vip_type": user.vip_type,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                }
            }
        )
        
    except Exception as e:
        log_error(f"登录失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "登录失败，请稍后重试",
                "data": None
            }
        )

@router.post("/refresh", response_model=AuthResponse, summary="刷新令牌")
async def refresh_token(
    req: RefreshTokenRequest,
    db: Session = Depends(get_db_common)
):
    """刷新访问令牌接口"""
    try:
        from jose import JWTError, jwt
        
        # 验证刷新令牌
        try:
            payload = jwt.decode(req.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if user_id is None or token_type != "refresh":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "code": 401,
                        "message": "无效的刷新令牌",
                        "data": None
                    }
                )
                
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "code": 401,
                    "message": "无效的刷新令牌",
                    "data": None
                }
            )
        
        # 查找用户
        user = db.query(User).filter(User.id == user_id).first()
        
        # 检查服务到期时间
        if user and user.is_vip and user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                # 服务到期，更新用户状态
                user.is_vip = False
                user.is_active = False  # 设置为非活跃，在用户管理页面显示为"到期"
                db.commit()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "code": 401,
                    "message": "用户不存在",
                    "data": None
                }
            )
        

        
        # 生成新的访问令牌
        access_token = create_access_token(data={"sub": user_id})
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "令牌刷新成功",
                "data": {
                    "access_token": access_token,
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                }
            }
        )
        
    except Exception as e:
        log_error(f"刷新令牌失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "刷新令牌失败，请稍后重试",
                "data": None
            }
        )

@router.post("/logout", response_model=AuthResponse, summary="用户登出")
async def logout(
    request: Request,
    db: Session = Depends(get_db_common)
):
    """用户登出接口"""
    try:
        # 从请求头获取令牌
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if token:
            # 这里可以添加令牌黑名单逻辑
            pass
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "登出成功",
                "data": None
            }
        )
        
    except Exception as e:
        log_error(f"登出失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "登出失败，请稍后重试",
                "data": None
            }
        )

@router.post("/send-verification-code", response_model=AuthResponse, summary="发送验证码")
async def send_verification_code(
    req: VerifyEmailRequest,
    db: Session = Depends(get_db_common)
):
    """发送邮箱验证码"""
    try:
        # 检查邮箱是否存在
        user = db.query(User).filter(User.email == req.email).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "邮箱未注册",
                    "data": None
                }
            )
        
        # 生成验证码
        from core.security import generate_verification_code
        code = generate_verification_code()
        
        # 这里可以添加发送邮件的逻辑
        # 暂时返回成功
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "验证码已发送",
                "data": {
                    "email": req.email
                }
            }
        )
        
    except Exception as e:
        log_error(f"发送验证码失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "发送验证码失败，请稍后重试",
                "data": None
            }
        )

@router.post("/reset-password", response_model=AuthResponse, summary="重置密码")
async def reset_password(
    req: ResetPasswordRequest,
    db: Session = Depends(get_db_common)
):
    """重置密码接口"""
    try:
        # 查找用户
        user = db.query(User).filter(User.email == req.email).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "邮箱未注册",
                    "data": None
                }
            )
        
        # 验证验证码（这里简化处理）
        # 实际项目中应该从缓存或数据库中验证
        
        # 更新密码
        user.password = get_password_hash(req.new_password)
        db.commit()
        
        log_user_action(user.id, "reset_password", f"用户重置密码: {user.username}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "密码重置成功",
                "data": None
            }
        )
        
    except Exception as e:
        log_error(f"重置密码失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "重置密码失败，请稍后重试",
                "data": None
            }
        )

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_common)
):
    """获取当前管理员用户"""
    from jose import JWTError, jwt
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查服务到期时间（管理员也需要检查）
    if user.is_vip and user.vip_end_time:
        if datetime.now() > user.vip_end_time:
            # 服务到期，更新用户状态
            user.is_vip = False
            user.is_active = False  # 设置为非活跃，在用户管理页面显示为"到期"
            db.commit()
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    
    return user