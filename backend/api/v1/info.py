from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import desc

from core.database import get_db_kaoyan, get_db_kaogong, get_db_common
from core.security import get_current_user
from models.kaoyan import KaoyanInfo
from models.kaogong import KaogongInfo
from models.users import User
from schemas.kaoyan import KaoyanInfoResponse
from schemas.kaogong import KaogongInfoResponse

router = APIRouter(tags=["info"])


@router.get("/list", response_model=dict)
async def get_info_list(
    time: Optional[str] = Query(None, description="时间范围: week, month, quarter"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_user: User = Depends(get_current_user)
):
    """获取情报列表（根据用户类型）"""
    try:
        all_info = []
        
        # 计算时间范围
        now = datetime.now()
        if time == "week":
            start_time = now - timedelta(days=7)
        elif time == "month":
            start_time = now - timedelta(days=30)
        elif time == "quarter":
            start_time = now - timedelta(days=90)
        else:
            start_time = None
        
        # 根据用户类型获取情报
        # 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        vip_type = current_user.vip_type
        
        # 获取考研情报
        if vip_type in [1, 3]:
            kaoyan_query = db_kaoyan.query(KaoyanInfo)
            if start_time:
                kaoyan_query = kaoyan_query.filter(KaoyanInfo.publish_time >= start_time)
            if search:
                kaoyan_query = kaoyan_query.filter(KaoyanInfo.title.contains(search) | KaoyanInfo.content.contains(search))
            kaoyan_info = kaoyan_query.order_by(KaoyanInfo.publish_time.desc()).all()
            
            for info in kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "content": info.content,
                    "type": "考研",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取考公情报
        if vip_type in [2, 3]:
            kaogong_query = db_kaogong.query(KaogongInfo)
            if start_time:
                kaogong_query = kaogong_query.filter(KaogongInfo.publish_time >= start_time)
            if search:
                kaogong_query = kaogong_query.filter(KaogongInfo.title.contains(search) | KaogongInfo.content.contains(search))
            kaogong_info = kaogong_query.order_by(KaogongInfo.publish_time.desc()).all()
            
            for info in kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "content": info.content,
                    "type": "考公",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 按时间排序
        all_info.sort(key=lambda x: x["time"], reverse=True)
        
        # 计算总数
        total = len(all_info)
        
        # 分页
        offset = (page - 1) * page_size
        paginated_info = all_info[offset:offset + page_size]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取情报列表成功",
                "data": {
                    "total": total,
                    "items": paginated_info
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取情报列表失败"
        )


@router.get("/related/{info_id}", response_model=dict)
async def get_related_info(
    info_id: int = Path(..., description="情报ID"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_user: dict = Depends(get_current_user)
):
    """获取相关情报"""
    try:
        # 这里可以实现相关情报的逻辑
        # 暂时返回空列表
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取相关情报成功",
                "data": []
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取相关情报失败"
        )


@router.get("/latest", response_model=dict)
async def get_latest_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_user: User = Depends(get_current_user)
):
    """获取最新情报（根据用户类型）"""
    try:
        all_info = []
        
        # 根据用户类型获取情报
        # 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        vip_type = current_user.vip_type
        
        # 获取当天的开始和结束时间
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 获取考研情报
        if vip_type in [1, 3]:
            kaoyan_info = db_kaoyan.query(KaoyanInfo).filter(
                KaoyanInfo.is_valid == True,
                KaoyanInfo.publish_time >= today_start,
                KaoyanInfo.publish_time <= today_end
            ).order_by(
                desc(KaoyanInfo.publish_time)
            ).limit(limit // 2 if vip_type == 3 else limit).all()
            
            for info in kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考研",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取考公情报
        if vip_type in [2, 3]:
            kaogong_info = db_kaogong.query(KaogongInfo).filter(
                KaogongInfo.is_valid == True,
                KaogongInfo.publish_time >= today_start,
                KaogongInfo.publish_time <= today_end
            ).order_by(
                desc(KaogongInfo.publish_time)
            ).limit(limit // 2 if vip_type == 3 else limit).all()
            
            for info in kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考公",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 按时间排序
        all_info.sort(key=lambda x: x["time"], reverse=True)
        
        # 限制数量
        all_info = all_info[:limit]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取最新情报成功",
                "data": all_info
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取最新情报失败"
        )


@router.get("/hot", response_model=dict)
async def get_history_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_user: User = Depends(get_current_user)
):
    """获取历史情报（根据用户类型）"""
    try:
        all_info = []
        
        # 获取昨天及之前的开始时间
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 根据用户类型获取情报
        # 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        vip_type = current_user.vip_type
        
        # 获取历史考研情报
        if vip_type in [1, 3]:
            kaoyan_info = db_kaoyan.query(KaoyanInfo).filter(
                KaoyanInfo.is_valid == True,
                KaoyanInfo.publish_time < today_start
            ).order_by(
                desc(KaoyanInfo.publish_time)
            ).limit(limit // 2 if vip_type == 3 else limit).all()
            
            for info in kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考研",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取历史考公情报
        if vip_type in [2, 3]:
            kaogong_info = db_kaogong.query(KaogongInfo).filter(
                KaogongInfo.is_valid == True,
                KaogongInfo.publish_time < today_start
            ).order_by(
                desc(KaogongInfo.publish_time)
            ).limit(limit // 2 if vip_type == 3 else limit).all()
            
            for info in kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考公",
                    "time": info.publish_time.isoformat(),
                    "source": info.source,
                    "url": info.url
                })
        
        # 按时间排序
        all_info.sort(key=lambda x: x["time"], reverse=True)
        
        # 限制数量
        all_info = all_info[:limit]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取历史情报成功",
                "data": all_info
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取历史情报失败"
        )
