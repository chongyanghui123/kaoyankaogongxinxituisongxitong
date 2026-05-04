from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db_common, get_db_kaoyan, get_db_kaogong
from core.models.school import School
from core.security import get_current_user, get_current_user_optional
from models.users import User
from models.sign_in import PointsRecord
from typing import List, Optional
from pydantic import BaseModel

import asyncio
from datetime import datetime
import os

router = APIRouter()

class DailyPracticeAnswerRequest(BaseModel):
    practice_id: int
    user_answer: str

@router.get("/schools")
async def get_schools_by_province(
    province: str = Query(..., description="省份名称"),
    db: Session = Depends(get_db_common)
):
    """
    根据省份获取学校列表
    """
    try:
        schools = db.query(School).filter(
            School.province == province
        ).all()
        school_names = [school.name for school in schools]
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学校列表成功",
                "data": school_names
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取学校列表失败: {str(e)}",
                "data": []
            }
        )

@router.get("/provinces")
async def get_provinces(db: Session = Depends(get_db_common)):
    """
    获取所有省份列表
    """
    try:
        provinces = db.query(School.province).distinct().all()
        province_list = [province[0] for province in provinces]
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取省份列表成功",
                "data": province_list
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取省份列表失败: {str(e)}",
                "data": []
            }
        )

@router.get("/all-schools")
async def get_all_schools(db: Session = Depends(get_db_common)):
    """
    获取所有学校列表（包含省份信息）
    """
    try:
        schools = db.query(School).all()
        school_list = [{"name": school.name, "province": school.province} for school in schools]
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学校列表成功",
                "data": school_list
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取学校列表失败: {str(e)}",
                "data": []
            }
        )

@router.get("/exam-countdowns")
async def get_exam_countdowns(db: Session = Depends(get_db_common)):
    """
    获取备考倒计时列表
    """
    from datetime import datetime
    from models.learning_materials import ExamSchedule
    
    try:
        schedules = db.query(ExamSchedule).filter(
            ExamSchedule.exam_date >= datetime.now(),
            ExamSchedule.is_active == True
        ).order_by(ExamSchedule.exam_date).limit(5).all()
        
        countdowns = []
        for schedule in schedules:
            days = (schedule.exam_date - datetime.now()).days
            countdowns.append({
                "id": schedule.id,
                "name": schedule.name,
                "date": schedule.exam_date.strftime("%Y-%m-%d"),
                "days": max(0, days)
            })
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "获取倒计时成功", "data": countdowns}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取倒计时失败: {str(e)}", "data": []}
        )

@router.get("/daily-practice")
async def get_daily_practice(
    category: str = Query("all", description="题目分类: kaoyan(考研), kaogong(考公), all(全部)"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db_common)
):
    """
    获取每日一练
    """
    from datetime import datetime
    from models.learning_materials import DailyPractice
    from sqlalchemy import func
    import json
    
    try:
        today = datetime.now().date()
        
        # 根据分类过滤题目
        query = db.query(DailyPractice).filter(
            DailyPractice.is_active == True
        )
        
        if category == "kaoyan":
            query = query.filter(DailyPractice.category.in_(["考研英语", "考研政治", "考研数学", "【考研英语】", "【考研政治】", "【考研数学】"]))
        elif category == "kaogong":
            query = query.filter(DailyPractice.category.in_(["行测", "申论", "【行测】", "【申论】"]))
        
        practice = query.filter(
            DailyPractice.show_date == today
        ).first()
        
        if not practice:
            practice = query.order_by(func.rand()).first()
        
        if practice:
            # 检查用户是否已经回答过
            from models.learning_materials import DailyPracticeRecord
            has_answered = False
            user_answer = None
            is_correct = None
            
            # 未登录用户不返回答案和解析
            show_answer = False
            show_analysis = False
            
            if current_user:
                existing_record = db.query(DailyPracticeRecord).filter(
                    DailyPracticeRecord.user_id == current_user.id,
                    DailyPracticeRecord.practice_id == practice.id,
                    DailyPracticeRecord.created_at >= datetime(today.year, today.month, today.day)
                ).first()
                
                if existing_record:
                    has_answered = True
                    user_answer = existing_record.user_answer
                    is_correct = existing_record.is_correct
                    show_answer = True
                    show_analysis = True
            
            options = json.loads(practice.options) if isinstance(practice.options, str) else practice.options
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "code": 200,
                    "message": "获取每日一练成功",
                    "data": {
                        "id": practice.id,
                        "type": practice.category,
                        "question": practice.question,
                        "options": options,
                        "answer": practice.answer if show_answer else None,
                        "analysis": practice.analysis if show_analysis else "",
                        "has_answered": has_answered,
                        "user_answer": user_answer,
                        "is_correct": is_correct,
                        "is_logged_in": current_user is not None
                    }
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "暂无每日一练题目", "data": None}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取每日一练失败: {str(e)}", "data": None}
        )

@router.post("/daily-practice/answer")
async def submit_daily_practice_answer(
    answer_data: DailyPracticeAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """
    提交每日一练答案并获取积分奖励
    """
    from datetime import datetime
    from models.learning_materials import DailyPractice, DailyPracticeRecord
    
    try:
        practice_id = answer_data.practice_id
        user_answer = answer_data.user_answer
        
        if practice_id == 0 or not practice_id or not user_answer:
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该题目暂不可答题，请刷新页面重试",
                    "data": None
                }
            )
        
        # 检查题目是否存在
        practice = db.query(DailyPractice).filter(
            DailyPractice.id == practice_id,
            DailyPractice.is_active == True
        ).first()
        
        if not practice:
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "code": 404,
                    "message": "题目不存在",
                    "data": None
                }
            )
        
        # 检查用户是否已经答过该题（今天）
        from models.learning_materials import DailyPracticeRecord
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        existing_record = db.query(DailyPracticeRecord).filter(
            DailyPracticeRecord.user_id == current_user.id,
            DailyPracticeRecord.practice_id == practice_id,
            DailyPracticeRecord.created_at >= today_start
        ).first()
        
        if existing_record:
            # 用户今天已经回答过该题目，返回之前的记录
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "code": 200,
                    "message": "您今天已经回答过该题目了",
                    "data": {
                        "practice_id": practice_id,
                        "user_answer": existing_record.user_answer,
                        "correct_answer": practice.answer,
                        "is_correct": existing_record.is_correct,
                        "score": existing_record.score,
                        "analysis": practice.analysis or "",
                        "total_points": current_user.points or 0,
                        "already_answered": True
                    }
                }
            )
        
        # 判断答案是否正确
        is_correct = user_answer.strip().upper() == practice.answer.strip().upper()
        score = 10 if is_correct else 0
        
        # 检查今日已获得积分
        DAILY_POINTS_LIMIT = 50
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_points_records = db.query(PointsRecord).filter(
            PointsRecord.user_id == current_user.id,
            PointsRecord.type == 2,
            PointsRecord.created_at >= today_start
        ).all()
        today_points = sum(r.points for r in today_points_records if r.points > 0)
        
        # 计算实际获得的积分
        actual_score = 0
        if is_correct:
            remaining_quota = DAILY_POINTS_LIMIT - today_points
            if remaining_quota > 0:
                actual_score = min(10, remaining_quota)
        
        score = actual_score
        
        # 记录答题结果
        record = DailyPracticeRecord(
            user_id=current_user.id,
            practice_id=practice_id,
            user_answer=user_answer,
            is_correct=is_correct,
            score=score
        )
        db.add(record)
        
        # 答对题目奖励积分
        if score > 0:
            current_user.points = (current_user.points or 0) + score
            points_record = PointsRecord(
                user_id=current_user.id,
                points=score,
                balance=current_user.points,
                type=2,
                description=f"每日一练答对获得{score}积分",
                related_id=practice_id
            )
            db.add(points_record)
        
        db.commit()
        db.refresh(current_user)
        
        limit_reached = today_points + score >= DAILY_POINTS_LIMIT
        message = "提交答案成功"
        if is_correct and score == 0:
            message = "回答正确，但今日积分已达上限"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": message,
                "data": {
                    "practice_id": practice_id,
                    "user_answer": user_answer,
                    "correct_answer": practice.answer,
                    "is_correct": is_correct,
                    "score": score,
                    "analysis": practice.analysis or "",
                    "total_points": current_user.points or 0,
                    "daily_points_limit": DAILY_POINTS_LIMIT,
                    "today_points": today_points + score,
                    "limit_reached": limit_reached
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=200,
            content={"success": False, "code": 500, "message": f"提交答案失败: {str(e)}", "data": None}
        )

@router.get("/hot-list")
async def get_hot_list(
    db: Session = Depends(get_db_common)
):
    """
    获取今日热点排行
    """
    from models.learning_materials import HotTopic
    from sqlalchemy import desc
    
    try:
        topics = db.query(HotTopic).filter(
            HotTopic.is_active == True
        ).order_by(desc(HotTopic.sort_order), desc(HotTopic.created_at)).limit(5).all()
        
        hot_list = []
        for topic in topics:
            hot_list.append({
                "id": topic.id,
                "title": topic.title,
                "category": topic.category or "通用",
                "views": topic.views or 0,
                "cover_image": topic.cover_image,
                "link_url": topic.link_url
            })
        
        if not hot_list:
            return JSONResponse(
                status_code=200,
                content={"success": True, "code": 200, "message": "暂无热点数据", "data": []}
            )
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "获取热点成功", "data": hot_list}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取热点失败: {str(e)}", "data": []}
        )

@router.post("/hot-topic/{topic_id}/view")
async def increment_hot_topic_view(
    topic_id: int,
    db: Session = Depends(get_db_common)
):
    """增加热点浏览量"""
    from models.learning_materials import HotTopic
    
    try:
        topic = db.query(HotTopic).filter(HotTopic.id == topic_id).first()
        if not topic:
            return JSONResponse(
                status_code=200,
                content={"success": False, "code": 404, "message": "热点不存在", "data": None}
            )
        
        topic.views = (topic.views or 0) + 1
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "浏览量已更新", "data": {"views": topic.views}}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新浏览量失败: {str(e)}", "data": None}
        )

@router.get("/rank-list")
async def get_rank_list(
    limit: int = Query(5, description="返回数量，默认5，最大20"),
    db: Session = Depends(get_db_common)
):
    """
    获取学习排行榜
    """
    from models.users import User
    from sqlalchemy import desc
    
    def anonymize_username(username: str) -> str:
        """匿名化用户名"""
        if not username:
            return "匿名用户"
        if len(username) <= 2:
            return username[0] + "*"
        return username[0] + "*" * (len(username) - 2) + username[-1]
    
    try:
        limit = min(limit, 20)
        users = db.query(User).filter(
            User.points > 0,
            User.is_admin == False
        ).order_by(desc(User.points)).limit(limit).all()
        
        rank_list = []
        for user in users:
            rank_list.append({
                "user_id": user.id,
                "username": anonymize_username(user.username) if user.username else f"用户***",
                "avatar": user.avatar,
                "points": user.points or 0,
                "is_vip": user.is_vip if hasattr(user, 'is_vip') else False
            })
        
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "获取排行榜成功", "data": rank_list}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取排行榜失败: {str(e)}", "data": []}
        )

@router.post("/analyze-demand")
async def analyze_and_generate_crawler_configs(
    user_id: int,
    category: str,
    provinces: List[str],
    schools: List[str],
    majors: str,
    types: List[str],
    keywords: str = ""
):
    """
    分析用户需求并生成爬虫配置
    根据用户填写的表单信息，生成匹配的网站结果，并为用户创建爬虫配置
    """
    try:
        # 构造需求文本
        demand_parts = []
        if provinces:
            demand_parts.append(f"关注{','.join(provinces)}地区")
        if schools:
            demand_parts.append(f"关注{','.join(schools)}")
        if majors:
            demand_parts.append(f"关注{majors}专业")
        if types:
            demand_parts.append(f"关注{','.join(types)}")
        if keywords:
            demand_parts.append(f"关键词:{keywords}")
        
        # 生成相关链接
        relevant_links = []
        crawler_configs = []
        
        # 学校相关链接和爬虫配置
        for school in schools:
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
                relevant_links.append({
                    'title': f'{clean_school}研究生招生网',
                    'url': url,
                    'relevance': 0.9,
                    'type': 'school'
                })
                
                # 生成爬虫配置
                crawler_configs.append({
                    'name': f"{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{clean_school}-研究生招生网",
                    'url': url,
                    'selector': '.news-list li, .article-list li, .list-item, .news-item',
                    'interval': 60,
                    'priority': 3,
                    'status': 1,
                    'match_score': 0.9,
                    'personalized': True
                })
        
        # 省份相关链接和爬虫配置
        for province in provinces:
            relevant_links.append({
                'title': f'{province}教育考试院',
                'url': f'https://www.{province}jyksy.cn/',
                'relevance': 0.8,
                'type': 'province'
            })
            
            # 生成爬虫配置
            crawler_configs.append({
                'name': f"{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{province}-教育考试院",
                'url': f'https://www.{province}jyksy.cn/',
                'selector': '.news-list li, .article-list li, .list-item, .news-item',
                'interval': 45,
                'priority': 2,
                'status': 1,
                'match_score': 0.8,
                'personalized': True
            })
        
        # 通用链接和爬虫配置
        if category == 'kaoyan':
            general_links = [
                {
                    'title': '研招网-考研政策',
                    'url': 'https://yz.chsi.com.cn/kyzx/',
                    'relevance': 0.9,
                    'type': 'general'
                },
                {
                    'title': '中国教育在线-考研资讯',
                    'url': 'https://kaoyan.eol.cn/',
                    'relevance': 0.8,
                    'type': 'general'
                }
            ]
            relevant_links.extend(general_links)
            
            # 生成通用爬虫配置
            for link in general_links:
                crawler_configs.append({
                    'name': f"{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                    'url': link['url'],
                    'selector': '.news-list li',
                    'interval': 30,
                    'priority': 2,
                    'status': 1,
                    'match_score': link['relevance'],
                    'personalized': False
                })
        elif category == 'kaogong':
            general_links = [
                {
                    'title': '国家公务员局-考试录用',
                    'url': 'http://bm.scs.gov.cn/pp/gkweb/core/web/ui/business/home/gkhome.html',
                    'relevance': 0.9,
                    'type': 'general'
                },
                {
                    'title': '中国人事考试网',
                    'url': 'https://www.cpta.com.cn/',
                    'relevance': 0.8,
                    'type': 'general'
                }
            ]
            relevant_links.extend(general_links)
            
            # 生成通用爬虫配置
            for link in general_links:
                crawler_configs.append({
                    'name': f"{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                    'url': link['url'],
                    'selector': '.news-list li',
                    'interval': 30,
                    'priority': 2,
                    'status': 1,
                    'match_score': link['relevance'],
                    'personalized': False
                })
        
        # 按相关性排序
        relevant_links.sort(key=lambda x: x['relevance'], reverse=True)
        
        # 限制返回数量
        relevant_links = relevant_links[:10]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "需求分析成功，已生成相关链接",
                "data": {
                    "links": relevant_links,
                    "crawler_configs": crawler_configs
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"需求分析失败: {str(e)}",
                "data": {
                    "links": [],
                    "demand_analysis": {},
                    "crawler_configs": []
                }
            }
        )


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    """
    上传文件
    """
    try:
        # 确保上传目录存在
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "carousels")
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成文件名
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"carousel_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)
        
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 生成文件URL
        file_url = f"/uploads/carousels/{file_name}"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "文件上传成功",
                "data": {
                    "file_url": file_url,
                    "file_name": file_name
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"文件上传失败: {str(e)}",
                "data": None
            }
        )