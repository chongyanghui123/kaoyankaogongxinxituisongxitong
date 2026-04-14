#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能个性化爬虫管理器
直接替换 crawler_manager.py
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import re
import random
import time
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 添加项目路径，导入火山引擎模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

try:
    from volcengine_ai_integration import (
        VolcEngineConfig,
        VolcEngineEnhancedCrawlerManager
    )
    VOLCENGINE_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ 火山引擎AI模块导入成功")
except ImportError as e:
    VOLCENGINE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.error(f"❌ 火山引擎AI模块导入失败: {e}")
    raise

from core.database import get_db
from core.crawlers.kaoyan import KaoyanCrawler
from core.crawlers.kaogong import KaogongCrawler
from models.kaoyan import KaoyanInfo, KaoyanCrawlerConfig, KaoyanCrawlerLog
from models.kaogong import KaogongInfo, KaogongCrawlerConfig, KaogongCrawlerLog
from models.users import User, UserSubscription, UserKeyword

# 全局调度器
crawler_scheduler = AsyncIOScheduler()

# 缓存配置
cache_expiry = 300  # 缓存过期时间（秒）
crawler_configs_cache = []  # 爬虫配置缓存
cache_last_update = time.time()  # 缓存最后更新时间（时间戳）

# 用户需求缓存
user_requirements_cache = {}

# 火山引擎AI管理器
volcengine_manager = None

# ============================================================================
# 火山引擎AI集成
# ============================================================================

def init_volcengine_ai(api_key: str = None):
    """初始化火山引擎AI"""
    global volcengine_manager
    
    if not VOLCENGINE_AVAILABLE:
        logger.error("火山引擎AI模块不可用")
        raise Exception("火山引擎AI模块不可用")
    
    try:
        # 尝试从环境变量或配置文件获取API密钥
        if not api_key:
            # 尝试从配置模块获取
            from config import settings
            api_key = settings.VOLCENGINE_API_KEY
            
            # 尝试从环境变量获取
            if not api_key:
                api_key = os.getenv('VOLCENGINE_API_KEY')
                
                # 尝试从配置文件获取
                if not api_key:
                    config_path = os.path.join(project_root, 'config', 'volcengine_config.yaml')
                    if os.path.exists(config_path):
                        import yaml
                        with open(config_path, 'r', encoding='utf-8') as f:
                            config = yaml.safe_load(f)
                            api_key = config.get('api', {}).get('key')
        
        if not api_key or api_key == "your_volcengine_api_key_here":
            logger.error("未配置火山引擎API密钥")
            raise Exception("未配置火山引擎API密钥")
        
        # 初始化火山引擎管理器
        volcengine_manager = VolcEngineEnhancedCrawlerManager(api_key)
        logger.info("🔥 火山引擎AI管理器初始化成功")
        return True
        
    except Exception as e:
        logger.error(f"初始化火山引擎AI失败: {str(e)}")
        raise

async def analyze_demand_with_volcengine(raw_demand: str, student_context: Dict) -> Dict:
    """使用火山引擎AI分析需求"""
    global volcengine_manager
    
    if not volcengine_manager:
        init_volcengine_ai()
    
    try:
        # 使用火山引擎AI分析
        return await volcengine_manager.analyze_student_demand(
            student_id=0,  # 临时ID
            raw_demand=raw_demand,
            student_profile=student_context
        )
    except Exception as e:
        logger.error(f"火山引擎AI分析失败: {str(e)}")
        raise

# ============================================================================
# 智能需求理解（火山引擎增强版）
# ============================================================================

class SmartDemandAnalyzer:
    """智能需求分析器（火山引擎增强）"""
    
    @staticmethod
    async def analyze_demand(raw_demand: str, student_context: Dict = None) -> Dict:
        """分析需求（使用火山引擎AI）"""
        student_context = student_context or {}
        
        # 使用火山引擎AI
        analysis = await analyze_demand_with_volcengine(raw_demand, student_context)
        
        # 标准化分析结果
        return SmartDemandAnalyzer._standardize_volcengine_analysis(analysis)
    
    @staticmethod
    def _standardize_volcengine_analysis(analysis: Dict) -> Dict:
        """标准化火山引擎AI分析结果"""
        standardized = {
            'category': 'unknown',
            'provinces': [],
            'schools': [],
            'majors': [],
            'keywords': [],
            'urgency': 0,
            'action': 'monitor',
            'volcengine_analysis': analysis,  # 保留原始分析
            'ai_confidence': analysis.get('confidence', 0.0)
        }
        
        # 转换意图到类别
        intent = analysis.get('intent', '').lower()
        if 'kaoyan' in intent or '考研' in intent:
            standardized['category'] = 'kaoyan'
        elif 'kaogong' in intent or '考公' in intent:
            standardized['category'] = 'kaogong'
        
        # 提取实体
        entities = analysis.get('entities', {})
        if isinstance(entities, dict):
            standardized['provinces'] = entities.get('provinces', standardized['provinces'])
            standardized['schools'] = entities.get('schools', standardized['schools'])
            standardized['majors'] = entities.get('majors', standardized['majors'])
            standardized['keywords'] = entities.get('keywords', standardized['keywords'])
        
        # 设置紧急度
        urgency = analysis.get('urgency', 1)
        if isinstance(urgency, (int, float)):
            standardized['urgency'] = min(max(urgency, 1), 5)
        
        return standardized

# ============================================================================
# 智能网站匹配（火山引擎增强版）
# ============================================================================



# ============================================================================
# 智能爬虫生成（火山引擎增强版）
# ============================================================================

class SmartCrawlerGenerator:
    """智能爬虫生成器（火山引擎增强）"""
    
    @staticmethod
    async def generate_crawler_config(demand_analysis: Dict, user_id: int = None) -> Dict:
        """生成爬虫配置（火山引擎增强）"""
        # 1. 根据用户需求生成个性化网站配置（AI动态生成）
        websites = await SmartCrawlerGenerator._generate_personalized_websites(demand_analysis)
        
        if not websites:
            return None
        
        # 3. AI增强配置优化
        optimized_config = await SmartCrawlerGenerator._ai_optimize_config(
            demand_analysis, websites
        )
        
        # 4. 生成个性化配置
        category = demand_analysis.get('category', 'unknown')
        config = {
            'name': f"{category}-{datetime.now().strftime('%Y%m%d%H%M')}",
            'websites': websites,
            'demand_analysis': demand_analysis,
            'interval': optimized_config.get('interval', websites[0].get('interval', 30)),
            'priority': optimized_config.get('priority', websites[0].get('priority', 1)),
            'timeout': optimized_config.get('timeout', 20),
            'retry_times': optimized_config.get('retry_times', 3),
            'created_at': datetime.now(),
            'ai_enhanced': False,
            'match_scores': [w.get('match_score', 0.5) for w in websites]
        }
        
        if user_id:
            config['user_id'] = user_id
        
        return config
    
    @staticmethod
    async def _generate_personalized_websites(demand_analysis: Dict) -> List[Dict]:
        """根据用户需求生成个性化网站配置（AI动态生成）"""
        personalized_websites = []
        category = demand_analysis.get('category', 'unknown')
        
        # 从需求分析中提取关键词
        provinces = demand_analysis.get('provinces', [])
        schools = demand_analysis.get('schools', [])
        majors = demand_analysis.get('majors', [])
        keywords = demand_analysis.get('keywords', [])
        
        # 构建需求文本
        demand_text = f"类别: {category}\n"
        if provinces:
            demand_text += f"省份: {', '.join(provinces)}\n"
        if schools:
            demand_text += f"学校: {', '.join(schools)}\n"
        if majors:
            demand_text += f"专业: {', '.join(majors)}\n"
        if keywords:
            demand_text += f"关键词: {', '.join(keywords)}\n"
        
        # 调用AI生成相关网站
        ai_websites = await SmartCrawlerGenerator._ai_generate_websites(demand_text, category)
        personalized_websites.extend(ai_websites)
        
        # 去重
        seen_urls = set()
        unique_websites = []
        for website in personalized_websites:
            if website['url'] not in seen_urls:
                seen_urls.add(website['url'])
                unique_websites.append(website)
        
        return unique_websites
    
    @staticmethod
    async def _ai_generate_websites(demand_text: str, category: str) -> List[Dict]:
        """使用AI生成相关网站"""
        try:
            from volcengine_ai_integration import VolcEngineEnhancedCrawlerManager
            
            # 初始化AI管理器
            ai_manager = VolcEngineEnhancedCrawlerManager()
            
            # 构建AI提示
            prompt = """请根据以下用户需求，推荐15个最精准的个性化网站，用于考研或考公信息监控：

""" + demand_text + """

详细要求：
1. **精准度要求**：生成的链接必须是最精准的，直接链接到与用户需求最相关的页面，确保用户点击后能直接访问到所需信息
2. **导航要求**：链接必须指向符合要求的导航，确保网站结构清晰，用户能够轻松找到相关信息
3. **个性化推荐**：根据用户的具体需求（省份、学校、专业、关键词）生成高度相关的网站
4. **网站类型多样化**：
   - 官方网站：目标学校的研究生招生网、目标省份的教育考试院网站
   - 专业相关网站：与用户专业相关的学术网站、专业论坛
   - 考试资讯网站：针对性的考研/考公资讯网站
   - 学习资源网站：与用户专业相关的学习资源网站
   - 社区论坛：目标学校的考研论坛、专业相关的社区
5. **网站质量要求**：
   - 网站必须是真实存在的，可访问的
   - 优先推荐官方网站和权威网站，这些网站通常提供最准确和最及时的信息
   - 网站内容必须与用户需求高度相关
   - 包含不同类型的网站，提供全面的信息来源
   - **禁止推荐**：不要推荐 `https://yz.chsi.com.cn/sch/` 格式的链接，因为这些链接通常会返回404错误
   - **推荐方式**：对于学校，直接推荐学校的官方研究生招生网站，而不是通过第三方平台的链接
6. **推荐理由**：
   - 每个网站的推荐理由必须具体，说明为什么这个网站与用户需求相关
   - 推荐理由要结合用户的省份、学校、专业等具体需求
   - 详细说明网站的导航结构，确保用户能够轻松找到所需信息
7. **排序要求**：按照与用户需求的相关性排序，最相关的排在前面
8. **数量要求**：至少推荐15个网站，确保覆盖不同类型和角度

请以JSON格式返回，包含一个websites数组，每个元素包含以下字段：
- name：网站名称
- url：网站URL（确保链接是最精准的，直接指向相关内容）
- description：网站简短描述
- reason：推荐理由（详细说明与用户需求的相关性和网站的导航结构）
- type：网站类型（官方网站/专业网站/资讯网站/学习资源/社区论坛）
- relevance_score：相关性评分（0-10，10分最高）

示例输出格式：
{
  "websites": [
    {
      "name": "北京大学研究生招生网",
      "url": "https://admission.pku.edu.cn/",
      "description": "北京大学官方研究生招生网站，提供招生简章、专业目录、报名信息等",
      "reason": "用户目标学校是北京大学，该网站是北京大学官方研究生招生网站，提供最权威、最及时的招生信息，网站导航清晰，用户可以轻松找到招生简章、专业目录等相关信息",
      "type": "官方网站",
      "relevance_score": 10
    },
    ...
  ]
}
"""
            
            # 调用AI分析
            import json
            analysis = await ai_manager.ai_provider.analyze_demand(prompt, {})
            
            # 解析AI返回的网站
            websites = []
            if 'suggested_websites' in analysis:
                for site in analysis['suggested_websites']:
                    # 使用AI返回的相关性评分作为匹配分数
                    relevance_score = site.get('relevance_score', 5)
                    match_score = min(relevance_score / 10.0, 1.0)
                    
                    # 根据网站类型设置优先级
                    site_type = site.get('type', '资讯网站')
                    priority_map = {
                        '官方网站': 3,
                        '专业网站': 2,
                        '资讯网站': 1,
                        '学习资源': 2,
                        '社区论坛': 1
                    }
                    priority = priority_map.get(site_type, 1)
                    
                    # 根据相关性评分设置爬取间隔
                    if match_score >= 0.8:
                        interval = 30  # 高相关性网站，爬取频率更高
                    elif match_score >= 0.6:
                        interval = 45  # 中等相关性网站
                    else:
                        interval = 60  # 低相关性网站
                    
                    websites.append({
                        'name': site.get('name', '未知网站'),
                        'url': site.get('url', ''),
                        'selector': '.news-list li, .article-list li, .list-item, .news-item',
                        'interval': interval,
                        'priority': priority,
                        'match_score': match_score,
                        'personalized': True,
                        'ai_generated': True,
                        'site_type': site_type,
                        'description': site.get('description', ''),
                        'reason': site.get('reason', '')
                    })
            elif 'content' in analysis:
                # 尝试从内容中提取网站
                content = analysis['content']
                # 简单的URL提取
                import re
                url_pattern = r'https?://[\w\-._~:/?#[\]@!$&\'()*+,;=.]+'
                urls = re.findall(url_pattern, content)
                for url in urls[:10]:  # 最多提取10个URL
                    # 跳过 yz.chsi.com.cn/sch/ 格式的链接，因为这些链接通常会返回404错误
                    if 'yz.chsi.com.cn/sch' in url:
                        logger.warning(f"跳过 yz.chsi.com.cn/sch 格式的链接: {url}")
                        continue
                    
                    websites.append({
                        'name': f'AI推荐网站-{len(websites)+1}',
                        'url': url,
                        'selector': '.news-list li, .article-list li, .list-item, .news-item',
                        'interval': 60,
                        'priority': 1,
                        'match_score': 0.7,
                        'personalized': True,
                        'ai_generated': True,
                        'site_type': '资讯网站',
                        'description': 'AI推荐的网站',
                        'reason': '根据用户需求推荐的相关网站'
                    })
            
            return websites
        except Exception as e:
            logger.warning(f"AI生成网站失败: {str(e)}")
            return []
    

    
    @staticmethod
    async def _ai_optimize_config(demand_analysis: Dict, websites: List[Dict]) -> Dict:
        """AI优化配置"""
        optimized = {
            'interval': 30,
            'priority': 1,
            'timeout': 20,
            'retry_times': 3
        }
        
        # 根据紧急度优化
        urgency = demand_analysis.get('urgency', 0)
        if urgency >= 3:
            optimized['interval'] = 5
            optimized['priority'] = 3
            optimized['timeout'] = 30
            optimized['retry_times'] = 5
        elif urgency >= 2:
            optimized['interval'] = 15
            optimized['priority'] = 2
            optimized['timeout'] = 20
            optimized['retry_times'] = 3
        else:
            optimized['interval'] = 30
            optimized['priority'] = 1
            optimized['timeout'] = 15
            optimized['retry_times'] = 2
        
        # 根据网站匹配度微调
        if websites:
            avg_match_score = sum(w.get('match_score', 0) for w in websites) / len(websites)
            if avg_match_score > 0.8:
                # 高匹配度网站，可适当降低频率
                optimized['interval'] = min(optimized['interval'] * 1.2, 60)
        
        return optimized

# ============================================================================
# 火山引擎AI增强的核心函数
# ============================================================================

async def get_user_requirements():
    """获取所有用户的需求配置（火山引擎增强）"""
    global user_requirements_cache, cache_last_update
    
    # 检查缓存是否过期
    current_time = time.time()
    if current_time - cache_last_update < cache_expiry and user_requirements_cache:
        logger.info("📊 使用缓存的用户需求")
        return
    
    db = next(get_db(database="common"))
    try:
        # 批量获取所有用户的订阅配置，只选择需要的字段
        subscriptions = db.query(
            UserSubscription.user_id,
            UserSubscription.config_json,
            UserSubscription.created_at
        ).filter(
            UserSubscription.status == 1
        ).all()
        
        # 如果没有活跃用户，清空缓存
        if not subscriptions:
            user_requirements_cache = {}
            cache_last_update = current_time
            logger.info("🔄 没有活跃用户，清空用户需求缓存")
            return
        
        # 构建用户需求缓存
        requirements = {}
        user_ids = []
        
        for sub in subscriptions:
            user_id = sub.user_id
            user_ids.append(user_id)
            if user_id not in requirements:
                requirements[user_id] = {
                    'kaoyan': {},
                    'kaogong': {},
                    'profile': {
                        'user_id': user_id,
                        'subscription_date': sub.created_at.isoformat() if sub.created_at else None
                    }
                }
            
            if sub.config_json:
                if 'kaoyan' in sub.config_json:
                    kaoyan_config = sub.config_json['kaoyan']
                    # 确保keywords是列表
                    if 'keywords' in kaoyan_config and not isinstance(kaoyan_config['keywords'], list):
                        kaoyan_config['keywords'] = []
                    requirements[user_id]['kaoyan'] = kaoyan_config
                if 'kaogong' in sub.config_json:
                    kaogong_config = sub.config_json['kaogong']
                    # 确保keywords是列表
                    if 'keywords' in kaogong_config and not isinstance(kaogong_config['keywords'], list):
                        kaogong_config['keywords'] = []
                    requirements[user_id]['kaogong'] = kaogong_config
        
        # 批量获取所有活跃用户的关键词，使用IN查询提高效率
        if user_ids:
            keywords = db.query(UserKeyword).filter(
                UserKeyword.is_active == True,
                UserKeyword.user_id.in_(user_ids)
            ).all()
            
            for kw in keywords:
                user_id = kw.user_id
                if user_id not in requirements:
                    requirements[user_id] = {
                        'kaoyan': {},
                        'kaogong': {},
                        'profile': {'user_id': user_id}
                    }
                
                category = 'kaoyan' if kw.category == 1 else 'kaogong'
                if 'keywords' not in requirements[user_id][category]:
                    requirements[user_id][category]['keywords'] = []
                requirements[user_id][category]['keywords'].append(kw.keyword)
        
        user_requirements_cache = requirements
        cache_last_update = current_time
        logger.info(f"📊 更新用户需求缓存，共 {len(requirements)} 个活跃用户")
        
    except Exception as e:
        logger.error(f"❌ 获取用户需求失败: {str(e)}")
    finally:
        db.close()

async def generate_dynamic_crawler_configs() -> List[Dict[str, Any]]:
    """生成网站推荐"""
    global crawler_configs_cache, cache_last_update
    
    # 检查缓存是否过期
    current_time = time.time()
    if current_time - cache_last_update < cache_expiry and crawler_configs_cache:
        logger.info("🧠 使用缓存的网站推荐")
        return crawler_configs_cache
    
    logger.info("🧠 生成网站推荐")
    
    # 先检查是否有活跃用户
    active_users = check_active_users()
    if active_users == 0:
        logger.info("🛑 没有活跃用户，不生成网站推荐")
        return []
    
    logger.info(f"✅ 检测到 {active_users} 个活跃用户，生成网站推荐")
    
    db = next(get_db(database="common"))
    try:
        # 获取所有用户的订阅配置
        subscriptions = db.query(UserSubscription).filter(
            UserSubscription.status == 1
        ).all()
        
        if not subscriptions:
            logger.info("ℹ️ 没有用户订阅配置，不生成网站推荐")
            return []
        
        dynamic_configs = []
        tasks = []
        
        # 学校URL映射表
        school_url_map = {
            '中山大学': 'https://graduate.sysu.edu.cn/',
            '北京大学': 'https://admission.pku.edu.cn/',
            '清华大学': 'https://yz.tsinghua.edu.cn/',
            '复旦大学': 'https://gs.fudan.edu.cn/',
            '上海交通大学': 'https://yzb.sjtu.edu.cn/'
        }
        
        async def process_subscription(sub):
            """处理单个用户的订阅配置"""
            if not sub.config_json:
                return []
            
            config_json = sub.config_json
            user_profile = user_requirements_cache.get(sub.user_id, {}).get('profile', {})
            user_configs = []
            
            # 处理考研需求
            if 'kaoyan' in config_json:
                kaoyan_config = config_json['kaoyan']
                
                # 构造需求文本，添加明确的类别信息
                demand_text = f"考研 {_construct_demand_text(kaoyan_config)}"
                
                # 火山引擎AI分析需求
                demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, user_profile)
                
                # 确保 category 字段正确设置
                demand_analysis['category'] = 'kaoyan'
                
                # 生成AI增强的爬虫配置
                crawler_config = await SmartCrawlerGenerator.generate_crawler_config(demand_analysis, sub.user_id)
                
                if crawler_config:
                    # 只添加网站信息，不创建爬虫配置
                    websites = crawler_config.get('websites', [])
                    for website in websites:
                        website_info = {
                            'user_id': sub.user_id,
                            'category': 'kaoyan',
                            'name': website['name'],
                            'url': website['url'],
                            'description': website.get('description', ''),
                            'reason': website.get('reason', ''),
                            'type': website.get('type', 'unknown'),
                            'relevance_score': website.get('relevance_score', 0)
                        }
                        user_configs.append(website_info)
                
                # 为用户的每个学校生成专属网站信息
                schools = kaoyan_config.get('schools', [])
                if schools:
                    for school in schools:
                        # 清理学校名称，移除括号内容
                        clean_school = school.split('（')[0].split('(')[0]
                        
                        # 检查是否在映射表中
                        if clean_school in school_url_map:
                            url = school_url_map[clean_school]
                            
                            # 创建学校专属网站信息
                            school_website_info = {
                                'user_id': sub.user_id,
                                'category': 'kaoyan',
                                'name': f"{clean_school}研究生招生网",
                                'url': url,
                                'description': f"{clean_school}官方研究生招生网站",
                                'reason': f"用户关注{clean_school}，直接访问官方网站获取最新招生信息",
                                'type': 'official',
                                'relevance_score': 0.9
                            }
                            user_configs.append(school_website_info)
                            logger.info(f"🎯 为用户 {sub.user_id} 推荐网站: {clean_school} - {url}")
            
            # 处理考公需求
            if 'kaogong' in config_json:
                kaogong_config = config_json['kaogong']
                
                # 构造需求文本，添加明确的类别信息
                demand_text = f"考公 {_construct_demand_text(kaogong_config)}"
                
                # 火山引擎AI分析需求
                demand_analysis = await SmartDemandAnalyzer.analyze_demand(demand_text, user_profile)
                
                # 确保 category 字段正确设置
                demand_analysis['category'] = 'kaogong'
                
                # 生成AI增强的爬虫配置
                crawler_config = await SmartCrawlerGenerator.generate_crawler_config(demand_analysis, sub.user_id)
                
                if crawler_config:
                    # 只添加网站信息，不创建爬虫配置
                    websites = crawler_config.get('websites', [])
                    for website in websites:
                        website_info = {
                            'user_id': sub.user_id,
                            'category': 'kaogong',
                            'name': website['name'],
                            'url': website['url'],
                            'description': website.get('description', ''),
                            'reason': website.get('reason', ''),
                            'type': website.get('type', 'unknown'),
                            'relevance_score': website.get('relevance_score', 0)
                        }
                        user_configs.append(website_info)
            
            return user_configs
        
        # 为每个订阅创建异步任务
        for sub in subscriptions:
            tasks.append(process_subscription(sub))
        
        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 收集结果
        for result in results:
            if isinstance(result, list):
                dynamic_configs.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"❌ 处理订阅失败: {str(result)}")
        
        # 缓存网站信息
        crawler_configs_cache = dynamic_configs
        cache_last_update = current_time
        
        logger.info(f"🎯 根据用户需求生成了 {len(dynamic_configs)} 个网站推荐")
        return dynamic_configs
        
    except Exception as e:
        logger.error(f"❌ 生成网站推荐失败: {str(e)}")
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
        # 使用count(*)提高查询效率
        from sqlalchemy import func
        active_count = db.query(func.count(UserSubscription.id)).filter(
            UserSubscription.status == 1
        ).scalar()
        return active_count or 0
    except Exception as e:
        logger.error(f"❌ 检查活跃用户失败: {str(e)}")
        return 0
    finally:
        db.close()

def clear_all_crawler_configs():
    """清除所有爬虫配置"""
    try:
        # 批量清除爬虫配置，使用批量删除提高效率
        # 清除考研爬虫配置
        kaoyan_db = next(get_db(database="kaoyan"))
        try:
            # 使用批量删除，不返回被删除的对象，提高效率
            kaoyan_db.query(KaoyanCrawlerConfig).delete(synchronize_session=False)
            kaoyan_db.commit()
        finally:
            kaoyan_db.close()
        
        # 清除考公爬虫配置
        kaogong_db = next(get_db(database="kaogong"))
        try:
            # 使用批量删除，不返回被删除的对象，提高效率
            kaogong_db.query(KaogongCrawlerConfig).delete(synchronize_session=False)
            kaogong_db.commit()
        finally:
            kaogong_db.close()
        
        logger.info("✅ 已清除所有爬虫配置")
    except Exception as e:
        logger.error(f"❌ 清除爬虫配置失败: {str(e)}")

async def start_crawler_scheduler():
    """生成网站推荐（只执行一次）"""
    logger.info("🚀 生成网站推荐（只执行一次）")
    
    try:
        # 1. 初始化火山引擎AI
        init_volcengine_ai()
        
        # 2. 先检查是否有活跃用户
        active_users = check_active_users()
        
        if active_users == 0:
            logger.info("🛑 没有活跃用户，不生成网站推荐")
            return
        
        logger.info(f"✅ 检测到 {active_users} 个活跃用户，生成网站推荐")
        
        # 3. 更新用户需求缓存
        await get_user_requirements()
        
        # 4. 生成网站推荐
        dynamic_configs = await generate_dynamic_crawler_configs()
        
        if not dynamic_configs:
            logger.warning("⚠️ 生成了0个网站推荐，可能用户需求为空或配置错误")
            return
        
        logger.info(f"✅ 网站推荐生成完成，共 {len(dynamic_configs)} 个网站")
        
    except Exception as e:
        logger.error(f"❌ 生成网站推荐失败: {str(e)}")

async def _schedule_and_process_configs(configs: List[Dict]):
    """调度处理配置"""
    processed_count = 0
    tasks = []
    
    for config in configs:
        try:
            # 提取网站配置
            websites = config.get('websites', [])
            user_id = config.get('user_id')
            category = config.get('category', 'unknown')
            
            for website in websites:
                # 创建爬虫配置
                crawler_config = {
                    'name': website['name'],
                    'url': website['url'],
                    'selector': website['selector'],
                    'interval': website.get('interval', config.get('interval', 30)),
                    'priority': website.get('priority', config.get('priority', 1)),
                    'timeout': config.get('timeout', 20),
                    'retry_times': config.get('retry_times', 3),
                    'status': 1,
                    'user_id': user_id,
                    'ai_enhanced': False,
                    'match_score': website.get('match_score', 0),
                    'personalized': website.get('personalized', False),
                    'category': category
                }
                
                # 创建异步任务
                tasks.append(_add_crawler_config_to_db(crawler_config))
                processed_count += 1
                
        except Exception as e:
            logger.error(f"❌ 处理爬虫配置失败: {str(e)}")
    
    # 并发执行所有任务
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    
    return processed_count

async def _add_crawler_config_to_db(config: Dict):
    """添加爬虫配置到数据库"""
    category = 'kaoyan' if '考研' in config['name'] or 'kaoyan' in config['name'].lower() else 'kaogong'
    
    parse_rules = {
        'title': 'a',
        'url': 'a@href',
        'time': '.date, .time, span[class*="date"], span[class*="time"]',
        'content': '.summary, .content, .description'
    }
    
    # 序列化解析规则，避免重复序列化
    parse_rules_json = json.dumps(parse_rules)
    
    if category == 'kaoyan':
        db = next(get_db(database="kaoyan"))
        try:
            # 检查URL是否已存在，避免重复添加
            existing = db.query(KaoyanCrawlerConfig).filter(
                KaoyanCrawlerConfig.url == config['url']
            ).first()
            
            if not existing:
                new_config = KaoyanCrawlerConfig(
                    name=config['name'],
                    url=config['url'],
                    selector=config['selector'],
                    parse_rules=parse_rules_json,
                    interval=config['interval'],
                    status=config['status'],
                    priority=config['priority'],
                    user_id=config.get('user_id')
                )
                db.add(new_config)
                db.commit()
                logger.info(f"✅ 添加考研爬虫配置: {config['name']} (匹配度: {config.get('match_score', 0):.2f})")
            else:
                logger.info(f"ℹ️ 考研爬虫配置已存在: {config['url']}")
        except Exception as e:
            logger.error(f"❌ 添加考研爬虫配置失败: {str(e)}")
            db.rollback()
        finally:
            db.close()
    else:
        db = next(get_db(database="kaogong"))
        try:
            # 检查URL是否已存在，避免重复添加
            existing = db.query(KaogongCrawlerConfig).filter(
                KaogongCrawlerConfig.url == config['url']
            ).first()
            
            if not existing:
                new_config = KaogongCrawlerConfig(
                    name=config['name'],
                    url=config['url'],
                    selector=config['selector'],
                    parse_rules=parse_rules_json,
                    interval=config['interval'],
                    status=config['status'],
                    priority=config['priority'],
                    user_id=config.get('user_id')
                )
                db.add(new_config)
                db.commit()
                logger.info(f"✅ 添加考公爬虫配置: {config['name']} (匹配度: {config.get('match_score', 0):.2f})")
            else:
                logger.info(f"ℹ️ 考公爬虫配置已存在: {config['url']}")
        except Exception as e:
            logger.error(f"❌ 添加考公爬虫配置失败: {str(e)}")
            db.rollback()
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
            logger.warning(f"⚠️ 考研爬虫配置不存在或未激活: {crawler_id}")
            return
        
        start_time = datetime.now()
        logger.info(f"🚀 开始运行考研爬虫: {config.name}")
        
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
        
        logger.info(f"✅ 考研爬虫运行完成: {config.name}, 耗时: {duration:.2f}秒, 存储: {stored_count}条")
        
    except Exception as e:
        logger.error(f"❌ 考研爬虫运行失败: {str(e)}")
    finally:
        db.close()

async def run_kaogong_crawler(crawler_id: int):
    """运行考公爬虫"""
    db = next(get_db(database="kaogong"))
    try:
        # 获取爬虫配置
        config = db.query(KaogongCrawlerConfig).filter(KaogongCrawlerConfig.id == crawler_id).first()
        if not config or config.status != 1:
            logger.warning(f"⚠️ 考公爬虫配置不存在或未激活: {crawler_id}")
            return
        
        start_time = datetime.now()
        logger.info(f"🚀 开始运行考公爬虫: {config.name}")
        
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
        
        logger.info(f"✅ 考公爬虫运行完成: {config.name}, 耗时: {duration:.2f}秒, 存储: {stored_count}条")
        
    except Exception as e:
        logger.error(f"❌ 考公爬虫运行失败: {str(e)}")
    finally:
        db.close()

# ============================================================================
# 火山引擎AI状态监控
# ============================================================================

def get_volcengine_status() -> Dict:
    """获取火山引擎AI状态"""
    if not volcengine_manager:
        return {
            'enabled': False,
            'status': 'not_initialized',
            'message': '火山引擎AI未初始化'
        }
    
    try:
        status = volcengine_manager.get_status()
        return {
            'enabled': True,
            'status': 'active',
            'provider': status['ai_provider']['provider'],
            'model': status['ai_provider']['model'],
            'performance': status['ai_provider']['performance'],
            'cache_stats': status['cache_stats']
        }
    except Exception as e:
        return {
            'enabled': False,
            'status': 'error',
            'error': str(e)
        }

def remove_crawler_job(crawler_type: str, config_id: int):
    """从调度器中移除爬虫任务"""
    try:
        job_id = f"{crawler_type}_crawler_{config_id}"
        if crawler_scheduler and crawler_scheduler.get_job(job_id):
            crawler_scheduler.remove_job(job_id)
            logger.info(f"✅ 从调度器中移除爬虫任务: {job_id}")
        else:
            logger.info(f"ℹ️ 爬虫任务不存在: {job_id}")
    except Exception as e:
        logger.error(f"❌ 移除爬虫任务失败: {str(e)}")

# ============================================================================
# 导出函数
# ============================================================================

__all__ = [
    # 核心函数
    'get_user_requirements',
    'generate_dynamic_crawler_configs',
    'check_active_users',
    'clear_all_crawler_configs',
    'start_crawler_scheduler',
    'run_kaoyan_crawler',
    'run_kaogong_crawler',
    'remove_crawler_job',
    
    # 火山引擎AI相关
    'init_volcengine_ai',
    'get_volcengine_status',
    
    # 智能分析器
    'SmartDemandAnalyzer',
    'SmartCrawlerGenerator',
    
    # 全局变量
    'crawler_scheduler',
    'user_requirements_cache',
    'volcengine_manager'
]