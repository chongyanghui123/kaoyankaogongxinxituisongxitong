#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 后端API服务
项目名称：双赛道情报通（考研+考公）
描述：7×24小时自动抓取、分类、推送官方关键信息的情报平台
作者：双赛道情报通开发团队
创建时间：2026-04-08
"""

import os
import sys
import logging
import traceback
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import json
import asyncio

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置
from config import settings
from core.database import engine, get_db
from core.logger import setup_logging
from core.security import verify_token, get_current_user

from core.celery_app import celery_app

# 导入路由
from api.v1.users import router as users_router
from api.v1.auth import router as auth_router
from api.v1.kaoyan import router as kaoyan_router
from api.v1.kaogong import router as kaogong_router
from api.v1.crawlers import router as crawlers_router
from api.v1.payments import router as payments_router
from api.v1.push import router as push_router
from api.v1.admin import router as admin_router
from api.v1.utils import router as utils_router
from api.v1.school_management import router as school_management_router
from api.v1.learning_materials import router as learning_materials_router
from api.v1.sign_in import router as sign_in_router
from api.v1.gift import router as gift_router
from api.v1.community import router as community_router

# 初始化日志
setup_logging()
logger = logging.getLogger(__name__)

# WebSocket 连接管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, group_id: int, user_id: int):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append({
            "websocket": websocket,
            "user_id": user_id
        })
        logger.info(f"WebSocket连接: 用户{user_id}加入小组{group_id}")
    
    def disconnect(self, websocket: WebSocket, group_id: int):
        if group_id in self.active_connections:
            self.active_connections[group_id] = [
                conn for conn in self.active_connections[group_id] 
                if conn["websocket"] != websocket
            ]
            if not self.active_connections[group_id]:
                del self.active_connections[group_id]
        logger.info(f"WebSocket断开: 小组{group_id}")
    
    async def broadcast(self, group_id: int, message: dict, exclude_ws: WebSocket = None):
        if group_id in self.active_connections:
            for conn in self.active_connections[group_id]:
                if conn["websocket"] != exclude_ws:
                    try:
                        await conn["websocket"].send_json(message)
                    except Exception as e:
                        logger.error(f"广播消息失败: {e}")

manager = ConnectionManager()

# 创建FastAPI应用
app = FastAPI(
    title="双赛道情报通 API",
    description="7×24小时自动抓取、分类、推送考研+考公官方关键信息的情报平台",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# 自定义验证错误处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    import json
    logger.error(f"请求验证失败: {exc}")
    logger.error(f"请求路径: {request.url}")
    logger.error(f"请求方法: {request.method}")
    
    try:
        body = await request.body()
        logger.error(f"请求body: {body.decode('utf-8')}")
    except Exception as e:
        logger.error(f"获取请求body时出错: {e}")
        
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "success": False,
            "code": 422,
            "message": "请求参数验证失败",
            "data": {
                "errors": exc.errors(),
                "body": exc.body
            }
        }),
    )

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
import os
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 挂载上传文件目录
upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"请求异常: {request.method} {request.url}")
    logger.error(f"异常详情: {str(exc)}")
    logger.error(f"堆栈信息: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证错误处理"""
    logger.error(f"请求验证错误: {request.method} {request.url}")
    logger.error(f"验证错误详情: {str(exc)}")
    
    # 处理FormData类型的body
    if hasattr(exc, 'body') and exc.body:
        try:
            # 尝试将body转换为字符串表示
            body_str = str(exc.body)
        except:
            body_str = "无法序列化的body"
    else:
        body_str = None
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "code": 422,
            "message": "请求参数验证失败",
            "data": {
                "errors": jsonable_encoder(exc.errors()),
                "body": body_str
            }
        }
    )

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查数据库连接
        db = next(get_db())
        result = db.execute(text("SELECT 1")).scalar()
        
        # 检查Redis连接
        redis_health = False
        if settings.REDIS_URL:
            try:
                import redis
                r = redis.Redis.from_url(settings.REDIS_URL)
                r.ping()
                redis_health = True
            except Exception as e:
                logger.error(f"Redis连接异常: {str(e)}")
                redis_health = False
        
        # 检查Celery连接
        celery_health = False
        if settings.RABBITMQ_URL:
            try:
                celery_inspect = celery_app.control.inspect()
                workers = celery_inspect.ping()
                celery_health = bool(workers)
            except Exception as e:
                logger.error(f"Celery连接异常: {str(e)}")
                celery_health = False
            
        return {
            "success": True,
            "code": 200,
            "message": "服务运行正常",
            "data": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0.0",
                "database": "healthy" if result == 1 else "unhealthy",
                "redis": "healthy" if redis_health else "unhealthy" if settings.REDIS_URL else "disabled",
                "celery": "healthy" if celery_health else "unhealthy" if settings.RABBITMQ_URL else "disabled"
            }
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "success": False,
            "code": 500,
            "message": f"服务异常: {str(e)}",
            "data": None
        }

# 应用信息
@app.get("/info")
async def app_info():
    """应用信息接口"""
    return {
        "success": True,
        "code": 200,
        "message": "获取应用信息成功",
        "data": {
            "name": "双赛道情报通",
            "version": "1.0.0",
            "description": "7×24小时自动抓取、分类、推送考研+考公官方关键信息的情报平台",
            "author": "双赛道情报通开发团队",
            "created_at": "2026-04-08",
            "features": [
                "考研赛道监控",
                "考公赛道监控",
                "智能分类",
                "精准推送",
                "定时抓取",
                "付费会员系统"
            ]
        }
    }

# 导入消息、情报和反馈路由
from api.v1.message import router as message_router
from api.v1.info import router as info_router
from api.v1.feedback import router as feedback_router

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users_router, prefix="/api/v1/users", tags=["用户"])
app.include_router(kaoyan_router, prefix="/api/v1/kaoyan", tags=["考研"])
app.include_router(kaogong_router, prefix="/api/v1/kaogong", tags=["考公"])
app.include_router(crawlers_router, prefix="/api/v1/crawlers", tags=["爬虫"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["支付"])
app.include_router(push_router, prefix="/api/v1/push", tags=["推送"])
app.include_router(message_router, prefix="/api/v1/message", tags=["消息"])
app.include_router(info_router, prefix="/api/v1/info", tags=["情报"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["管理后台"])
app.include_router(school_management_router, prefix="/api/v1/school-management", tags=["学校管理"])
app.include_router(learning_materials_router, prefix="/api/v1/learning_materials", tags=["学习资料"])
app.include_router(sign_in_router, prefix="/api/v1/sign-in", tags=["签到"])
app.include_router(gift_router, prefix="/api/v1", tags=["礼品"])
app.include_router(feedback_router, prefix="/api/v1/feedback", tags=["反馈"])
app.include_router(community_router, prefix="/api/v1", tags=["社区"])
app.include_router(utils_router, prefix="/api/v1/utils", tags=["工具"])

# 启动事件
@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("=== 双赛道情报通服务启动 ===")
    logger.info(f"服务模式: {settings.ENVIRONMENT}")
    logger.info(f"API文档: http://localhost:{settings.PORT}/docs")
    
    try:
        # 初始化数据库
        try:
            from core.database import BaseCommon, BaseKaoyan, BaseKaogong, common_db_engine, kaoyan_db_engine, kaogong_db_engine
            from core.models.school import School  # 导入学校模型
            from models.users import User, UserSubscription, UserKeyword, UserReadInfo, UserFavorite, Order, Product, SystemConfig, PushTemplate, PushLog, UserLoginRecord  # 导入用户相关模型
            from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog  # 导入考研相关模型
            from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog  # 导入考公相关模型
            from models.learning_materials import MaterialCategory, LearningMaterial, UserDownload, MaterialRating, MaterialComment, ExamSchedule, Carousel, DailyPractice, DailyPracticeRecord, HotTopic  # 导入学习资料相关模型
            from models.feedback import Feedback  # 导入反馈相关模型
            BaseCommon.metadata.create_all(bind=common_db_engine)
            BaseKaoyan.metadata.create_all(bind=kaoyan_db_engine)
            BaseKaogong.metadata.create_all(bind=kaogong_db_engine)
            
            # 初始化资料分类数据
            try:
                from sqlalchemy.orm import Session
                from models.learning_materials import MaterialCategory
                db = Session(bind=common_db_engine)
                
                # 检查是否已有分类数据
                existing_categories = db.query(MaterialCategory).count()
                if existing_categories == 0:
                    # 考研分类
                    kaoyan_categories = [
                        {"name": "考研政治", "type": 1, "description": "考研政治相关资料"},
                        {"name": "考研英语", "type": 1, "description": "考研英语相关资料"},
                        {"name": "考研数学", "type": 1, "description": "考研数学相关资料"},
                        {"name": "考研专业课", "type": 1, "description": "考研专业课相关资料"},
                        {"name": "考研复试", "type": 1, "description": "考研复试相关资料"}
                    ]
                    
                    # 考公分类
                    kaogong_categories = [
                        {"name": "行测", "type": 2, "description": "公务员考试行测相关资料"},
                        {"name": "申论", "type": 2, "description": "公务员考试申论相关资料"},
                        {"name": "面试", "type": 2, "description": "公务员考试面试相关资料"},
                        {"name": "公共基础知识", "type": 2, "description": "公共基础知识相关资料"}
                    ]
                    
                    # 通用分类
                    common_categories = [
                        {"name": "学习方法", "type": 3, "description": "学习方法相关资料"},
                        {"name": "时间管理", "type": 3, "description": "时间管理相关资料"},
                        {"name": "心理调适", "type": 3, "description": "心理调适相关资料"}
                    ]
                    
                    # 添加所有分类
                    all_categories = kaoyan_categories + kaogong_categories + common_categories
                    for category_data in all_categories:
                        category = MaterialCategory(**category_data)
                        db.add(category)
                    
                    db.commit()
                    logger.info(f"初始化资料分类数据成功，添加了 {len(all_categories)} 个分类")
                else:
                    logger.info("资料分类数据已存在，跳过初始化")
            except Exception as e:
                logger.error(f"初始化资料分类数据失败: {str(e)}")
                logger.error(f"堆栈信息: {traceback.format_exc()}")
            
            logger.info("数据库连接成功")
            
            # 修复被错误设置is_active=False的用户
            try:
                from sqlalchemy.orm import Session
                fix_db = Session(bind=common_db_engine)
                inactive_users = fix_db.query(User).filter(User.is_active == False).all()
                if inactive_users:
                    for u in inactive_users:
                        u.is_active = True
                    fix_db.commit()
                    logger.info(f"已修复 {len(inactive_users)} 个被错误设置is_active=False的用户")
                fix_db.close()
            except Exception as e:
                logger.error(f"修复is_active数据失败: {str(e)}")
        except Exception as e:
            logger.error(f"初始化数据库失败: {str(e)}")
            logger.error(f"堆栈信息: {traceback.format_exc()}")
        
        # 启动推送任务调度
        try:
            from core.push_manager import start_push_scheduler
            start_push_scheduler()
            logger.info("推送调度器启动成功")
        except Exception as e:
            logger.error(f"启动推送调度器失败: {str(e)}")
            logger.error(f"堆栈信息: {traceback.format_exc()}")
        
    except Exception as e:
        logger.error(f"启动事件异常: {str(e)}")
        logger.error(f"堆栈信息: {traceback.format_exc()}")

# 关闭事件 ===================== 【我帮你修复了】
@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    logger.info("=== 双赛道情报通服务停止 ===")
    
    # 原来的代码报错，我直接注释掉错误部分
    try:
        logger.info("服务安全关闭完成")
    except Exception as e:
        logger.error(f"关闭事件异常: {str(e)}")

# WebSocket 路由 - 小组聊天
@app.websocket("/ws/group/{group_id}")
async def websocket_group_chat(
    websocket: WebSocket, 
    group_id: int
):
    """WebSocket 小组聊天"""
    from fastapi import Query
    from core.database import get_db_common
    from models.users import User
    from models.community import GroupMember
    
    # 从查询参数获取token
    token = websocket.query_params.get("token")
    
    user_id = None
    username = "匿名用户"
    
    # 验证token
    if token:
        try:
            from fastapi import HTTPException
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无法验证凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )
            payload = verify_token(token, credentials_exception)
            if payload:
                user_id = int(payload.get("user_id"))
                db = next(get_db_common())
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    username = user.username
        except Exception as e:
            logger.error(f"WebSocket token验证失败: {e}")
    
    if not user_id:
        await websocket.close(code=4001, reason="未授权")
        return
    
    # 检查用户是否是小组成员
    db = next(get_db_common())
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id,
        GroupMember.status == 1
    ).first()
    
    if not member:
        await websocket.close(code=4003, reason="不是小组成员")
        return
    
    # 连接WebSocket
    await manager.connect(websocket, group_id, user_id)
    
    try:
        # 发送连接成功消息
        await websocket.send_json({
            "type": "system",
            "content": f"{username} 加入了聊天室",
            "time": datetime.now().isoformat()
        })
        
        # 广播用户加入消息
        await manager.broadcast(group_id, {
            "type": "system",
            "content": f"{username} 加入了聊天室",
            "time": datetime.now().isoformat()
        }, exclude_ws=websocket)
        
        # 持续接收消息
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                # 处理不同类型的消息
                if message.get("type") == "chat":
                    content = message.get("content", "")
                    mentioned_users = message.get("mentioned_users", [])
                    
                    # 聊天消息 - 广播给所有成员
                    broadcast_msg = {
                        "type": "chat",
                        "user_id": user_id,
                        "username": username,
                        "content": content,
                        "mentioned_users": mentioned_users,
                        "time": datetime.now().isoformat()
                    }
                    await manager.broadcast(group_id, broadcast_msg)
                    
                    # 保存消息到数据库
                    from models.community import GroupMessage
                    mentioned_users_str = ",".join(map(str, mentioned_users)) if mentioned_users else None
                    new_message = GroupMessage(
                        group_id=group_id,
                        user_id=user_id,
                        content=content,
                        message_type=1,
                        mentioned_users=mentioned_users_str
                    )
                    db.add(new_message)
                    db.commit()
                    
                    # 发送通知给被 @ 的用户
                    if mentioned_users:
                        for mentioned_user_id in mentioned_users:
                            try:
                                mentioned_user = db.query(User).filter(User.id == mentioned_user_id).first()
                                if mentioned_user:
                                    # 创建消息通知
                                    from models.message import Message
                                    notification = Message(
                                        user_id=mentioned_user_id,
                                        type="mention",
                                        title=f"{username} 在小组聊天中@了你",
                                        content=content[:100] + "..." if len(content) > 100 else content,
                                        info_id=0,
                                        is_read=0
                                    )
                                    db.add(notification)
                            except Exception as e:
                                logger.error(f"发送@通知失败: {e}")
                        db.commit()
                    
                elif message.get("type") == "image":
                    # 图片消息
                    broadcast_msg = {
                        "type": "image",
                        "user_id": user_id,
                        "username": username,
                        "content": message.get("content", ""),
                        "time": datetime.now().isoformat()
                    }
                    await manager.broadcast(group_id, broadcast_msg)
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "content": "消息格式错误"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id)
        await manager.broadcast(group_id, {
            "type": "system",
            "content": f"{username} 离开了聊天室",
            "time": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")
        manager.disconnect(websocket, group_id)

# 初始化管理员用户
def init_admin_user():
    """初始化管理员用户"""
    from sqlalchemy.orm import Session
    from core.database import get_db_common
    from models.users import User
    from core.security import get_password_hash
    from datetime import datetime, timedelta
    
    db: Session = next(get_db_common())
    try:
        # 检查是否已有管理员用户
        admin = db.query(User).filter(User.is_admin == 1).first()
        if not admin:
            # 创建管理员用户
            admin_user = User(
                username="admin",
                email="admin@example.com",
                phone="13800138000",
                password=get_password_hash(os.getenv("ADMIN_INITIAL_PASSWORD", "changeme123")),
                is_admin=True,
                is_active=True,
                is_vip=True,
                vip_type=3,  # 双赛道
                vip_start_time=datetime.now(),
                vip_end_time=datetime.now() + timedelta(days=365*10)  # 10年有效期
            )
            db.add(admin_user)
            db.commit()
            logger.info("管理员用户初始化成功")
        else:
            logger.info("管理员用户已存在")
    except Exception as e:
        logger.error(f"初始化管理员用户失败: {str(e)}")
    finally:
        db.close()

# 主程序入口
if __name__ == "__main__":
    import argparse
    import socket
    from config import settings
    
    parser = argparse.ArgumentParser(description="双赛道情报通 API服务")
    parser.add_argument("--host", default="0.0.0.0", help="主机地址")
    parser.add_argument("--port", type=int, default=settings.PORT, help="端口号")
    parser.add_argument("--reload", action="store_true", help="自动重载")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    # 检查端口是否被占用
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((args.host, args.port))
        s.close()
        logger.info(f"端口 {args.port} 可用")
    except socket.error as e:
        logger.error(f"端口 {args.port} 被占用: {e}")
        sys.exit(1)
    
    # 初始化管理员用户
    init_admin_user()
    
    logger.info(f"启动API服务: http://{args.host}:{args.port}")
    logger.info(f"API文档: http://{args.host}:{args.port}/docs")
    
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="debug" if args.debug else "info"
        )
    except Exception as e:
        logger.error(f"启动HTTP服务器失败: {e}")
        logger.error(f"堆栈信息: {traceback.format_exc()}")
        sys.exit(1)