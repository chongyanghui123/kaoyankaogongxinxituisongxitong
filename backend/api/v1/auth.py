#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 认证路由
"""

from datetime import datetime, timedelta, date
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, validator, model_validator

from config import settings
from core.database import get_db_common
from core.security import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, validate_email, validate_phone, validate_password as validate_pwd,
    get_current_user
)
from core.logger import log_user_action, log_error

from models.users import User, UserSubscription, UserLoginRecord
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
            values['password'] = os.getenv("DEFAULT_USER_PASSWORD", "changeme123")
            
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
        
        # 发送欢迎邮件
        try:
            from core.push_manager import send_email
            
            # 获取原始密码
            original_password = req.password if req.password else os.getenv("DEFAULT_USER_PASSWORD", "changeme123")
            
            email_subject = "欢迎注册双赛道情报通"
            email_content = f"""尊敬的 {new_user.username}：

欢迎注册双赛道情报通！

您的账号信息：
- 用户名：{new_user.username}
- 邮箱：{new_user.email}
- 手机号：{new_user.phone or '未设置'}
- 原始密码：{original_password}

为了您的账号安全，建议您登录后尽快修改密码。

我们为您提供考研和考公相关的最新资讯推送服务，帮助您及时掌握相关信息。

如有任何问题，请联系客服。

此致
双赛道情报通团队
"""
            send_email(new_user.email, email_subject, email_content)
        except Exception as e:
            log_error(f"发送欢迎邮件失败: {str(e)}")
        
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
        # 打印详细的请求信息用于调试
        import sys
        print(f"=== 登录请求调试信息 ===", file=sys.stderr)
        print(f"请求方法: {request.method}", file=sys.stderr)
        print(f"请求路径: {request.url}", file=sys.stderr)
        print(f"请求体: {req}", file=sys.stderr)
        print(f"用户名参数: '{req.username}'", file=sys.stderr)
        print(f"密码参数长度: {len(req.password)} 字符", file=sys.stderr)
        
        # 检查是否是管理员登录（只有邮箱和密码）
        # 如果是邮箱格式，则可能是管理员登录
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_email = re.match(email_pattern, req.username)
        
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
        
        # 检查用户登录方式
        # 管理员必须使用邮箱登录
        # 普通用户可以使用手机号登录
        if user.is_admin:
            # 管理员必须使用邮箱登录
            if not is_email:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "code": 401,
                        "message": "管理员只能使用邮箱登录",
                        "data": None
                    }
                )
        else:
            # 普通用户可以使用邮箱或手机号登录
            # 移除手机号登录的限制
            pass
        
        # 验证密码
        password_valid = False
        if user:
            print(f"=== 密码验证调试信息 ===", file=sys.stderr)
            print(f"数据库存储的密码: '{user.password}'", file=sys.stderr)
            print(f"数据库密码类型: {type(user.password)}", file=sys.stderr)
            print(f"传入的密码: '{req.password}'", file=sys.stderr)
            print(f"传入密码类型: {type(req.password)}", file=sys.stderr)
            
            password_valid = verify_password(req.password, user.password)
            print(f"密码验证结果: {password_valid}", file=sys.stderr)
        
        if not password_valid:
            print(f"=== 登录失败调试信息 ===", file=sys.stderr)
            print(f"用户: '{user.username}'")
            print(f"密码验证失败", file=sys.stderr)
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
                user.is_vip = False
                db.commit()
        
        

        
        # 更新登录信息
        user.last_login_ip = request.client.host
        user.last_login_time = datetime.now()
        
        # 记录每日登录
        from models.users import UserLoginRecord
        from datetime import date
        today = date.today()
        
        # 检查今天是否已经记录过登录
        existing_record = db.query(UserLoginRecord).filter(
            UserLoginRecord.user_id == user.id,
            UserLoginRecord.login_date == today
        ).first()
        
        # 如果今天还没有记录，则添加登录记录
        if not existing_record:
            login_record = UserLoginRecord(
                user_id=user.id,
                login_date=today,
                login_time=datetime.now(),
                login_ip=request.client.host
            )
            db.add(login_record)
        
        db.commit()
        
        # 生成令牌
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        log_user_action(user.id, "login", f"用户登录: {user.username}")
        
        # 检查用户是否需要修改密码
        # 优先检查用户的need_change_password字段的值
        need_change_password = False
        if hasattr(user, 'need_change_password'):
            need_change_password = user.need_change_password
        else:
            # 对于新用户，默认需要修改密码
            # 检查用户的密码是否是默认密码
            default_password = os.getenv("DEFAULT_USER_PASSWORD", "changeme123")
            if verify_password(default_password, user.password):
                need_change_password = True
        
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
    """微信登录接口（用于小程序登录，开发模式自动降级为模拟登录）"""
    try:
        import httpx
        import hashlib
        
        appid = settings.WECHAT_APP_ID
        secret = settings.WECHAT_APP_SECRET
        openid = None
        unionid = None
        mock_login = False
        
        if appid and secret:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://api.weixin.qq.com/sns/jscode2session",
                        params={
                            "appid": appid,
                            "secret": secret,
                            "js_code": req.code,
                            "grant_type": "authorization_code"
                        },
                        timeout=10.0
                    )
                    
                    wechat_data = response.json()
                    
                    if "errcode" in wechat_data and wechat_data["errcode"] != 0:
                        log_error(f"微信API返回错误: {wechat_data}, 降级为模拟登录")
                        mock_login = True
                    else:
                        openid = wechat_data.get("openid")
                        unionid = wechat_data.get("unionid")
            except Exception as e:
                log_error(f"微信API调用异常: {str(e)}, 降级为模拟登录")
                mock_login = True
        else:
            mock_login = True
        
        if mock_login or not openid:
            openid = f"mock_{hashlib.md5(req.code.encode()).hexdigest()[:16]}"
            log_user_action(0, "mock_wechat_login", f"开发模式模拟登录, code={req.code[:8]}...")
        
        user = db.query(User).filter(User.wx_openid == openid).first()
        
        if not user:
            import uuid
            temp_username = f"wx_{openid[:16]}"
            temp_email = f"{openid[:16]}@wechat.local"
            
            new_user = User(
                username=temp_username,
                email=temp_email,
                phone=None,
                password="",
                register_ip=request.client.host,
                is_active=True,
                is_admin=False,
                user_type=1,
                is_vip=False,
                wx_openid=openid,
                wx_unionid=unionid,
                phone_bound=False,
                trial_status=0
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            default_subscription = UserSubscription(
                user_id=new_user.id,
                subscribe_type=3,
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
        
        if user.is_vip and user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                user.is_vip = False
                user.user_type = 1
                db.commit()
        
        user.last_login_ip = request.client.host
        user.last_login_time = datetime.now()
        
        from models.users import UserLoginRecord
        from datetime import date
        today = date.today()
        
        existing_record = db.query(UserLoginRecord).filter(
            UserLoginRecord.user_id == user.id,
            UserLoginRecord.login_date == today
        ).first()
        
        if not existing_record:
            login_record = UserLoginRecord(
                user_id=user.id,
                login_date=today,
                login_time=datetime.now(),
                login_ip=request.client.host
            )
            db.add(login_record)
        
        db.commit()
        
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
                    "avatar": user.avatar,
                    "real_name": user.real_name,
                    "is_admin": user.is_admin,
                    "is_vip": user.is_vip,
                    "user_type": user.user_type,
                    "is_trial": user.trial_status == 1,
                    "vip_type": user.vip_type,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "phone_bound": user.phone_bound,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
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
                user.is_vip = False
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

@router.get("/user")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户的信息"""
    return {
        "success": True,
        "code": 200,
        "message": "获取用户信息成功",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "phone": current_user.phone,
            "real_name": current_user.real_name,
            "gender": current_user.gender,
            "birthdate": current_user.birthdate,
            "is_vip": current_user.is_vip,
            "vip_type": current_user.vip_type,
            "vip_start_time": current_user.vip_start_time,
            "vip_end_time": current_user.vip_end_time,
            "is_admin": current_user.is_admin,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at
        }
    }


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
            user.is_vip = False
            db.commit()
    
    return user

class SendSmsCodeRequest(BaseModel):
    """发送短信验证码请求模型"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    type: str = Field(..., description="验证码类型: login/reset_password")

    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v

    @validator('type')
    def validate_code_type(cls, v):
        if v not in ['login', 'reset_password']:
            raise ValueError('验证码类型不正确')
        return v

class ResetPasswordByPhoneRequest(BaseModel):
    """手机号重置密码请求模型"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, description="新密码")

    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v

    @validator('new_password')
    def validate_password(cls, v):
        if not validate_pwd(v):
            raise ValueError('密码强度不足，至少包含6个字符且包含字母和数字')
        return v

@router.post("/send-sms-code", response_model=AuthResponse, summary="发送验证码")
async def send_sms_code(
    req: SendSmsCodeRequest,
    db: Session = Depends(get_db_common)
):
    """发送邮件验证码接口"""
    try:
        # 检查手机号是否已注册
        user = db.query(User).filter(User.phone == req.phone).first()
        
        if req.type == 'reset_password' and not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "手机号未注册",
                    "data": None
                }
            )
        
        # 生成验证码
        from core.security import generate_verification_code
        code = generate_verification_code()
        
        # 发送邮件验证码
        from core.push_manager import send_email
        email_subject = "密码重置验证码"
        email_content = f"您的密码重置验证码是：{code}，有效期为5分钟。"
        
        if not send_email(user.email, email_subject, email_content):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "code": 500,
                    "message": "发送验证码失败，请稍后重试",
                    "data": None
                }
            )
        
        # 打印验证码，方便测试
        print(f"邮件验证码已发送到 {user.email}，验证码: {code}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "验证码已发送到您的邮箱",
                "data": {
                    "phone": req.phone,
                    "email": user.email
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

@router.post("/reset-password-by-phone", response_model=AuthResponse, summary="手机号重置密码")
async def reset_password_by_phone(
    req: ResetPasswordByPhoneRequest,
    db: Session = Depends(get_db_common)
):
    """手机号重置密码接口"""
    try:
        # 查找用户
        user = db.query(User).filter(User.phone == req.phone).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "手机号未注册",
                    "data": None
                }
            )
        
        # 验证验证码（这里简化处理，实际项目中应该从缓存或数据库中验证）
        # 暂时假设验证码正确
        
        # 更新密码
        user.password = get_password_hash(req.new_password)
        # 标记用户已修改密码
        if hasattr(user, 'need_change_password'):
            user.need_change_password = False
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
    old_password: Optional[str] = Field(None, description="旧密码（第一次登录时可选）")
    new_password: str = Field(..., min_length=6, description="新密码")

@router.post("/change-password", response_model=AuthResponse, summary="修改密码")
async def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """修改密码接口"""
    try:
        # 检查用户是否是第一次登录
        if current_user.need_change_password:
            # 第一次登录，不需要验证旧密码
            if not req.new_password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "请输入新密码",
                        "data": None
                    }
                )
        else:
            # 不是第一次登录，需要验证旧密码
            if not req.old_password or not req.new_password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "请输入旧密码和新密码",
                        "data": None
                    }
                )
            
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
        
        # 验证新密码
        if len(req.new_password) < 6:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "新密码长度至少6位",
                    "data": None
                }
            )
        
        # 更新密码
        current_user.password = get_password_hash(req.new_password)
        # 标记用户已修改密码
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
            user.is_vip = False
            db.commit()
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    
    return user


class WechatLoginRequest2(BaseModel):
    code: str = Field(..., description="微信登录code")
    userInfo: Optional[dict] = Field(None, description="微信用户信息")


@router.post("/wechat-login-v2", summary="微信登录(兼容旧接口)")
async def wechat_login_v2(
    request: Request,
    req: WechatLoginRequest2,
    db: Session = Depends(get_db_common)
):
    """微信登录 - 兼容旧接口，开发模式自动降级为模拟登录"""
    import httpx
    import hashlib
    
    try:
        appid = settings.WECHAT_APP_ID
        secret = settings.WECHAT_APP_SECRET
        openid = None
        unionid = None
        mock_login = False
        
        if appid and secret:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://api.weixin.qq.com/sns/jscode2session",
                        params={
                            "appid": appid,
                            "secret": secret,
                            "js_code": req.code,
                            "grant_type": "authorization_code"
                        },
                        timeout=10.0
                    )
                    
                    wechat_data = response.json()
                    
                    if "errcode" in wechat_data and wechat_data["errcode"] != 0:
                        log_error(f"微信API返回错误: {wechat_data}, 降级为模拟登录")
                        mock_login = True
                    else:
                        openid = wechat_data.get("openid")
                        unionid = wechat_data.get("unionid")
            except Exception as e:
                log_error(f"微信API调用异常: {str(e)}, 降级为模拟登录")
                mock_login = True
        else:
            mock_login = True
        
        if mock_login or not openid:
            openid = f"mock_{hashlib.md5(req.code.encode()).hexdigest()[:16]}"
            log_user_action(0, "mock_wechat_login", f"开发模式模拟登录(旧接口), code={req.code[:8]}...")
        
        user = db.query(User).filter(User.wx_openid == openid).first()
        
        if user:
            if req.userInfo and req.userInfo.get("avatarUrl"):
                user.avatar = req.userInfo.get("avatarUrl")
            if req.userInfo and req.userInfo.get("nickName"):
                if not user.real_name:
                    user.real_name = req.userInfo.get("nickName")
            user.last_login_time = datetime.now()
            user.last_login_ip = request.client.host
            
            from models.users import UserLoginRecord
            from datetime import date
            today = date.today()
            
            existing_record = db.query(UserLoginRecord).filter(
                UserLoginRecord.user_id == user.id,
                UserLoginRecord.login_date == today
            ).first()
            
            if not existing_record:
                login_record = UserLoginRecord(
                    user_id=user.id,
                    login_date=today,
                    login_time=datetime.now(),
                    login_ip=request.client.host
                )
                db.add(login_record)
            
            db.commit()
        else:
            temp_username = f"wx_{openid[:16]}"
            temp_email = f"{openid[:16]}@wechat.local"
            avatar = req.userInfo.get("avatarUrl", "") if req.userInfo else ""
            real_name = req.userInfo.get("nickName") if req.userInfo else None
            
            user = User(
                username=temp_username,
                email=temp_email,
                phone=None,
                password="",
                avatar=avatar,
                real_name=real_name,
                is_active=True,
                is_admin=False,
                user_type=1,
                is_vip=False,
                wx_openid=openid,
                wx_unionid=unionid,
                phone_bound=False,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            default_subscription = UserSubscription(
                user_id=user.id,
                subscribe_type=3,
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
            
            from models.users import UserLoginRecord
            from datetime import date
            today = date.today()
            
            login_record = UserLoginRecord(
                user_id=user.id,
                login_date=today,
                login_time=datetime.now(),
                login_ip=request.client.host
            )
            db.add(login_record)
            db.commit()
        
        if user.is_vip and user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                user.is_vip = False
                user.user_type = 1
                db.commit()
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "登录成功",
                "data": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "avatar": user.avatar,
                    "real_name": user.real_name,
                    "is_admin": user.is_admin,
                    "is_vip": user.is_vip,
                    "user_type": user.user_type,
                    "vip_type": user.vip_type or 0,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "phone_bound": user.phone_bound,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": 604800
                }
            }
        )
        
    except Exception as e:
        log_error(f"微信登录异常: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"登录失败: {str(e)}",
                "data": None
            }
        )


class BindPhoneRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    code: str = Field(..., min_length=4, max_length=6, description="验证码")

    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v


@router.post("/bind-phone", response_model=AuthResponse, summary="绑定手机号")
async def bind_phone(
    req: BindPhoneRequest,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """绑定手机号接口"""
    try:
        if current_user.phone_bound and current_user.phone:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "您已绑定手机号",
                    "data": None
                }
            )
        
        existing_user = db.query(User).filter(
            User.phone == req.phone,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该手机号已被其他用户绑定",
                    "data": None
                }
            )
        
        current_user.phone = req.phone
        current_user.phone_bound = True
        db.commit()
        
        log_user_action(current_user.id, "bind_phone", f"用户绑定手机号: {req.phone}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "手机号绑定成功",
                "data": {
                    "user_id": current_user.id,
                    "phone": current_user.phone,
                    "phone_bound": True
                }
            }
        )
        
    except Exception as e:
        log_error(f"绑定手机号失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "绑定手机号失败，请稍后重试",
                "data": None
            }
        )


class PhoneLoginRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    code: str = Field(..., min_length=4, max_length=6, description="验证码")

    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v


@router.post("/phone-login", response_model=AuthResponse, summary="手机号验证码登录")
async def phone_login(
    request: Request,
    req: PhoneLoginRequest,
    db: Session = Depends(get_db_common)
):
    """手机号验证码登录接口"""
    try:
        user = db.query(User).filter(User.phone == req.phone).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "code": 401,
                    "message": "该手机号未注册，请先使用微信登录后绑定手机号",
                    "data": None
                }
            )
        
        if user.is_vip and user.vip_end_time:
            if datetime.now() > user.vip_end_time:
                user.is_vip = False
                user.user_type = 1
                db.commit()
        
        user.last_login_ip = request.client.host
        user.last_login_time = datetime.now()
        
        from models.users import UserLoginRecord
        from datetime import date
        today = date.today()
        
        existing_record = db.query(UserLoginRecord).filter(
            UserLoginRecord.user_id == user.id,
            UserLoginRecord.login_date == today
        ).first()
        
        if not existing_record:
            login_record = UserLoginRecord(
                user_id=user.id,
                login_date=today,
                login_time=datetime.now(),
                login_ip=request.client.host
            )
            db.add(login_record)
        
        db.commit()
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        log_user_action(user.id, "phone_login", f"手机号登录: {user.phone}")
        
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
                    "avatar": user.avatar,
                    "real_name": user.real_name,
                    "is_admin": user.is_admin,
                    "is_vip": user.is_vip,
                    "user_type": user.user_type,
                    "is_trial": user.trial_status == 1,
                    "vip_type": user.vip_type,
                    "vip_end_time": user.vip_end_time.isoformat() if user.vip_end_time else None,
                    "phone_bound": user.phone_bound,
                    "need_change_password": user.need_change_password,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                }
            }
        )
        
    except Exception as e:
        log_error(f"手机号登录失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "登录失败，请稍后重试",
                "data": None
            }
        )


class SendPhoneCodeRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    type: str = Field(..., description="验证码类型: login/bind_phone/reset_password")

    @validator('phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('手机号格式不正确')
        return v

    @validator('type')
    def validate_code_type(cls, v):
        if v not in ['login', 'bind_phone', 'reset_password']:
            raise ValueError('验证码类型不正确')
        return v


@router.post("/send-phone-code", response_model=AuthResponse, summary="发送手机验证码")
async def send_phone_code(
    req: SendPhoneCodeRequest,
    db: Session = Depends(get_db_common)
):
    """发送手机验证码接口"""
    try:
        from core.security import generate_verification_code
        
        user = db.query(User).filter(User.phone == req.phone).first()
        
        if req.type == 'bind_phone' and user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该手机号已被其他用户绑定",
                    "data": None
                }
            )
        
        if req.type == 'login' and not user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该手机号未注册，请先使用微信登录后绑定手机号",
                    "data": None
                }
            )
        
        code = generate_verification_code()
        
        if user and user.email:
            from core.push_manager import send_email
            email_subject = "验证码通知"
            email_content = f"尊敬的用户：\n\n您正在进行{('登录' if req.type == 'login' else '绑定手机号' if req.type == 'bind_phone' else '重置密码')}操作，验证码为：{code}，有效期为5分钟。\n\n如非本人操作，请忽略此邮件。\n\n双赛道情报通团队"
            send_email(user.email, email_subject, email_content)
        
        print(f"[验证码] 手机号: {req.phone}, 类型: {req.type}, 验证码: {code}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "验证码已发送",
                "data": {
                    "phone": req.phone
                }
            }
        )
        
    except Exception as e:
        log_error(f"发送手机验证码失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "发送验证码失败，请稍后重试",
                "data": None
            }
        )


@router.post("/record-activity", summary="记录用户活跃")
async def record_activity(
    request: Request,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """记录用户今日活跃（小程序打开时调用）"""
    try:
        today = date.today()
        
        existing_record = db.query(UserLoginRecord).filter(
            UserLoginRecord.user_id == current_user.id,
            UserLoginRecord.login_date == today
        ).first()
        
        if not existing_record:
            login_record = UserLoginRecord(
                user_id=current_user.id,
                login_date=today,
                login_time=datetime.now(),
                login_ip=request.client.host if request.client else None
            )
            db.add(login_record)
            db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "活跃记录成功",
                "data": {"is_active_today": True}
            }
        )
    except Exception as e:
        log_error(f"记录活跃失败: {str(e)}")
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "记录活跃失败但不影响使用",
                "data": {"is_active_today": False}
            }
        )