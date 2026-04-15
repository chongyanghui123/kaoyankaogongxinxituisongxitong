#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 爬虫路由
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, Field, validator

from config import settings
from core.database import get_db_kaoyan, get_db_kaogong
from core.security import get_current_active_admin
from core.logger import log_system_event, log_error
from models.kaoyan import KaoyanCrawlerConfig, KaoyanCrawlerLog
from models.kaogong import KaogongCrawlerConfig, KaogongCrawlerLog

router = APIRouter()

class CrawlerConfigRequest(BaseModel):
    """爬虫配置请求模型"""
    name: str = Field(..., min_length=1, max_length=100, description="配置名称")
    url: str = Field(..., min_length=10, max_length=500, description="监控网址")
    selector: Optional[str] = Field(None, description="页面选择器")
    parse_rules: Optional[dict] = Field(None, description="解析规则")
    interval: int = Field(..., ge=1, le=1440, description="抓取间隔(分钟)")
    status: int = Field(..., ge=0, le=1, description="状态: 1-启用, 0-禁用")
    priority: int = Field(..., ge=0, le=2, description="优先级: 0-普通, 1-高, 2-非常高")

class CrawlerLogResponse(BaseModel):
    """爬虫日志响应模型"""
    id: int
    config_id: int
    url: str
    status: int
    status_text: str
    info_count: int
    error_msg: Optional[str]
    crawl_time: str

class KaoyanCrawlerConfigResponse(BaseModel):
    """考研爬虫配置响应模型"""
    id: int
    name: str
    url: str
    selector: Optional[str]
    parse_rules: Optional[dict]
    interval: int
    status: int
    status_text: str
    priority: int
    priority_text: str
    last_crawl_time: Optional[str]
    next_crawl_time: Optional[str]
    created_at: str
    updated_at: str

class KaogongCrawlerConfigResponse(BaseModel):
    """考公爬虫配置响应模型"""
    id: int
    name: str
    url: str
    selector: Optional[str]
    parse_rules: Optional[dict]
    interval: int
    status: int
    status_text: str
    priority: int
    priority_text: str
    last_crawl_time: Optional[str]
    next_crawl_time: Optional[str]
    created_at: str
    updated_at: str

@router.get("/kaoyan/config", response_model=List[KaoyanCrawlerConfigResponse], summary="获取考研爬虫配置列表")
async def get_kaoyan_crawler_configs(
    status: Optional[int] = Query(None, ge=0, le=1, description="状态"),
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """获取考研爬虫配置列表"""
    try:
        query = db.query(KaoyanCrawlerConfig)
        
        if status is not None:
            query = query.filter(KaoyanCrawlerConfig.status == status)
        
        configs = query.order_by(KaoyanCrawlerConfig.priority.desc(), KaoyanCrawlerConfig.id).all()
        
        items = []
        for config in configs:
            # 处理parse_rules类型转换
            parse_rules = config.parse_rules
            if isinstance(parse_rules, str):
                import json
                try:
                    parse_rules = json.loads(parse_rules)
                except:
                    parse_rules = None
            
            items.append(KaoyanCrawlerConfigResponse(
                id=config.id,
                name=config.name,
                url=config.url,
                selector=config.selector,
                parse_rules=parse_rules,
                interval=config.interval,
                status=config.status,
                status_text=config.status_text,
                priority=config.priority,
                priority_text=config.priority_text,
                last_crawl_time=config.last_crawl_time.isoformat() if config.last_crawl_time else None,
                next_crawl_time=config.next_crawl_time.isoformat() if config.next_crawl_time else None,
                created_at=config.created_at.isoformat(),
                updated_at=config.updated_at.isoformat()
            ))
        
        return items
    except Exception as e:
        log_error(f"获取考研爬虫配置列表失败: {str(e)}")
        from fastapi import status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考研爬虫配置列表失败"
        )

@router.post("/kaoyan/config", response_model=KaoyanCrawlerConfigResponse, summary="添加考研爬虫配置")
async def add_kaoyan_crawler_config(
    req: CrawlerConfigRequest,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """添加考研爬虫配置"""
    try:
        # 检查URL是否已存在
        existing_config = db.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.url == req.url
        ).first()
        
        if existing_config:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该URL已存在",
                    "data": None
                }
            )
        
        # 创建新配置
        new_config = KaoyanCrawlerConfig(
            name=req.name,
            url=req.url,
            selector=req.selector,
            parse_rules=req.parse_rules,
            interval=req.interval,
            status=req.status,
            priority=req.priority
        )
        
        db.add(new_config)
        db.commit()
        db.refresh(new_config)
        
        log_system_event("add_kaoyan_crawler", f"添加考研爬虫配置: {req.name}")
        
        return KaoyanCrawlerConfigResponse(
            id=new_config.id,
            name=new_config.name,
            url=new_config.url,
            selector=new_config.selector,
            parse_rules=new_config.parse_rules,
            interval=new_config.interval,
            status=new_config.status,
            status_text=new_config.status_text,
            priority=new_config.priority,
            priority_text=new_config.priority_text,
            last_crawl_time=new_config.last_crawl_time.isoformat() if new_config.last_crawl_time else None,
            next_crawl_time=new_config.next_crawl_time.isoformat() if new_config.next_crawl_time else None,
            created_at=new_config.created_at.isoformat(),
            updated_at=new_config.updated_at.isoformat()
        )
    except Exception as e:
        log_error(f"添加考研爬虫配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "添加考研爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.put("/kaoyan/config/{config_id}", response_model=KaoyanCrawlerConfigResponse, summary="更新考研爬虫配置")
async def update_kaoyan_crawler_config(
    config_id: int,
    req: CrawlerConfigRequest,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """更新考研爬虫配置"""
    try:
        config = db.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 检查URL是否已被其他配置使用
        if req.url != config.url:
            existing_config = db.query(KaoyanCrawlerConfig).filter(
                KaoyanCrawlerConfig.url == req.url,
                KaoyanCrawlerConfig.id != config_id
            ).first()
            
            if existing_config:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "该URL已被其他配置使用",
                        "data": None
                    }
                )
        
        # 更新配置
        config.name = req.name
        config.url = req.url
        config.selector = req.selector
        config.parse_rules = req.parse_rules
        config.interval = req.interval
        config.status = req.status
        config.priority = req.priority
        
        db.commit()
        db.refresh(config)
        
        log_system_event("update_kaoyan_crawler", f"更新考研爬虫配置: {config.name}")
        
        return KaoyanCrawlerConfigResponse(
            id=config.id,
            name=config.name,
            url=config.url,
            selector=config.selector,
            parse_rules=config.parse_rules,
            interval=config.interval,
            status=config.status,
            status_text=config.status_text,
            priority=config.priority,
            priority_text=config.priority_text,
            last_crawl_time=config.last_crawl_time.isoformat() if config.last_crawl_time else None,
            next_crawl_time=config.next_crawl_time.isoformat() if config.next_crawl_time else None,
            created_at=config.created_at.isoformat(),
            updated_at=config.updated_at.isoformat()
        )
    except Exception as e:
        log_error(f"更新考研爬虫配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "更新考研爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/kaoyan/config/{config_id}", summary="删除考研爬虫配置")
async def delete_kaoyan_crawler_config(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """删除考研爬虫配置"""
    try:
        config = db.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            from fastapi import status
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        config_name = config.name
        db.delete(config)
        db.commit()
        

        
        log_system_event("delete_kaoyan_crawler", f"删除考研爬虫配置: {config_name}")
        
        from fastapi import status
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "删除考研爬虫配置成功",
                "data": None
            }
        )
    except Exception as e:
        db.rollback()
        log_error(f"删除考研爬虫配置失败: {str(e)}")
        from fastapi import status
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "删除考研爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.get("/kaoyan/logs", response_model=List[CrawlerLogResponse], summary="获取考研爬虫日志")
async def get_kaoyan_crawler_logs(
    config_id: Optional[int] = Query(None, description="配置ID"),
    status: Optional[int] = Query(None, ge=0, le=1, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """获取考研爬虫日志"""
    try:
        query = db.query(KaoyanCrawlerLog)
        
        if config_id:
            query = query.filter(KaoyanCrawlerLog.config_id == config_id)
        if status is not None:
            query = query.filter(KaoyanCrawlerLog.status == status)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        logs = query.order_by(KaoyanCrawlerLog.crawl_time.desc()).offset(offset).limit(page_size).all()
        
        items = []
        for log in logs:
            items.append(CrawlerLogResponse(
                id=log.id,
                config_id=log.config_id,
                url=log.url,
                status=log.status,
                status_text=log.status_text,
                info_count=log.info_count,
                error_msg=log.error_msg,
                crawl_time=log.crawl_time.isoformat()
            ))
        
        return items
    except Exception as e:
        log_error(f"获取考研爬虫日志失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考研爬虫日志失败"
        )

@router.get("/kaogong/config", response_model=List[KaogongCrawlerConfigResponse], summary="获取考公爬虫配置列表")
async def get_kaogong_crawler_configs(
    status: Optional[int] = Query(None, ge=0, le=1, description="状态"),
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """获取考公爬虫配置列表"""
    try:
        query = db.query(KaogongCrawlerConfig)
        
        if status is not None:
            query = query.filter(KaogongCrawlerConfig.status == status)
        
        configs = query.order_by(KaogongCrawlerConfig.priority.desc(), KaogongCrawlerConfig.id).all()
        
        items = []
        for config in configs:
            # 处理parse_rules类型转换
            parse_rules = config.parse_rules
            if isinstance(parse_rules, str):
                import json
                try:
                    parse_rules = json.loads(parse_rules)
                except:
                    parse_rules = None
            
            items.append(KaogongCrawlerConfigResponse(
                id=config.id,
                name=config.name,
                url=config.url,
                selector=config.selector,
                parse_rules=parse_rules,
                interval=config.interval,
                status=config.status,
                status_text=config.status_text,
                priority=config.priority,
                priority_text=config.priority_text,
                last_crawl_time=config.last_crawl_time.isoformat() if config.last_crawl_time else None,
                next_crawl_time=config.next_crawl_time.isoformat() if config.next_crawl_time else None,
                created_at=config.created_at.isoformat(),
                updated_at=config.updated_at.isoformat()
            ))
        
        return items
    except Exception as e:
        log_error(f"获取考公爬虫配置列表失败: {str(e)}")
        from fastapi import status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考公爬虫配置列表失败"
        )

@router.post("/kaogong/config", response_model=KaogongCrawlerConfigResponse, summary="添加考公爬虫配置")
async def add_kaogong_crawler_config(
    req: CrawlerConfigRequest,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """添加考公爬虫配置"""
    try:
        # 检查URL是否已存在
        existing_config = db.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.url == req.url
        ).first()
        
        if existing_config:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该URL已存在",
                    "data": None
                }
            )
        
        # 创建新配置
        new_config = KaogongCrawlerConfig(
            name=req.name,
            url=req.url,
            selector=req.selector,
            parse_rules=req.parse_rules,
            interval=req.interval,
            status=req.status,
            priority=req.priority
        )
        
        db.add(new_config)
        db.commit()
        db.refresh(new_config)
        
        log_system_event("add_kaogong_crawler", f"添加考公爬虫配置: {req.name}")
        
        return KaogongCrawlerConfigResponse(
            id=new_config.id,
            name=new_config.name,
            url=new_config.url,
            selector=new_config.selector,
            parse_rules=new_config.parse_rules,
            interval=new_config.interval,
            status=new_config.status,
            status_text=new_config.status_text,
            priority=new_config.priority,
            priority_text=new_config.priority_text,
            last_crawl_time=new_config.last_crawl_time.isoformat() if new_config.last_crawl_time else None,
            next_crawl_time=new_config.next_crawl_time.isoformat() if new_config.next_crawl_time else None,
            created_at=new_config.created_at.isoformat(),
            updated_at=new_config.updated_at.isoformat()
        )
    except Exception as e:
        log_error(f"添加考公爬虫配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "添加考公爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.put("/kaogong/config/{config_id}", response_model=KaogongCrawlerConfigResponse, summary="更新考公爬虫配置")
async def update_kaogong_crawler_config(
    config_id: int,
    req: CrawlerConfigRequest,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """更新考公爬虫配置"""
    try:
        config = db.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 检查URL是否已被其他配置使用
        if req.url != config.url:
            existing_config = db.query(KaogongCrawlerConfig).filter(
                KaogongCrawlerConfig.url == req.url,
                KaogongCrawlerConfig.id != config_id
            ).first()
            
            if existing_config:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "该URL已被其他配置使用",
                        "data": None
                    }
                )
        
        # 更新配置
        config.name = req.name
        config.url = req.url
        config.selector = req.selector
        config.parse_rules = req.parse_rules
        config.interval = req.interval
        config.status = req.status
        config.priority = req.priority
        
        db.commit()
        db.refresh(config)
        
        log_system_event("update_kaogong_crawler", f"更新考公爬虫配置: {config.name}")
        
        return KaogongCrawlerConfigResponse(
            id=config.id,
            name=config.name,
            url=config.url,
            selector=config.selector,
            parse_rules=config.parse_rules,
            interval=config.interval,
            status=config.status,
            status_text=config.status_text,
            priority=config.priority,
            priority_text=config.priority_text,
            last_crawl_time=config.last_crawl_time.isoformat() if config.last_crawl_time else None,
            next_crawl_time=config.next_crawl_time.isoformat() if config.next_crawl_time else None,
            created_at=config.created_at.isoformat(),
            updated_at=config.updated_at.isoformat()
        )
    except Exception as e:
        log_error(f"更新考公爬虫配置失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "更新考公爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.delete("/kaogong/config/{config_id}", summary="删除考公爬虫配置")
async def delete_kaogong_crawler_config(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """删除考公爬虫配置"""
    try:
        config = db.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            from fastapi import status
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        config_name = config.name
        db.delete(config)
        db.commit()
        

        
        log_system_event("delete_kaogong_crawler", f"删除考公爬虫配置: {config_name}")
        
        from fastapi import status
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "删除考公爬虫配置成功",
                "data": None
            }
        )
    except Exception as e:
        db.rollback()
        log_error(f"删除考公爬虫配置失败: {str(e)}")
        from fastapi import status
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "删除考公爬虫配置失败，请稍后重试",
                "data": None
            }
        )

@router.get("/kaogong/logs", response_model=List[CrawlerLogResponse], summary="获取考公爬虫日志")
async def get_kaogong_crawler_logs(
    config_id: Optional[int] = Query(None, description="配置ID"),
    status: Optional[int] = Query(None, ge=0, le=1, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """获取考公爬虫日志"""
    try:
        query = db.query(KaogongCrawlerLog)
        
        if config_id:
            query = query.filter(KaogongCrawlerLog.config_id == config_id)
        if status is not None:
            query = query.filter(KaogongCrawlerLog.status == status)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        logs = query.order_by(KaogongCrawlerLog.crawl_time.desc()).offset(offset).limit(page_size).all()
        
        items = []
        for log in logs:
            items.append(CrawlerLogResponse(
                id=log.id,
                config_id=log.config_id,
                url=log.url,
                status=log.status,
                status_text=log.status_text,
                info_count=log.info_count,
                error_msg=log.error_msg,
                crawl_time=log.crawl_time.isoformat()
            ))
        
        return items
    except Exception as e:
        log_error(f"获取考公爬虫日志失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取考公爬虫日志失败"
        )

@router.post("/kaoyan/start/{config_id}", summary="启动考研爬虫")
async def start_kaoyan_crawler(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """启动考研爬虫"""
    try:
        config = db.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 更新状态为启用
        config.status = 1
        db.commit()
        
        log_system_event("start_kaoyan_crawler", f"启动考研爬虫: {config.name}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "启动考研爬虫成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"启动考研爬虫失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "启动考研爬虫失败，请稍后重试",
                "data": None
            }
        )

@router.post("/kaoyan/stop/{config_id}", summary="停止考研爬虫")
async def stop_kaoyan_crawler(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaoyan)
):
    """停止考研爬虫"""
    try:
        config = db.query(KaoyanCrawlerConfig).filter(
            KaoyanCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 更新状态为禁用
        config.status = 0
        db.commit()
        
        log_system_event("stop_kaoyan_crawler", f"停止考研爬虫: {config.name}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "停止考研爬虫成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"停止考研爬虫失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "停止考研爬虫失败，请稍后重试",
                "data": None
            }
        )

@router.post("/kaogong/start/{config_id}", summary="启动考公爬虫")
async def start_kaogong_crawler(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """启动考公爬虫"""
    try:
        config = db.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 更新状态为启用
        config.status = 1
        db.commit()
        
        log_system_event("start_kaogong_crawler", f"启动考公爬虫: {config.name}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "启动考公爬虫成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"启动考公爬虫失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "启动考公爬虫失败，请稍后重试",
                "data": None
            }
        )

@router.post("/kaogong/stop/{config_id}", summary="停止考公爬虫")
async def stop_kaogong_crawler(
    config_id: int,
    current_admin: Session = Depends(get_current_active_admin),
    db: Session = Depends(get_db_kaogong)
):
    """停止考公爬虫"""
    try:
        config = db.query(KaogongCrawlerConfig).filter(
            KaogongCrawlerConfig.id == config_id
        ).first()
        
        if not config:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "code": 404,
                    "message": "配置不存在",
                    "data": None
                }
            )
        
        # 更新状态为禁用
        config.status = 0
        db.commit()
        
        log_system_event("stop_kaogong_crawler", f"停止考公爬虫: {config.name}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "code": 200,
                "message": "停止考公爬虫成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"停止考公爬虫失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "code": 500,
                "message": "停止考公爬虫失败，请稍后重试",
                "data": None
            }
        )