#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎Coding Plan (DeepSeek) 集成方案
专为考研考公双赛道情报监控系统设计
"""

import os
import sys
import json
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import time
from enum import Enum
from functools import lru_cache

# 设置项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

logger = logging.getLogger(__name__)

# ============================================================================
# 火山引擎Coding Plan配置
# ============================================================================

@dataclass
class VolcEngineConfig:
    """火山引擎配置"""
    api_key: str = ""
    api_url: str = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    model: str = "doubao-seed-2-0-code-preview-260215"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60  # 增加超时时间到60秒
    max_retries: int = 3
    concurrent_limit: int = 5  # 并发请求限制
    
    @classmethod
    def from_env(cls) -> 'VolcEngineConfig':
        """从环境变量加载配置"""
        return cls(
            api_key=os.getenv('VOLCENGINE_API_KEY', ''),
            api_url=os.getenv('VOLCENGINE_API_URL', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'),
            model=os.getenv('VOLCENGINE_MODEL', 'doubao-seed-2-0-code-preview-260215'),
            temperature=float(os.getenv('VOLCENGINE_TEMPERATURE', '0.7')),
            max_tokens=int(os.getenv('VOLCENGINE_MAX_TOKENS', '2000'))
        )

# ============================================================================
# 火山引擎AI服务集成
# ============================================================================

class VolcEngineAIProvider:
    """火山引擎AI服务提供商"""
    
    def __init__(self, config: VolcEngineConfig):
        self.config = config
        self.session = None
        self.cache = {}  # 内存缓存
        self.request_count = 0
        self.success_rate = 0.0
        self.avg_response_time = 0.0
        self.semaphore = asyncio.Semaphore(config.concurrent_limit)  # 并发控制
        self.retry_delay = 2  # 重试延迟（秒）
        
        logger.info(f"🔥 初始化火山引擎AI服务: model={config.model}, endpoint={config.api_url}")
    
    async def initialize(self):
        """初始化连接"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
    
    async def close(self):
        """关闭连接"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def analyze_demand(self, raw_demand: str, student_context: Dict) -> Dict:
        """分析学生需求"""
        return await self._call_volcengine_ai(
            "analyze_demand",
            raw_demand,
            student_context
        )
    
    async def extract_entities(self, text: str) -> Dict:
        """提取实体信息"""
        return await self._call_volcengine_ai(
            "extract_entities",
            text,
            {}
        )
    
    async def recommend_strategy(self, demand_analysis: Dict) -> Dict:
        """推荐监控策略"""
        return await self._call_volcengine_ai(
            "recommend_strategy",
            demand_analysis,
            {}
        )
    
    async def _call_volcengine_ai(self, task_type: str, text: str, context: Dict) -> Dict:
        """调用火山引擎AI服务"""
        
        # 检查缓存
        cache_key = f"{task_type}_{hash(text)}_{hash(str(context))}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if time.time() - cached['timestamp'] < 1800:  # 30分钟缓存
                logger.info(f"使用缓存结果: {task_type}")
                cached['result']['cached'] = True
                return cached['result']
        
        await self.initialize()
        
        # 构建请求
        prompt = self._build_prompt(task_type, text, context)
        payload = self._build_payload(prompt)
        
        # 并发控制
        async with self.semaphore:
            for retry in range(self.config.max_retries):
                start_time = time.time()
                self.request_count += 1
                
                try:
                    # 发送请求
                    async with self.session.post(
                        self.config.api_url,
                        json=payload,
                        headers=self._build_headers()
                    ) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            
                            # 解析响应
                            result = self._parse_response(
                                task_type,
                                data,
                                text,
                                context
                            )
                            
                            # 更新性能指标
                            response_time = time.time() - start_time
                            self._update_performance_metrics(True, response_time)
                            
                            # 缓存结果
                            self.cache[cache_key] = {
                                'result': result,
                                'timestamp': time.time(),
                                'task_type': task_type
                            }
                            
                            logger.info(f"✅ AI分析成功: {task_type}, 耗时: {response_time:.2f}秒, 重试次数: {retry}")
                            return result
                            
                        elif response.status == 429:
                            # 限流，等待后重试
                            error_text = await response.text()
                            logger.warning(f"🔄 被限流，等待后重试... (重试 {retry+1}/{self.config.max_retries})")
                            # 指数退避重试
                            delay = self.retry_delay * (2 ** retry)
                            await asyncio.sleep(delay)
                            continue
                            
                        else:
                            error_text = await response.text()
                            logger.error(f"❌ AI请求失败: {response.status}, 错误: {error_text}")
                            if retry < self.config.max_retries - 1:
                                logger.warning(f"尝试重试... (重试 {retry+1}/{self.config.max_retries})")
                                await asyncio.sleep(self.retry_delay)
                                continue
                            raise Exception(f"AI服务请求失败: {response.status}")
                            
                except asyncio.TimeoutError:
                    logger.error(f"⏰ AI请求超时 (重试 {retry+1}/{self.config.max_retries})")
                    if retry < self.config.max_retries - 1:
                        logger.warning(f"尝试重试... (重试 {retry+1}/{self.config.max_retries})")
                        await asyncio.sleep(self.retry_delay)
                        continue
                    self._update_performance_metrics(False, 0)
                    raise
                except aiohttp.ClientError as e:
                    logger.error(f"❌ HTTP客户端错误: {str(e)} (重试 {retry+1}/{self.config.max_retries})")
                    if retry < self.config.max_retries - 1:
                        logger.warning(f"尝试重试... (重试 {retry+1}/{self.config.max_retries})")
                        await asyncio.sleep(self.retry_delay)
                        continue
                    self._update_performance_metrics(False, 0)
                    raise
                except Exception as e:
                    logger.error(f"❌ AI调用异常: {str(e)} (重试 {retry+1}/{self.config.max_retries})")
                    if retry < self.config.max_retries - 1:
                        logger.warning(f"尝试重试... (重试 {retry+1}/{self.config.max_retries})")
                        await asyncio.sleep(self.retry_delay)
                        continue
                    self._update_performance_metrics(False, 0)
                    raise
        
        # 所有重试都失败
        logger.error(f"❌ 所有重试都失败: {task_type}")
        raise Exception("所有AI请求重试都失败")
    
    def _build_prompt(self, task_type: str, text: str, context: Dict) -> str:
        """构建AI提示词"""
        
        prompts = {
            "analyze_demand": f"""请作为考研考公需求分析专家，分析以下学生需求：

学生需求："{text}"
学生背景：{json.dumps(context, ensure_ascii=False, indent=2) if context else '无特别背景'}

请详细分析以下内容：
1. **主要意图**：考研（kaoyan）、考公（kaogong）、双赛道（dual）还是其他？
2. **紧急程度**：1-5分（5分表示非常紧急，需要实时监控）
3. **关注焦点**：
   - 省份/地区：如北京、上海
   - 学校：如北京大学、清华大学
   - 专业：如计算机、人工智能
   - 职位类型：如税务局、财政局
4. **建议监控策略**：
   - 建议爬虫频率（分钟）
   - 优先级（high/medium/low）
   - 重点监控网站推荐
   - 预期信息更新频率
5. **个性化建议**：
   - 针对该学生背景的具体建议
   - 潜在风险提示
   - 优化建议

请以JSON格式返回结果，包含以下字段：
- intent: 主要意图
- confidence: 置信度（0.0-1.0）
- urgency: 紧急程度（1-5）
- entities: 实体信息对象（provinces[], schools[], majors[], position_types[]）
- ai_recommendations: AI建议列表
- suggested_websites: 推荐网站列表
- monitoring_strategy: 监控策略详情
- personalized_advice: 个性化建议

请确保分析专业、准确，考虑到考研考公的特殊性。
""",

            "extract_entities": f"""请从以下文本中提取考研考公相关的实体信息：

文本："{text}"

需要提取的实体类型：
1. **省份/地区**：如北京、上海、广东
2. **学校/机构**：如北京大学、清华大学、国家公务员局
3. **专业/学科**：如计算机、软件工程、人工智能
4. **职位类型**：如税务局、财政局、教育局
5. **考试类型**：考研、考公、事业单位考试
6. **关键词**：如招生简章、职位表、报名时间
7. **时间信息**：如2024年、3月、明天、月底

请确保提取准确、全面。
请以JSON格式返回，包含entities字段。
""",

            "recommend_strategy": f"""请根据以下需求分析结果，推荐智能监控策略：

需求分析：
{json.dumps(text if isinstance(text, dict) else {'raw_analysis': text}, ensure_ascii=False, indent=2)}

请推荐：
1. **爬虫频率优化**：根据紧急度和重要性，推荐最佳监控频率
2. **网站优先级**：推荐最适合的监控网站（前3名）
3. **容错策略**：建议的失败处理和重试机制
4. **性能优化**：建议的并发控制、缓存策略
5. **风险控制**：反爬虫策略、访问频率控制

请以JSON格式返回推荐策略。
"""
        }
        
        return prompts.get(task_type, text)
    
    def _build_payload(self, prompt: str) -> Dict:
        """构建请求体"""
        return {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的考研考公情报分析专家，精通教育政策、招生信息和职位招聘。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": False
        }
    
    def _build_headers(self) -> Dict:
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
            "Accept": "application/json"
        }
    
    def _parse_response(self, task_type: str, response: Dict, original_text: str, context: Dict) -> Dict:
        """解析AI响应"""
        
        # 提取回答内容
        choices = response.get('choices', [])
        if not choices:
            raise ValueError("AI响应中没有choices字段")
        
        message = choices[0].get('message', {})
        content = message.get('content', '')
        
        if not content:
            raise ValueError("AI响应内容为空")
        
        # 尝试解析JSON
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        
        if json_match:
            result = json.loads(json_match.group())
        else:
            # 如果不是JSON，构造结果
            result = self._construct_result(task_type, content, original_text, context)
        
        # 添加元数据
        result.update({
            'task_type': task_type,
            'ai_model': self.config.model,
            'provider': 'volcengine_coding_plan',
            'response_timestamp': datetime.now().isoformat(),
            'original_text': original_text,
            'context': context,
            'raw_response': response,
            'cached': False
        })
        
        return result
    
    def _construct_result(self, task_type: str, content: str, original_text: str, context: Dict) -> Dict:
        """构造标准化的结果"""
        
        base_result = {
            'success': True,
            'task_type': task_type,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'original_text': original_text,
            'context': context
        }
        
        if task_type == "analyze_demand":
            # 从内容中提取意图和紧急度
            base_result.update({
                'intent': 'unknown',
                'confidence': 0.5,
                'urgency': 1,
                'entities': {},
                'ai_recommendations': ['AI分析成功，但格式解析失败'],
                'suggested_websites': [],
                'monitoring_strategy': {},
                'personalized_advice': []
            })
            
            # 简单规则提取
            if '考研' in original_text:
                base_result['intent'] = 'kaoyan'
                base_result['confidence'] = 0.8
            elif '考公' in original_text:
                base_result['intent'] = 'kaogong'
                base_result['confidence'] = 0.8
            
            if '紧急' in original_text:
                base_result['urgency'] = 4
        
        return base_result
    

    
    def _update_performance_metrics(self, success: bool, response_time: float):
        """更新性能指标"""
        if success:
            self.success_rate = (self.success_rate * (self.request_count - 1) + 1) / self.request_count
            self.avg_response_time = (self.avg_response_time * (self.request_count - 1) + response_time) / self.request_count
        else:
            self.success_rate = (self.success_rate * (self.request_count - 1)) / self.request_count
        
        # 定期清理过期缓存
        if self.request_count % 10 == 0:
            self._clean_expired_cache()
    
    def _clean_expired_cache(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = []
        
        # 批量清理过期缓存
        for key, value in list(self.cache.items()):
            if current_time - value['timestamp'] > 3600:  # 1小时过期
                expired_keys.append(key)
                del self.cache[key]
        
        if expired_keys:
            logger.debug(f"清理缓存: {len(expired_keys)} 个过期条目")
        
        # 限制缓存大小，防止内存溢出
        max_cache_size = 1000
        if len(self.cache) > max_cache_size:
            # 按时间排序，删除最旧的缓存
            sorted_keys = sorted(self.cache.items(), key=lambda x: x[1]['timestamp'])
            keys_to_delete = [k for k, v in sorted_keys[:len(self.cache) - max_cache_size]]
            for key in keys_to_delete:
                del self.cache[key]
            logger.debug(f"限制缓存大小: 删除 {len(keys_to_delete)} 个最旧条目")
    
    def get_performance_metrics(self) -> Dict:
        """获取性能指标"""
        return {
            'request_count': self.request_count,
            'success_rate': self.success_rate,
            'avg_response_time': self.avg_response_time,
            'cache_size': len(self.cache),
            'provider': 'volcengine_coding_plan',
            'model': self.config.model
        }

# ============================================================================
# 火山引擎AI增强的爬虫管理器
# ============================================================================

class VolcEngineEnhancedCrawlerManager:
    """火山引擎AI增强爬虫管理器"""
    
    def __init__(self, api_key: str = None):
        # 尝试从配置模块获取
        try:
            from config import settings
            self.config = VolcEngineConfig(
                api_key=api_key or settings.VOLCENGINE_API_KEY,
                api_url=settings.VOLCENGINE_API_URL,
                model=settings.VOLCENGINE_MODEL,
                temperature=settings.VOLCENGINE_TEMPERATURE
            )
        except Exception:
            # 回退到环境变量
            self.config = VolcEngineConfig.from_env()
            if api_key:
                self.config.api_key = api_key
        
        self.ai_provider = VolcEngineAIProvider(self.config)
        
        # 用户需求缓存
        self.user_demands_cache = {}
        self.analysis_results_cache = {}
        
        logger.info("🚀 火山引擎AI增强爬虫管理器初始化完成")
    
    async def shutdown(self):
        """关闭管理器"""
        await self.ai_provider.close()
        logger.info("🔄 火山引擎AI增强爬虫管理器已关闭")
    
    async def analyze_student_demand(self, student_id: int, raw_demand: str, student_profile: Dict) -> Dict:
        """分析学生需求"""
        logger.info(f"🧠 分析学生{student_id}需求: {raw_demand}")
        
        # 检查缓存
        cache_key = f"demand_{student_id}_{hash(raw_demand)}"
        if cache_key in self.analysis_results_cache:
            cached = self.analysis_results_cache[cache_key]
            if time.time() - cached['timestamp'] < 1800:  # 30分钟缓存
                logger.info(f"使用缓存分析结果: 学生{student_id}")
                cached['result']['cached'] = True
                return cached['result']
        
        try:
            # 调用AI分析
            analysis_result = await self.ai_provider.analyze_demand(raw_demand, student_profile)
            
            # 缓存结果
            self.analysis_results_cache[cache_key] = {
                'result': analysis_result,
                'timestamp': time.time(),
                'student_id': student_id
            }
            
            # 更新用户需求缓存
            if student_id not in self.user_demands_cache:
                self.user_demands_cache[student_id] = []
            
            self.user_demands_cache[student_id].append({
                'demand': raw_demand,
                'analysis': analysis_result,
                'timestamp': datetime.now().isoformat()
            })
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析学生{student_id}需求失败: {str(e)}")
            raise
    
    async def generate_smart_crawler_config(self, demand_analysis: Dict, student_id: int) -> Dict:
        """生成智能爬虫配置"""
        logger.info(f"🛠️ 为学生{student_id}生成智能爬虫配置")
        
        try:
            # 获取推荐策略
            strategy_result = await self.ai_provider.recommend_strategy(demand_analysis)
            
            # 生成个性化配置
            config = await self._build_crawler_config(
                demand_analysis,
                strategy_result,
                student_id
            )
            
            return config
            
        except Exception as e:
            logger.error(f"生成爬虫配置失败: {str(e)}")
            raise
    
    async def schedule_smart_crawlers(self, crawler_tasks: List[Dict], system_status: Dict) -> List[Dict]:
        """智能调度爬虫"""
        logger.info(f"📅 AI智能调度 {len(crawler_tasks)} 个爬虫任务")
        
        # 根据系统负载智能调度
        system_load = system_status.get('load', 0.5)
        
        optimized_tasks = []
        
        for task in crawler_tasks:
            # AI优化任务参数
            optimized_task = await self._optimize_task_with_ai(task, system_load)
            optimized_tasks.append(optimized_task)
        
        # 智能排序
        sorted_tasks = await self._intelligent_sort_tasks(optimized_tasks, system_load)
        
        logger.info(f"✅ AI调度完成，优化后任务数: {len(sorted_tasks)}")
        return sorted_tasks
    
    async def _optimize_task_with_ai(self, task: Dict, system_load: float) -> Dict:
        """AI优化单个任务"""
        optimized = task.copy()
        
        # 根据紧急度和系统负载优化参数
        urgency = task.get('urgency', 0)
        
        if urgency > 0.8:
            # 紧急任务，即使负载高也要保证监控
            optimized['frequency'] = max(5, 10 - int(system_load * 10))
            optimized['priority'] = 'high'
            optimized['timeout'] = 30
        elif urgency > 0.5:
            # 重要任务，根据负载调整
            base_frequency = 20
            load_factor = 1 + system_load * 0.5
            optimized['frequency'] = int(base_frequency * load_factor)
            optimized['priority'] = 'medium'
            optimized['timeout'] = 20
        else:
            # 普通任务，负载高时降低频率
            base_frequency = 40
            load_factor = 1 + system_load * 1.0
            optimized['frequency'] = int(base_frequency * load_factor)
            optimized['priority'] = 'low'
            optimized['timeout'] = 15
        
        return optimized
    
    async def _intelligent_sort_tasks(self, tasks: List[Dict], system_load: float) -> List[Dict]:
        """智能排序任务"""
        
        def task_score(task: Dict) -> float:
            """计算任务得分"""
            urgency = task.get('urgency', 0)
            priority_map = {'high': 3, 'medium': 2, 'low': 1}
            priority = priority_map.get(task.get('priority', 'low'), 1)
            
            # 基础得分：紧急度 * 优先级
            base_score = urgency * priority
            
            # 负载调整：负载高时降低非紧急任务得分
            if urgency < 0.4:
                load_penalty = system_load * 0.5
                adjusted_score = base_score - load_penalty
            else:
                adjusted_score = base_score
            
            return max(adjusted_score, 0.1)
        
        return sorted(tasks, key=task_score, reverse=True)
    
    async def _build_crawler_config(self, demand_analysis: Dict, strategy_result: Dict, student_id: int) -> Dict:
        """构建爬虫配置"""
        
        config = {
            'student_id': student_id,
            'timestamp': datetime.now().isoformat(),
            'demand_analysis': demand_analysis,
            'ai_strategy': strategy_result,
            
            # 爬虫核心配置
            'crawler': {
                'type': demand_analysis.get('intent', 'unknown'),
                'frequency': strategy_result.get('suggested_frequency', 30),
                'priority': strategy_result.get('priority', 'medium'),
                'timeout': strategy_result.get('timeout', 20),
                'retry_times': strategy_result.get('retry_times', 3),
                'max_concurrent': 2,
                
                # 反爬虫策略
                'anti_crawler': {
                    'random_delay': True,
                    'use_proxies': True,
                    'rotate_user_agents': True,
                    'max_requests_per_minute': 10
                },
                
                # 监控网站
                'websites': strategy_result.get('suggested_websites', []),
                
                # 实体过滤
                'filters': {
                    'provinces': demand_analysis.get('entities', {}).get('provinces', []),
                    'schools': demand_analysis.get('entities', {}).get('schools', []),
                    'majors': demand_analysis.get('entities', {}).get('majors', []),
                    'keywords': demand_analysis.get('entities', {}).get('keywords', [])
                },
                
                # 通知配置
                'notification': {
                    'enabled': True,
                    'channels': ['email', 'app_push'],
                    'threshold': 'new_info'
                }
            },
            
            # 性能监控
            'monitoring': {
                'enabled': True,
                'metrics': ['success_rate', 'response_time', 'new_info_count'],
                'alert_threshold': {
                    'success_rate': 0.8,
                    'response_time': 30.0
                }
            }
        }
        
        return config
    

    

    
    def get_status(self) -> Dict:
        """获取管理器状态"""
        return {
            'ai_provider': {
                'provider': 'volcengine_coding_plan',
                'model': self.config.model,
                'performance': self.ai_provider.get_performance_metrics()
            },
            'cache_stats': {
                'user_demands_cache_size': len(self.user_demands_cache),
                'analysis_results_cache_size': len(self.analysis_results_cache),
                'total_cached_users': len(self.user_demands_cache)
            },
            'timestamp': datetime.now().isoformat()
        }

# ============================================================================
# 快速集成助手
# ============================================================================

class VolcEngineIntegrationHelper:
    """火山引擎集成助手"""
    
    @staticmethod
    def create_default_config(api_key: str) -> Dict:
        """创建默认配置"""
        return {
            "version": "1.0",
            "provider": "volcengine_coding_plan",
            "api_key": api_key,
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 2000,
            "timeout": 30,
            "max_retries": 3,
            "cache": {
                "enabled": True,
                "default_ttl": 1800
            },
            "monitoring": {
                "enabled": True,
                "log_level": "INFO"
            }
        }
    
    @staticmethod
    def generate_integration_code(api_key: str) -> str:
        """生成集成代码"""
        code = f'''# 火山引擎Coding Plan集成代码
# 生成时间: {datetime.now().isoformat()}

import os
import sys
from volcengine_ai_integration import (
    VolcEngineConfig,
    VolcEngineAIProvider,
    VolcEngineEnhancedCrawlerManager
)

# 配置火山引擎
volcengine_config = VolcEngineConfig(
    api_key="{api_key}",
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=2000,
    timeout=30
)

# 初始化AI服务
ai_provider = VolcEngineAIProvider(volcengine_config)

# 创建增强爬虫管理器
crawler_manager = VolcEngineEnhancedCrawlerManager("{api_key}")

# 示例：分析学生需求
async def analyze_student_demand_example():
    raw_demand = "我想考北京大学计算机专业的研究生"
    student_profile = {{"grade": "senior", "major": "computer science"}}
    
    analysis = await crawler_manager.analyze_student_demand(
        student_id=1001,
        raw_demand=raw_demand,
        student_profile=student_profile
    )
    
    print(f"分析结果: {{analysis}}")

# 示例：生成爬虫配置
async def generate_crawler_config_example():
    # 假设的需求分析结果
    demand_analysis = {{
        "intent": "kaoyan",
        "urgency": 4,
        "entities": {{
            "provinces": ["北京"],
            "schools": ["北京大学"],
            "majors": ["计算机"]
        }}
    }}
    
    config = await crawler_manager.generate_smart_crawler_config(
        demand_analysis,
        student_id=1001
    )
    
    print(f"爬虫配置: {{config}}")
'''
        return code

# ============================================================================
# 演示代码
# ============================================================================

async def demo_volcengine_integration():
    """演示火山引擎集成"""
    
    print("=" * 60)
    print("🔥 火山引擎Coding Plan集成演示")
    print("=" * 60)
    
    # 使用示例API密钥（实际使用时请替换）
    demo_api_key = "your_volcengine_api_key_here"
    
    print(f"\n🔐 API密钥已配置: {demo_api_key[:20]}...")
    
    # 1. 创建管理器
    print("\n1️⃣ 创建AI增强爬虫管理器...")
    manager = VolcEngineEnhancedCrawlerManager(demo_api_key)
    
    # 2. 演示需求分析
    print("\n2️⃣ 演示需求分析...")
    
    test_cases = [
        {
            "student_id": 1001,
            "demand": "我想考北京大学计算机专业的研究生，需要及时了解招生信息",
            "profile": {"grade": "senior", "target_major": "computer science"}
        },
        {
            "student_id": 1002,
            "demand": "紧急关注北京地区公务员税务局的招聘公告",
            "profile": {"province": "北京", "exam_type": "公务员"}
        }
    ]
    
    for test in test_cases:
        print(f"\n📝 分析学生{test['student_id']}的需求: {test['demand']}")
        
        try:
            # 调用真实的AI服务
            analysis = await manager.analyze_student_demand(
                test["student_id"],
                test["demand"],
                test["profile"]
            )
            
            print(f"🎯 AI识别意图: {analysis.get('intent', 'unknown')}")
            print(f"📊 置信度: {analysis.get('confidence', 0.0):.2f}")
            print(f"🚨 紧急度: {analysis.get('urgency', 0)}/5")
            print(f"📍 实体: {analysis.get('entities', {})}")
        except Exception as e:
            print(f"❌ AI分析失败: {str(e)}")
            print("使用备用分析结果...")
            # 备用分析结果
            intent = "kaoyan" if "考研" in test["demand"] else "kaogong"
            urgency = 4 if "紧急" in test["demand"] else 2
            entities = {
                "provinces": ["北京"],
                "schools": ["北京大学"] if "北京大学" in test["demand"] else [],
                "majors": ["计算机"] if "计算机" in test["demand"] else []
            }
            print(f"🎯 识别意图: {intent}")
            print(f"🚨 紧急度: {urgency}/5")
            print(f"📍 实体: {entities}")
    
    # 3. 获取管理器状态
    print("\n3️⃣ 获取管理器状态...")
    status = manager.get_status()
    
    print(f"📊 管理器状态:")
    print(f"  AI提供商: {status['ai_provider']['provider']}")
    print(f"  模型: {status['ai_provider']['model']}")
    print(f"  缓存用户数: {status['cache_stats']['total_cached_users']}")
    
    # 4. 演示爬虫配置生成
    print("\n4️⃣ 演示爬虫配置生成...")
    
    example_analysis = {
        "intent": "kaoyan",
        "urgency": 4,
        "entities": {
            "provinces": ["北京"],
            "schools": ["北京大学"],
            "majors": ["计算机"]
        }
    }
    
    try:
        # 调用真实的爬虫配置生成
        config = await manager.generate_smart_crawler_config(
            example_analysis,
            student_id=1001
        )
        
        print(f"🛠️ 生成的爬虫配置:")
        print(f"  类型: {config.get('crawler', {}).get('type', 'unknown')}")
        print(f"  频率: {config.get('crawler', {}).get('frequency', 30)} 分钟")
        print(f"  优先级: {config.get('crawler', {}).get('priority', 'medium')}")
        print(f"  监控网站数: {len(config.get('crawler', {}).get('websites', []))}")
    except Exception as e:
        print(f"❌ 生成爬虫配置失败: {str(e)}")
        print("使用默认爬虫配置...")
        # 默认爬虫配置
        print(f"🛠️ 生成的爬虫配置:")
        print(f"  类型: kaoyan")
        print(f"  频率: 30 分钟")
        print(f"  优先级: medium")
        print(f"  监控网站数: 2")
    
    # 5. 清理
    await manager.shutdown()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成")
    print("💡 实际集成步骤：")
    print("  1. 安装依赖: pip install aiohttp")
    print("  2. 配置你的API密钥")
    print("  3. 集成到现有爬虫管理器")
    print("  4. 测试AI分析功能")
    print("=" * 60)

if __name__ == "__main__":
    # 运行演示
    asyncio.run(demo_volcengine_integration())