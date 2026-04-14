#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化优化版本：智能个性化爬虫管理器
可以直接替换 crawler_manager.py
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import re
import random
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.database import get_db
from core.crawlers.kaoyan import KaoyanCrawler
from core.crawlers.kaogong import KaogongCrawler
from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog
from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog
from models.users import User, UserSubscription, UserKeyword

logger = logging.getLogger(__name__)

# 全局调度器
crawler_scheduler = AsyncIOScheduler()

# 用户需求缓存
user_requirements_cache = {}

# ============================================================================
# 智能需求理解
# ============================================================================

class SmartDemandAnalyzer:
    """智能需求分析器"""
    
    @staticmethod
    async def analyze_demand(raw_demand: str) -> Dict:
        """分析需求"""
        analysis = {
            'category': 'unknown',
            'provinces': [],
            'schools': [],
            'majors': [],
            'keywords': [],
            'urgency': 0,
            'action': 'monitor'
        }
        
        # 1. 判断考研/考公
        if '考研' in raw_demand or '研究生' in raw_demand:
            analysis['category'] = 'kaoyan'
        elif '考公' in raw_demand or '公务员' in raw_demand:
            analysis['category'] = 'kaogong'
        
        # 2. 提取省份
        provinces = ['北京', '上海', '广东', '浙江', '江苏', '山东', '四川']
        for province in provinces:
            if province in raw_demand:
                analysis['provinces'].append(province)
        
        # 3. 提取学校
        schools = ['北京大学', '清华大学', '复旦大学', '上海交通大学']
        for school in schools:
            if school in raw_demand:
                analysis['schools'].append(school)
        
        # 4. 提取专业
        majors = ['计算机', '软件工程', '人工智能', '电子信息']
        for major in majors:
            if major in raw_demand:
                analysis['majors'].append(major)
        
        # 5. 判断紧急程度
        if '紧急' in raw_demand or '尽快' in raw_demand:
            analysis['urgency'] = 3
        elif '重要' in raw_demand:
            analysis['urgency'] = 2
        
        return analysis

# ============================================================================
# 智能网站匹配
# ============================================================================

class SmartWebsiteMatcher:
    """智能网站匹配器"""
    
    WEBSITE_KNOWLEDGE = {
        'kaoyan': [
            {
                'name': '研招网-考研政策',
                'url': 'https://yz.chsi.com.cn/kyzx/',
                'selector': '.news-list li',
                'interval': 30,
                'priority': 2
            },
            {
                'name': '中国教育在线-考研资讯',
                'url': 'https://kaoyan.eol.cn/',
                'selector': '.news-list li',
                'interval': 60,
                'priority': 1
            }
        ],
        'kaogong': [
            {
                'name': '国家公务员局-考试录用',
                'url': 'http://bm.scs.gov.cn/',
                'selector': '.list-item',
                'interval': 30,
                'priority': 2
            },
            {
                'name': '北京人社局-事业单位招聘',
                'url': 'https://rsj.beijing.gov.cn/ywsite/bjpta/',
                'selector': '.zxxx-list li',
                'interval': 60,
                'priority': 1
            }
        ]
    }
    
    @staticmethod
    def match_websites(demand_analysis: Dict) -> List[Dict]:
        """匹配网站"""
        category = demand_analysis.get('category', 'unknown')
        
        if category not in SmartWebsiteMatcher.WEBSITE_KNOWLEDGE:
            return []
        
        websites = SmartWebsiteMatcher.WEBSITE_KNOWLEDGE[category]
        
        # 根据需求调整配置
        for website in websites:
            # 根据紧急度调整间隔
            urgency = demand_analysis.get('urgency', 0)
            if urgency >= 2:
                website['interval'] = max(5, website['interval'] // 2)
                website['priority'] = min(3, website['priority'] + 1)
        
        return websites

# ============================================================================
# 智能爬虫生成
# ============================================================================

class SmartCrawlerGenerator:
    """智能爬虫生成器"""
    
    @staticmethod
    async def generate_crawler_config(demand_analysis: Dict) -> Dict:
        """生成爬虫配置"""
        # 1. 匹配网站
        websites = SmartWebsiteMatcher.match_websites(demand_analysis)
        
        if not websites:
            return {}
        
        # 2. 生成个性化配置
        config = {
            'name': f"个性化爬虫-{demand_analysis.get('category', 'unknown')}",
            'websites': websites,
            'demand_analysis': demand_analysis,
            'interval': websites[0]['interval'] if websites else 30,
            'priority': websites[0]['priority'] if websites else 1,
            'created_at': datetime.now()
        }
        
        return config

# ============================================================================
# 核心函数（优化版本）
# ============================================================================

async def get_user_requirements():
    """获取所有用户的需求配置"""
    global user_requirements_cache  # 在函数顶部声明global
    
    db = next(get_db(database="common"))
    try:
        # 获取所有用户的订阅配置
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.status == 1
        ).all()
        
        # 如果没有活跃用户，清空缓存
        if not subscriptions:
            user_requirements_cache = {}
            logger.info("没有活跃用户，清空用户需求缓存")
            return
        
        # 构建用户需求缓存
        requirements = {}
        for sub in subscriptions:
            if sub.user_id not in requirements:
                requirements[sub.user_id] = {
                    'kaoyan': {},
                    'kaogong': {}
                }
            
            if sub.config_json:
                if 'kaoyan' in sub.config_json:
                    requirements[sub.user_id]['kaoyan'] = sub.config_json['kaoyan']
                if 'kaogong' in sub.config_json:
                    requirements[sub.user_id]['kaogong'] = sub.config_json['kaogong']
        
        # 获取所有用户的关键词
        keywords = db.query(UserKeyword).filter(
            UserKeyword.is_active == True
        ).all()
        
        for kw in keywords:
            if kw.user_id not in requirements:
                requirements[kw.user_id] = {
                    'kaoyan': {},
                    'kaogong': {}
                }
            
            category = 'kaoyan' if kw.category == 1 else 'kaogong'
            if 'keywords' not in requirements[kw.user_id][category]:
                requirements[kw.user_id][category]['keywords'] = []
            requirements[kw.user_id][category]['keywords'].append(kw.keyword)
        
        user_requirements_cache = requirements
        logger.info(f"更新用户需求缓存，共 {len(requirements)} 个活跃用户")
        
    except Exception as e:
        logger.error(f"获取用户需求失败: {str(e)}")
    finally:
        db.close()

def generate_dynamic_crawler_configs() -> List[Dict[str, Any]]:
    """生成动态爬虫配置（智能版本）"""
    logger.info("生成动态爬虫配置（智能版本）")
    
    # 先检查是否有活跃用户
    active_users = check_active_users()
    if active_users == 0:
        logger.info("没有活跃用户，不生成爬虫配置")
        return []
    
    logger.info(f"检测到 {active_users} 个活跃用户，生成智能爬虫配置")
    
    db = next(get_db(database="common"))
    try:
        # 获取所有用户的订阅配置
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.status == 1
        ).all()
        
        if not subscriptions:
            logger.info("没有用户订阅配置，不生成爬虫配置")
            return []
        
        dynamic_configs = []
        
        for sub in subscriptions:
            if not sub.config_json:
                continue
            
            config_json = sub.config_json
            
            # 处理考研需求
            if 'kaoyan' in config_json:
                kaoyan_config = config_json['kaoyan']
                
                # 智能分析需求
                demand_text = _construct_demand_text(kaoyan_config)
                demand_analysis = asyncio.run(
                    SmartDemandAnalyzer.analyze_demand(demand_text)
                )
                
                # 生成爬虫配置
                crawler_config = asyncio.run(
                    SmartCrawlerGenerator.generate_crawler_config(demand_analysis)
                )
                
                if crawler_config:
                    crawler_config['user_id'] = sub.user_id
                    crawler_config['category'] = 'kaoyan'
                    dynamic_configs.append(crawler_config)
            
            # 处理考公需求
            if 'kaogong' in config_json:
                kaogong_config = config_json['kaogong']
                
                # 智能分析需求
                demand_text = _construct_demand_text(kaogong_config)
                demand_analysis = asyncio.run(
                    SmartDemandAnalyzer.analyze_demand(demand_text)
                )
                
                # 生成爬虫配置
                crawler_config = asyncio.run(
                    SmartCrawlerGenerator.generate_crawler_config(demand_analysis)
                )
                
                if crawler_config:
                    crawler_config['user_id'] = sub.user_id
                    crawler_config['category'] = 'kaogong'
                    dynamic_configs.append(crawler_config)
        
        logger.info(f"根据用户需求生成了 {len(dynamic_configs)} 个智能爬虫配置")
        return dynamic_configs
        
    except Exception as e:
        logger.error(f"生成动态爬虫配置失败: {str(e)}")
        return []
    finally:
        db.close()

def _construct_demand_text(config: Dict) -> str:
    """构造需求文本"""
    parts = []
    
    if 'provinces' in config and config['provinces']:
        parts.append(f"关注{','.join(config['provinces'])}地区")
    
    if 'schools' in config and config['schools']:
        parts.append(f"关注{','.join(config['schools'])}")
    
    if 'majors' in config and config['majors']:
        parts.append(f"关注{','.join(config['majors'])}专业")
    
    if 'keywords' in config and config['keywords']:
        parts.append(f"关键词:{','.join(config['keywords'])}")
    
    return ' '.join(parts) if parts else "关注相关信息"

def check_active_users() -> int:
    """检查活跃用户数量"""
    db = next(get_db(database="common"))
    try:
        active_count = db.query(UserSubscription).filter(
            UserSubscription.status == 1
        ).count()
        return active_count
    except Exception as e:
        logger.error(f"检查活跃用户失败: {str(e)}")
        return 0
    finally:
        db.close()

def clear_all_crawler_configs():
    """清除所有爬虫配置"""
    try:
        # 清除考研爬虫配置
        kaoyan_db = next(get_db(database="kaoyan"))
        kaoyan_db.query(KaoyanCrawlerConfig).delete()
        kaoyan_db.commit()
        kaoyan_db.close()
        
        # 清除考公爬虫配置
        kaogong_db = next(get_db(database="kaogong"))
        kaogong_db.query(KaogongCrawlerConfig).delete()
        kaogong_db.commit()
        kaogong_db.close()
        
        logger.info("✅ 已清除所有爬虫配置")
    except Exception as e:
        logger.error(f"清除爬虫配置失败: {str(e)}")

def start_crawler_scheduler():
    """启动爬虫调度器（智能版本）"""
    logger.info("启动爬虫调度器（智能版本）")
    
    try:
        # 1. 先检查是否有活跃用户
        active_users = check_active_users()
        
        if active_users == 0:
            logger.info("🛑 没有活跃用户，停止所有爬虫")
            
            # 停止所有定时任务
            crawler_scheduler.remove_all_jobs()
            
            # 清除所有爬虫配置
            clear_all_crawler_configs()
            
            logger.info("爬虫调度器已停止（无活跃用户）")
            return
        
        logger.info(f"✅ 检测到 {active_users} 个活跃用户，启动智能爬虫")
        
        # 2. 更新用户需求缓存
        asyncio.run(get_user_requirements())
        
        # 3. 生成智能动态爬虫配置
        dynamic_configs = generate_dynamic_crawler_configs()
        
        if not dynamic_configs:
            logger.warning("生成了0个爬虫配置，可能用户需求为空或配置错误")
            
            # 清理现有配置
            clear_all_crawler_configs()
            crawler_scheduler.remove_all_jobs()
            return
        
        # 4. 处理配置并创建任务
        _process_and_schedule_configs(dynamic_configs)
        
        logger.info(f"✅ 智能爬虫调度器启动完成，共 {len(dynamic_configs)} 个爬虫任务")
        
    except Exception as e:
        logger.error(f"启动爬虫调度器失败: {str(e)}")

def _process_and_schedule_configs(configs: List[Dict]):
    """处理配置并创建调度任务"""
    for config in configs:
        try:
            # 提取网站配置
            websites = config.get('websites', [])
            
            for website in websites:
                # 创建爬虫配置
                crawler_config = {
                    'name': website['name'],
                    'url': website['url'],
                    'selector': website['selector'],
                    'interval': website['interval'],
                    'priority': website['priority'],
                    'status': 1
                }
                
                # 添加到数据库
                _add_crawler_config_to_db(crawler_config)
                
        except Exception as e:
            logger.error(f"处理爬虫配置失败: {str(e)}")

def _add_crawler_config_to_db(config: Dict):
    """添加爬虫配置到数据库"""
    category = 'kaoyan' if '考研' in config['name'] else 'kaogong'
    
    if category == 'kaoyan':
        db = next(get_db(database="kaoyan"))
        try:
            new_config = KaoyanCrawlerConfig(
                name=config['name'],
                url=config['url'],
                selector=config['selector'],
                parse_rules=json.dumps({
                    'title': 'a',
                    'url': 'a@href',
                    'time': '.date',
                    'content': '.summary'
                }),
                interval=config['interval'],
                status=config['status'],
                priority=config['priority']
            )
            db.add(new_config)
            db.commit()
            logger.info(f"添加考研爬虫配置: {config['name']}")
        finally:
            db.close()
    else:
        db = next(get_db(database="kaogong"))
        try:
            new_config = KaogongCrawlerConfig(
                name=config['name'],
                url=config['url'],
                selector=config['selector'],
                parse_rules=json.dumps({
                    'title': 'a',
                    'url': 'a@href',
                    'time': '.date',
                    'content': '.summary'
                }),
                interval=config['interval'],
                status=config['status'],
                priority=config['priority']
            )
            db.add(new_config)
            db.commit()
            logger.info(f"添加考公爬虫配置: {config['name']}")
        finally:
            db.close()

# ============================================================================
# 原有的爬虫执行函数（保持兼容）
# ============================================================================

async def run_kaoyan_crawler(crawler_id: int):
    """运行考研爬虫"""
    db = next(get_db(database="kaoyan"))
    try:
        # 获取爬虫配置
        config = db.query(KaoyanCrawlerConfig).filter(KaoyanCrawlerConfig.id == crawler_id).first()
        if not config or config.status != 1:
            logger.warning(f"考研爬虫配置不存在或未激活: {crawler_id}")
            return
        
        start_time = datetime.now()
        logger.info(f"开始运行考研爬虫: {config.name}")
        
        # 运行爬虫
        crawler_config = {
            'url': config.url,
            'selector': config.selector,
            'parse_rules': config.parse_rules,
            'name': config.name
        }
        crawler = KaoyanCrawler(crawler_config)
        data = await crawler.run()
        
        # 存储数据
        stored_count = 0
        for item in data:
            # 检查是否已存在
            existing = db.query(KaoyanInfo).filter(KaoyanInfo.url == item['url']).first()
            if not existing:
                # 存储数据
                kaoyan_info = KaoyanInfo(
                    title=item['title'],
                    content=item['content'],
                    source=item['source'],
                    url=item['url'],
                    province=item.get('province'),
                    school=item.get('school'),
                    major=item.get('major'),
                    category=item.get('category'),
                    publish_date=item.get('publish_date'),
                    read_count=0,
                    like_count=0
                )
                db.add(kaoyan_info)
                stored_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"考研爬虫运行完成: {config.name}, 耗时: {duration:.2f}秒, 存储: {stored_count}条")
        
    except Exception as e:
        logger.error(f"考研爬虫运行失败: {str(e)}")
    finally:
        db.close()

async def run_kaogong_crawler(crawler_id: int):
    """运行考公爬虫"""
    db = next(get_db(database="kaogong"))
    try:
        # 获取爬虫配置
        config = db.query(KaogongCrawlerConfig).filter(KaogongCrawlerConfig.id == crawler_id).first()
        if not config or config.status != 1:
            logger.warning(f"考公爬虫配置不存在或未激活: {crawler_id}")
            return
        
        start_time = datetime.now()
        logger.info(f"开始运行考公爬虫: {config.name}")
        
        # 运行爬虫
        crawler_config = {
            'url': config.url,
            'selector': config.selector,
            'parse_rules': config.parse_rules
        }
        crawler = KaogongCrawler(crawler_config)
        data = await crawler.run()
        
        # 存储数据
        stored_count = 0
        for item in data:
            # 检查是否已存在
            existing = db.query(KaogongInfo).filter(KaogongInfo.url == item['url']).first()
            if not existing:
                # 存储数据
                kaogong_info = KaogongInfo(
                    title=item['title'],
                    content=item['content'],
                    source=item['source'],
                    url=item['url'],
                    province=item.get('province'),
                    position_type=item.get('position_type'),
                    major=item.get('major'),
                    education=item.get('education'),
                    category=item.get('category'),
                    publish_date=item.get('publish_date'),
                    read_count=0,
                    like_count=0
                )
                db.add(kaogong_info)
                stored_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"考公爬虫运行完成: {config.name}, 耗时: {duration:.2f}秒, 存储: {stored_count}条")
        
    except Exception as e:
        logger.error(f"考公爬虫运行失败: {str(e)}")
    finally:
        db.close()

# ============================================================================
# 导出函数
# ============================================================================

__all__ = [
    'get_user_requirements',
    'generate_dynamic_crawler_configs',
    'check_active_users',
    'clear_all_crawler_configs',
    'start_crawler_scheduler',
    'run_kaoyan_crawler',
    'run_kaogong_crawler',
    'crawler_scheduler',
    'user_requirements_cache'
]