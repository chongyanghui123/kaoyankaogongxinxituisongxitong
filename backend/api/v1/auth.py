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
            # 普通用户设置默认密码
            values['password'] = '123456789'
            
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
        # 普通用户设置默认密码，管理员用户使用提供的密码
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
    """用户登录接口"""
    try:
        # 查找用户
        user = db.query(User).filter(
            (User.username == req.username) |
            (User.email == req.username) |
            (User.phone == req.username)
        ).first()
        
        # 检查用户是否存在
        if not user:
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
        
        # 检查用户是否需要修改密码
        # 对于新用户，默认需要修改密码
        # 这里暂时设置为False，避免用户登录后立即跳转到修改密码页面
        need_change_password = False
        
        # 打印用户信息，以便调试
        print(f"用户登录成功: {user.username}, ID: {user.id}, VIP类型: {user.vip_type}, 是否VIP: {user.is_vip}")
        
        # 检查用户的is_vip属性
        print(f"用户的is_vip属性: {user.is_vip}")
        print(f"用户的is_vip_active属性: {user.is_vip_active}")
        
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
                    "is_vip": user.is_vip,
                    "is_trial": user.is_trial_active,
                    "vip_type": user.vip_type,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "need_change_password": need_change_password,
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

class WechatLoginRequest(BaseModel):
    """微信登录请求模型"""
    code: str = Field(..., description="微信登录code")

@router.post("/wechat-login", response_model=AuthResponse, summary="微信登录")
async def wechat_login(
    request: Request,
    req: WechatLoginRequest,
    db: Session = Depends(get_db_common)
):
    """微信登录接口（用于小程序登录）"""
    try:
        # 这里应该调用微信API获取openid，暂时模拟
        # 实际项目中需要使用微信开发者工具的AppID和AppSecret
        openid = f"openid_{req.code}"
        
        # 查找用户是否已存在
        user = db.query(User).filter(User.username == openid).first()
        
        if not user:
            # 创建新用户
            new_user = User(
                username=openid,
                email=f"{openid}@wechat.com",
                phone="",
                password="",
                register_ip=request.client.host,
                is_active=True,
                is_admin=False,
                trial_status=1
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # 创建默认订阅配置
            default_subscription = UserSubscription(
                user_id=new_user.id,
                subscribe_type=3,  # 默认双赛道
                status=1,
                config_json={
                    "kaoyan": {
                        "provinces": [],
                        "schools": [],
                        "majors": [],
                        "degree_type": [],
                        "study_type": []
                    },
                    "kaogong": {
                        "provinces": [],
                        "position_types": [],
                        "majors": [],
                        "education": ["不限"],
                        "is_fresh_graduate": "不限",
                        "is_unlimited": None
                    }
                }
            )
            
            db.add(default_subscription)
            db.commit()
            
            user = new_user
        
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
        
        log_user_action(user.id, "wechat_login", f"微信用户登录: {user.username}")
        
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
                    "is_vip": user.is_vip,
                    "is_trial": user.trial_status == 1,
                    "vip_type": user.vip_type,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                        "is_vip": user.is_vip,
                        "is_admin": user.is_admin,
                        "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None
                    }
                }
            }
        )
        
    except Exception as e:
        log_error(f"微信登录失败: {str(e)}")
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

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_common)
):
    """获取当前用户"""
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
    
    # 检查服务到期时间
    if user.is_vip and user.vip_end_time:
        if datetime.now() > user.vip_end_time:
            # 服务到期，更新用户状态
            user.is_vip = False
            user.is_active = False  # 设置为非活跃，在用户管理页面显示为"到期"
            db.commit()
    
    return user

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

class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")

@router.post("/change-password", response_model=AuthResponse, summary="修改密码")
async def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """修改密码接口"""
    try:
        # 验证旧密码
        if not verify_password(req.old_password, current_user.password):
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
        current_user.password = get_password_hash(req.new_password)
        # 检查用户是否有need_change_password字段
        if hasattr(current_user, 'need_change_password'):
            current_user.need_change_password = False
        db.commit()
        
        log_user_action(current_user.id, "change_password", f"用户修改密码: {current_user.username}")
        
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