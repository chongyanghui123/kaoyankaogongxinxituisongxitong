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
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置
from config import settings
from core.database import engine, get_db
from core.logger import setup_logging
from core.security import verify_token, get_current_user
from core.scheduler import scheduler
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

# 初始化日志
setup_logging()
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="双赛道情报通 API",
    description="7×24小时自动抓取、分类、推送考研+考公官方关键信息的情报平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查数据库连接
        db = next(get_db())
        result = db.execute(text("SELECT 1")).scalar()
        
        # 检查Redis连接
        try:
            import redis
            r = redis.Redis.from_url(settings.REDIS_URL)
            r.ping()
            redis_health = True
        except Exception as e:
            logger.error(f"Redis连接异常: {str(e)}")
            redis_health = False
        
        # 检查Celery连接
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
                "redis": "healthy" if redis_health else "unhealthy",
                "celery": "healthy" if celery_health else "unhealthy"
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

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users_router, prefix="/api/v1/users", tags=["用户"])
app.include_router(kaoyan_router, prefix="/api/v1/kaoyan", tags=["考研"])
app.include_router(kaogong_router, prefix="/api/v1/kaogong", tags=["考公"])
app.include_router(crawlers_router, prefix="/api/v1/crawlers", tags=["爬虫"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["支付"])
app.include_router(push_router, prefix="/api/v1/push", tags=["推送"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["管理后台"])
app.include_router(school_management_router, prefix="/api/v1/school-management", tags=["学校管理"])
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
            from models.users import User, UserSubscription, UserKeyword, UserReadInfo, UserFavorite, Order, Product, SystemConfig, PushTemplate, PushLog  # 导入用户相关模型
            from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog  # 导入考研相关模型
            from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog  # 导入考公相关模型
            BaseCommon.metadata.create_all(bind=common_db_engine)
            BaseKaoyan.metadata.create_all(bind=kaoyan_db_engine)
            BaseKaogong.metadata.create_all(bind=kaogong_db_engine)
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"初始化数据库失败: {str(e)}")
            logger.error(f"堆栈信息: {traceback.format_exc()}")
        
        # 启动爬虫调度（只执行一次，不开启定时任务）
        try:
            import asyncio
            from core.crawler_manager import start_crawler_scheduler
            # 异步执行，不阻塞服务启动
            asyncio.create_task(start_crawler_scheduler())
            logger.info("爬虫调度器已启动（只执行一次）")
        except Exception as e:
            logger.error(f"启动爬虫调度器失败: {str(e)}")
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

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    logger.info("=== 双赛道情报通服务停止 ===")
    
    try:
        # 停止调度器
        scheduler.shutdown()
        logger.info("调度器停止成功")
        
    except Exception as e:
        logger.error(f"关闭事件异常: {str(e)}")
        logger.error(f"堆栈信息: {traceback.format_exc()}")

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
                password="admin123",  # 存储明文密码
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
    
    parser = argparse.ArgumentParser(description="双赛道情报通 API服务")
    parser.add_argument("--host", default="0.0.0.0", help="主机地址")
    parser.add_argument("--port", type=int, default=8000, help="端口号")
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