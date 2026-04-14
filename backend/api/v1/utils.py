from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db_common
from core.models.school import School
from core.crawler_manager import SmartDemandAnalyzer
import asyncio
from datetime import datetime

router = APIRouter()

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

@router.post("/analyze-demand")
async def analyze_demand(
    category: str,
    provinces: list = [],
    schools: list = [],
    majors: str = "",
    types: list = [],
    keywords: str = ""
):
    """
    分析用户需求并生成爬虫配置
    根据用户填写的表单信息，通过AI分析生成匹配的网站结果，并为用户创建爬虫配置
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
        
        demand_text = f"{category} {' '.join(demand_parts)}"
        
        # 调用AI分析需求
        demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, {})
        
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
                    'name': f"AI增强-{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{clean_school}-研究生招生网",
                    'url': url,
                    'selector': '.news-list li, .article-list li, .list-item, .news-item',
                    'interval': 60,
                    'priority': 3,
                    'status': 1,
                    'ai_enhanced': True,
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
                'name': f"AI增强-{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{province}-教育考试院",
                'url': f'https://www.{province}jyksy.cn/',
                'selector': '.news-list li, .article-list li, .list-item, .news-item',
                'interval': 45,
                'priority': 2,
                'status': 1,
                'ai_enhanced': True,
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
                    'name': f"AI增强-{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                    'url': link['url'],
                    'selector': '.news-list li',
                    'interval': 30,
                    'priority': 2,
                    'status': 1,
                    'ai_enhanced': True,
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
                    'name': f"AI增强-{category}-{datetime.now().strftime('%Y%m%d%H%M')}-{link['title']}",
                    'url': link['url'],
                    'selector': '.news-list li',
                    'interval': 30,
                    'priority': 2,
                    'status': 1,
                    'ai_enhanced': True,
                    'match_score': link['relevance'],
                    'personalized': False
                })
        
        # 按相关性排序
        relevant_links.sort(key=lambda x: x['relevance'], reverse=True)
        
        # 限制返回数量
        relevant_links = relevant_links[:10]
        
        # 清理旧的爬虫配置
        from core.crawler_manager import clear_all_crawler_configs
        clear_all_crawler_configs()
        
        # 添加新的爬虫配置到数据库
        from core.crawler_manager import _add_crawler_config_to_db
        for config in crawler_configs:
            _add_crawler_config_to_db(config)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "需求分析成功，已生成爬虫配置",
                "data": {
                    "links": relevant_links,
                    "demand_analysis": demand_analysis,
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