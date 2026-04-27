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
from models.users import User, UserSubscription, UserKeyword
from schemas.kaoyan import KaoyanInfoResponse
from schemas.kaogong import KaogongInfoResponse

router = APIRouter(tags=["info"])


@router.get("/public/latest", response_model=dict)
async def get_public_latest_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong)
):
    """获取最新情报（公开接口，不需要登录，按上传时间排序）"""
    try:
        all_info = []

        kaoyan_infos = db_kaoyan.query(KaoyanInfo).filter(
            KaoyanInfo.is_valid == True
        ).order_by(desc(KaoyanInfo.created_at)).limit(limit).all()

        for info in kaoyan_infos:
            all_info.append({
                "id": info.id,
                "title": info.title,
                "type": "考研",
                "time": info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "source": info.source,
                "url": info.url,
                "province": info.province,
                "school": info.school,
                "major": info.major,
                "like_count": info.like_count or 0,
                "favorite_count": info.favorite_count or 0
            })

        kaogong_infos = db_kaogong.query(KaogongInfo).filter(
            KaogongInfo.is_valid == True
        ).order_by(desc(KaogongInfo.created_at)).limit(limit).all()

        for info in kaogong_infos:
            all_info.append({
                "id": info.id,
                "title": info.title,
                "type": "考公",
                "time": info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "source": info.source,
                "url": info.url,
                "province": info.province,
                "position_type": info.position_type,
                "major": info.major,
                "like_count": info.like_count or 0,
                "favorite_count": info.favorite_count or 0
            })

        all_info.sort(key=lambda x: x["time"], reverse=True)
        all_info = all_info[:limit]

        # 计算今日情报数量
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        # 计算今日考研情报数量
        today_kaoyan_count = db_kaoyan.query(KaoyanInfo).filter(
            KaoyanInfo.is_valid == True,
            KaoyanInfo.created_at >= today,
            KaoyanInfo.created_at < tomorrow
        ).count()
        
        # 计算今日考公情报数量
        today_kaogong_count = db_kaogong.query(KaogongInfo).filter(
            KaogongInfo.is_valid == True,
            KaogongInfo.created_at >= today,
            KaogongInfo.created_at < tomorrow
        ).count()
        
        today_count = today_kaoyan_count + today_kaogong_count

        kaoyan_total = db_kaoyan.query(KaoyanInfo).filter(KaoyanInfo.is_valid == True).count()
        kaogong_total = db_kaogong.query(KaogongInfo).filter(KaogongInfo.is_valid == True).count()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取公开情报成功",
                "data": {
                    "items": all_info,
                    "kaoyan_total": kaoyan_total,
                    "kaogong_total": kaogong_total,
                    "today_count": today_count
                }
            }
        )
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"获取公开情报失败: {error_msg}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": "获取公开情报失败"
            }
        )


@router.get("/public/hot", response_model=dict)
async def get_public_hot_info(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong)
):
    """获取热门情报（公开接口，不需要登录，按收藏数排序前10条）"""
    try:
        all_info = []

        kaoyan_infos = db_kaoyan.query(KaoyanInfo).filter(
            KaoyanInfo.is_valid == True
        ).order_by(desc(KaoyanInfo.favorite_count), desc(KaoyanInfo.created_at)).limit(limit).all()

        for info in kaoyan_infos:
            all_info.append({
                "id": info.id,
                "title": info.title,
                "type": "考研",
                "time": info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "source": info.source,
                "url": info.url,
                "province": info.province,
                "school": info.school,
                "major": info.major,
                "like_count": info.like_count or 0,
                "favorite_count": info.favorite_count or 0
            })

        kaogong_infos = db_kaogong.query(KaogongInfo).filter(
            KaogongInfo.is_valid == True
        ).order_by(desc(KaogongInfo.favorite_count), desc(KaogongInfo.created_at)).limit(limit).all()

        for info in kaogong_infos:
            all_info.append({
                "id": info.id,
                "title": info.title,
                "type": "考公",
                "time": info.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "source": info.source,
                "url": info.url,
                "province": info.province,
                "position_type": info.position_type,
                "major": info.major,
                "like_count": info.like_count or 0,
                "favorite_count": info.favorite_count or 0
            })

        all_info.sort(key=lambda x: (x["favorite_count"], x["time"]), reverse=True)
        all_info = all_info[:10]

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取热门情报成功",
                "data": all_info
            }
        )
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"获取热门情报失败: {error_msg}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": "获取热门情报失败"
            }
        )


@router.get("/list", response_model=dict)
async def get_info_list(
    time: Optional[str] = Query(None, description="时间范围: week, month, quarter"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    db_common: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取情报列表（根据用户需求）"""
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
        
        # 获取用户的订阅配置
        subscription = db_common.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        # 获取用户的关键词
        kaoyan_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 1,
            UserKeyword.is_active == True
        ).all()]
        
        kaogong_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 2,
            UserKeyword.is_active == True
        ).all()]
        
        # 从订阅配置中获取用户关注的省份、学校、专业等
        config_json = subscription.config_json if subscription and subscription.config_json else {}
        kaoyan_config = config_json.get('kaoyan') or {}
        kaoyan_provinces = kaoyan_config.get('provinces', [])
        kaoyan_schools = kaoyan_config.get('schools', [])
        if isinstance(kaoyan_schools, str):
            kaoyan_schools = [kaoyan_schools]
        kaoyan_majors = kaoyan_config.get('majors', [])
        if isinstance(kaoyan_majors, str):
            kaoyan_majors = [kaoyan_majors]
        
        kaogong_config = config_json.get('kaogong') or {}
        kaogong_provinces = kaogong_config.get('provinces', [])
        kaogong_position_types = kaogong_config.get('position_types', [])
        kaogong_majors = kaogong_config.get('majors', [])
        if isinstance(kaogong_majors, str):
            kaogong_majors = [kaogong_majors]
        
        # 获取考研情报
        if vip_type in [1, 3]:
            # 获取所有考研情报
            kaoyan_query = db_kaoyan.query(KaoyanInfo)
            if start_time:
                kaoyan_query = kaoyan_query.filter(KaoyanInfo.publish_time >= start_time)
            if search:
                kaoyan_query = kaoyan_query.filter(KaoyanInfo.title.contains(search) | KaoyanInfo.content.contains(search))
            
            # 筛选符合用户需求的情报
            relevant_kaoyan_info = []
            for info in kaoyan_query.all():
                # 检查省份
                if kaoyan_provinces and info.province and info.province not in kaoyan_provinces:
                    continue
                # 检查学校
                if kaoyan_schools and info.school and info.school not in kaoyan_schools:
                    continue
                # 检查专业
                if kaoyan_majors and info.major and info.major not in kaoyan_majors:
                    continue
                # 检查关键词
                if kaoyan_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaoyan_keywords):
                        continue
                relevant_kaoyan_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaoyan_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            for info in relevant_kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "content": info.content,
                    "type": "考研",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取考公情报
        if vip_type in [2, 3]:
            # 获取所有考公情报
            kaogong_query = db_kaogong.query(KaogongInfo)
            if start_time:
                kaogong_query = kaogong_query.filter(KaogongInfo.publish_time >= start_time)
            if search:
                kaogong_query = kaogong_query.filter(KaogongInfo.title.contains(search) | KaogongInfo.content.contains(search))
            
            # 筛选符合用户需求的情报
            relevant_kaogong_info = []
            for info in kaogong_query.all():
                # 检查省份
                if kaogong_provinces and info.province and info.province not in kaogong_provinces:
                    continue
                # 检查岗位类别
                if kaogong_position_types and info.position_type and info.position_type not in kaogong_position_types:
                    continue
                # 检查专业
                if kaogong_majors and info.major and info.major not in kaogong_majors:
                    continue
                # 检查关键词
                if kaogong_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaogong_keywords):
                        continue
                relevant_kaogong_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaogong_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            for info in relevant_kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "content": info.content,
                    "type": "考公",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
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
    db_common: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取最新情报（根据用户需求）"""
    try:
        all_info = []
        
        # 根据用户类型获取情报
        # 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        vip_type = current_user.vip_type
        
        # 获取当天的开始和结束时间
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 获取用户的订阅配置
        subscription = db_common.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        # 获取用户的关键词
        kaoyan_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 1,
            UserKeyword.is_active == True
        ).all()]
        
        kaogong_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 2,
            UserKeyword.is_active == True
        ).all()]
        
        # 从订阅配置中获取用户关注的省份、学校、专业等
        config_json = subscription.config_json if subscription else {}
        kaoyan_config = config_json.get('kaoyan', {})
        kaoyan_provinces = kaoyan_config.get('provinces', [])
        kaoyan_schools = kaoyan_config.get('schools', [])
        if isinstance(kaoyan_schools, str):
            kaoyan_schools = [kaoyan_schools]
        kaoyan_majors = kaoyan_config.get('majors', [])
        if isinstance(kaoyan_majors, str):
            kaoyan_majors = [kaoyan_majors]
        
        kaogong_config = config_json.get('kaogong') or {}
        kaogong_provinces = kaogong_config.get('provinces', [])
        kaogong_position_types = kaogong_config.get('position_types', [])
        kaogong_majors = kaogong_config.get('majors', [])
        if isinstance(kaogong_majors, str):
            kaogong_majors = [kaogong_majors]
        
        # 获取考研情报
        if vip_type in [1, 3]:
            # 获取所有当天考研情报
            kaoyan_query = db_kaoyan.query(KaoyanInfo).filter(
                KaoyanInfo.is_valid == True,
                KaoyanInfo.publish_time >= today_start,
                KaoyanInfo.publish_time <= today_end
            )
            
            # 筛选符合用户需求的情报
            relevant_kaoyan_info = []
            for info in kaoyan_query.all():
                # 检查省份
                if kaoyan_provinces and info.province and info.province not in kaoyan_provinces:
                    continue
                # 检查学校
                if kaoyan_schools and info.school and info.school not in kaoyan_schools:
                    continue
                # 检查专业
                if kaoyan_majors and info.major and info.major not in kaoyan_majors:
                    continue
                # 检查关键词
                if kaoyan_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaoyan_keywords):
                        continue
                relevant_kaoyan_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaoyan_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            # 限制数量
            relevant_kaoyan_info = relevant_kaoyan_info[:limit // 2 if vip_type == 3 else limit]
            
            for info in relevant_kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考研",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取考公情报
        if vip_type in [2, 3]:
            # 获取所有当天考公情报
            kaogong_query = db_kaogong.query(KaogongInfo).filter(
                KaogongInfo.is_valid == True,
                KaogongInfo.publish_time >= today_start,
                KaogongInfo.publish_time <= today_end
            )
            
            # 筛选符合用户需求的情报
            relevant_kaogong_info = []
            for info in kaogong_query.all():
                # 检查省份
                if kaogong_provinces and info.province and info.province not in kaogong_provinces:
                    continue
                # 检查岗位类别
                if kaogong_position_types and info.position_type and info.position_type not in kaogong_position_types:
                    continue
                # 检查专业
                if kaogong_majors and info.major and info.major not in kaogong_majors:
                    continue
                # 检查关键词
                if kaogong_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaogong_keywords):
                        continue
                relevant_kaogong_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaogong_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            # 限制数量
            relevant_kaogong_info = relevant_kaogong_info[:limit // 2 if vip_type == 3 else limit]
            
            for info in relevant_kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考公",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
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
    db_common: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取历史情报（根据用户需求）"""
    try:
        all_info = []
        
        # 获取昨天及之前的开始时间
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 根据用户类型获取情报
        # 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        vip_type = current_user.vip_type
        
        # 获取用户的订阅配置
        subscription = db_common.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        
        # 获取用户的关键词
        kaoyan_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 1,
            UserKeyword.is_active == True
        ).all()]
        
        kaogong_keywords = [kw.keyword for kw in db_common.query(UserKeyword).filter(
            UserKeyword.user_id == current_user.id,
            UserKeyword.category == 2,
            UserKeyword.is_active == True
        ).all()]
        
        # 从订阅配置中获取用户关注的省份、学校、专业等
        config_json = subscription.config_json if subscription else {}
        kaoyan_config = config_json.get('kaoyan', {})
        kaoyan_provinces = kaoyan_config.get('provinces', [])
        kaoyan_schools = kaoyan_config.get('schools', [])
        if isinstance(kaoyan_schools, str):
            kaoyan_schools = [kaoyan_schools]
        kaoyan_majors = kaoyan_config.get('majors', [])
        if isinstance(kaoyan_majors, str):
            kaoyan_majors = [kaoyan_majors]
        
        kaogong_config = config_json.get('kaogong') or {}
        kaogong_provinces = kaogong_config.get('provinces', [])
        kaogong_position_types = kaogong_config.get('position_types', [])
        kaogong_majors = kaogong_config.get('majors', [])
        if isinstance(kaogong_majors, str):
            kaogong_majors = [kaogong_majors]
        
        # 获取历史考研情报
        if vip_type in [1, 3]:
            # 获取所有历史考研情报
            kaoyan_query = db_kaoyan.query(KaoyanInfo).filter(
                KaoyanInfo.is_valid == True,
                KaoyanInfo.publish_time < today_start
            )
            
            # 筛选符合用户需求的情报
            relevant_kaoyan_info = []
            for info in kaoyan_query.all():
                # 检查省份
                if kaoyan_provinces and info.province and info.province not in kaoyan_provinces:
                    continue
                # 检查学校
                if kaoyan_schools and info.school and info.school not in kaoyan_schools:
                    continue
                # 检查专业
                if kaoyan_majors and info.major and info.major not in kaoyan_majors:
                    continue
                # 检查关键词
                if kaoyan_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaoyan_keywords):
                        continue
                relevant_kaoyan_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaoyan_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            # 限制数量
            relevant_kaoyan_info = relevant_kaoyan_info[:limit // 2 if vip_type == 3 else limit]
            
            for info in relevant_kaoyan_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考研",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "source": info.source,
                    "url": info.url
                })
        
        # 获取历史考公情报
        if vip_type in [2, 3]:
            # 获取所有历史考公情报
            kaogong_query = db_kaogong.query(KaogongInfo).filter(
                KaogongInfo.is_valid == True,
                KaogongInfo.publish_time < today_start
            )
            
            # 筛选符合用户需求的情报
            relevant_kaogong_info = []
            for info in kaogong_query.all():
                # 检查省份
                if kaogong_provinces and info.province and info.province not in kaogong_provinces:
                    continue
                # 检查岗位类别
                if kaogong_position_types and info.position_type and info.position_type not in kaogong_position_types:
                    continue
                # 检查专业
                if kaogong_majors and info.major and info.major not in kaogong_majors:
                    continue
                # 检查关键词
                if kaogong_keywords:
                    info_text = f"{info.title} {info.content or ''}"
                    if not any(keyword in info_text for keyword in kaogong_keywords):
                        continue
                relevant_kaogong_info.append(info)
            
            # 按发布时间倒序排序
            relevant_kaogong_info.sort(key=lambda x: x.publish_time, reverse=True)
            
            # 限制数量
            relevant_kaogong_info = relevant_kaogong_info[:limit // 2 if vip_type == 3 else limit]
            
            for info in relevant_kaogong_info:
                all_info.append({
                    "id": info.id,
                    "title": info.title,
                    "type": "考公",
                    "time": info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
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


@router.get("/detail/{info_id}")
async def get_info_detail(
    info_id: int = Path(..., description="情报ID"),
    db_kaoyan: Session = Depends(get_db_kaoyan),
    db_kaogong: Session = Depends(get_db_kaogong),
    current_user: User = Depends(get_current_user)
):
    """获取情报详情"""
    try:
        # 先从考研库中查找
        kaoyan_info = db_kaoyan.query(KaoyanInfo).filter(KaoyanInfo.id == info_id).first()
        if kaoyan_info:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "code": 200,
                    "message": "获取情报详情成功",
                    "data": {
                        "id": kaoyan_info.id,
                        "title": kaoyan_info.title,
                        "content": kaoyan_info.content,
                        "type": "考研",
                        "time": kaoyan_info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "source": kaoyan_info.source,
                        "url": kaoyan_info.url,
                        "province": kaoyan_info.province,
                        "school": kaoyan_info.school,
                        "major": kaoyan_info.major
                    }
                }
            )
        
        # 再从考公库中查找
        kaogong_info = db_kaogong.query(KaogongInfo).filter(KaogongInfo.id == info_id).first()
        if kaogong_info:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "code": 200,
                    "message": "获取情报详情成功",
                    "data": {
                        "id": kaogong_info.id,
                        "title": kaogong_info.title,
                        "content": kaogong_info.content,
                        "type": "考公",
                        "time": kaogong_info.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "source": kaogong_info.source,
                        "url": kaogong_info.url,
                        "province": kaogong_info.province,
                        "position_type": kaogong_info.position_type,
                        "major": kaogong_info.major
                    }
                }
            )
        
        # 情报不存在
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "code": 404,
                "message": "情报不存在",
                "data": None
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="获取情报详情失败"
        )
