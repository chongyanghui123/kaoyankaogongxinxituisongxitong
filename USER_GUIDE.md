# 🎯 考研考公双赛道情报监控系统使用指南

## 📋 系统概述

### 🔥 火山引擎AI增强特性
- **🤖 智能需求分析**：使用AI理解学生需求，提取关键信息
- **🎯 个性化网站匹配**：根据需求智能推荐最适合的监控网站
- **⚡ 动态频率调整**：根据紧急度自动调整爬虫监控频率
- **🔄 自动降级**：AI服务不可用时自动使用备用方案
- **📊 性能监控**：实时监控AI性能和系统状态

### 🏗️ 系统架构
1. **用户需求层** - 收集学生个性化需求
2. **AI分析层** - 火山引擎AI智能分析需求
3. **爬虫调度层** - 智能调度个性化爬虫
4. **数据存储层** - 存储分析结果和监控数据
5. **通知推送层** - 个性化信息推送

## 🚀 快速开始

### 第一步：配置API密钥

```bash
# 编辑配置文件
nano config/volcengine_config.yaml

# 找到这一行
key: "your_volcengine_api_key_here"

# 替换为你的真实API密钥
key: "sk-1234567890abcdef"
```

### 第二步：启动系统

```bash
# 启动AI增强版本
python start_optimized_system.py

# 查看启动日志
tail -f logs/optimized_start.log
```

### 第三步：添加用户需求

```python
# 示例：添加学生需求
from backend.core.database import get_db
from models.users import User, UserSubscription, UserKeyword

# 1. 创建用户（如果不存在）
db = next(get_db(database="common"))
user = User(name="张三", email="zhangsan@example.com")
db.add(user)
db.commit()

# 2. 订阅监控服务
subscription = UserSubscription(
    user_id=user.id,
    config_json={
        "kaoyan": {
            "provinces": ["北京"],
            "schools": ["北京大学"],
            "majors": ["计算机"],
            "keywords": ["研究生招生", "录取分数线"]
        }
    },
    status=1
)
db.add(subscription)

# 3. 添加关键词
keyword = UserKeyword(
    user_id=user.id,
    keyword="人工智能",
    category=1,  # 1=考研，2=考公
    is_active=True
)
db.add(keyword)

db.commit()
```

### 第四步：监控系统状态

```bash
# 查看AI服务状态
python -c "
from backend.core.crawler_manager import get_volcengine_status
status = get_volcengine_status()
print(f'🔥 AI状态: {\"已启用\" if status.get(\"enabled\") else \"未启用\"}')
print(f'🤖 模型: {status.get(\"model\", \"unknown\")}')
if status.get(\"enabled\"):
    perf = status.get(\"performance\", {})
    print(f'📊 请求数: {perf.get(\"request_count\", 0)}')
    print(f'✅ 成功率: {perf.get(\"success_rate\", 0):.2%}')
    print(f'⏱️  平均响应: {perf.get(\"avg_response_time\", 0):.2f}秒')
"</script>
```



## 🎯 核心功能

### 1. 智能需求分析

```python
from backend.core.crawler_manager import SmartDemandAnalyzer

# 分析学生需求
async def analyze_student_demand():
    raw_demand = "我想考北京大学计算机专业的研究生，需要及时了解招生信息"
    student_context = {
        "grade": "senior",
        "province": "北京",
        "target_major": "计算机"
    }
    
    analysis = await SmartDemandAnalyzer.analyze_demand(
        raw_demand, student_context
    )
    
    print(f"🎯 意图: {analysis['category']}")
    print(f"🚨 紧急度: {analysis['urgency']}/5")
    print(f"📍 实体: {analysis}")
```

### 2. 智能网站匹配

```python
from backend.core.crawler_manager import SmartWebsiteMatcher


# 匹配最适合的网站
def match_websites_for_student():
    demand_analysis = {
        'category': 'kaoyan',
        'urgency': 4,
        'provinces': ['北京'],
        'schools': ['北京大学'],
        'majors': ['计算机']
    }
    
    websites = SmartWebsiteMatcher.match_websites(demand_analysis)
    
    for website in websites:
        print(f"🌐 推荐网站: {website['name']}")
        print(f"  监控频率: {website['interval']}分钟")
        print(f"  优先级: {website['priority']}")
        print(f"  匹配度: {website.get('match_score', 0):.2f}")
```

### 3. 个性化爬虫生成

```python
from backend.core.crawler_manager import SmartCrawlerGenerator


# 生成个性化爬虫配置
async def generate_personalized_crawler():
    demand_analysis = {
        'category': 'kaoyan',
        'urgency': 4,
        'provinces': ['北京'],
        'schools': ['北京大学'],
        'majors': ['计算机']
    }
    
    config = await SmartCrawlerGenerator.generate_crawler_config(
        demand_analysis,
        user_id=1001
    )
    
    print(f"🛠️ 爬虫名称: {config.get('name')}")
    print(f"⏰ 监控频率: {config.get('interval', 30)}分钟")
    print(f"🏆 优先级: {config.get('priority', 'medium')}")
    print(f"⏱️  超时时间: {config.get('timeout', 20)}秒")
    print(f"🔄 重试次数: {config.get('retry_times', 3)}")
    print(f"🌐 监控网站: {[w['name'] for w in config.get('websites', [])]}")
```

### 4. 智能任务调度

```python
from backend.core.crawler_manager import start_crawler_scheduler


# 启动智能调度
def start_smart_scheduling():
    print("🚀 启动AI增强爬虫调度...")
    start_crawler_scheduler()
    
    print("✅ 调度器已启动")
    print("📊 系统将根据以下策略进行调度:")
    print("  - 紧急任务（urgency>0.7）: 5分钟间隔，高优先级")
    print("  - 重要任务（urgency>0.4）: 15分钟间隔，中优先级")
    print("  - 普通任务: 30分钟间隔，低优先级")
```

## 📊 系统监控

### 查看系统状态

```bash
# 查看整体状态
python -c "
import sys
sys.path.append('.')
from backend.core.crawler_manager import get_volcengine_status
status = get_volcengine_status()
print('🔥 火山引擎AI状态:')
print(f'   启用状态: {status.get(\"enabled\", False)}')
print(f'   运行状态: {status.get(\"status\", \"unknown\")}')
if status.get(\"enabled\"):
    print(f'   模型版本: {status.get(\"model\", \"unknown\")}')
    print(f'   性能数据:')
    print(f'      请求总数: {status.get(\"performance\", {}).get(\"request_count\", 0)}')
    print(f'      成功率: {status.get(\"performance\", {}).get(\"success_rate\", 0):.2%}')
    print(f'      平均响应时间: {status.get(\"performance\", {}).get(\"avg_response_time\", 0):.2f}秒')
"</script>
```

### 查看监控日志

```bash
# 查看AI分析日志
tail -f logs/crawler_manager.log | grep -E "(AI|火山引擎|analysis)"

# 查看爬虫运行日志
tail -f logs/crawler_manager.log | grep -E "(开始运行|运行完成)"

# 查看系统错误日志
tail -f logs/crawler_manager.log | grep -E "(失败|错误|❌)"
```

### 查看数据统计

```bash
# 查看爬虫配置统计
python -c "
from backend.core.database import get_db
from models.kaoyan import KaoyanCrawlerConfig
from models.kaogong import KaogongCrawlerConfig

# 考研爬虫配置统计
db = next(get_db(database=\"kaoyan\"))
count_kaoyan = db.query(KaoyanCrawlerConfig).count()
print(f'考研爬虫配置数: {count_kaoyan}')

# 考公爬虫配置统计
db = next(get_db(database=\"kaogong\"))
count_kaogong = db.query(KaogongCrawlerConfig).count()
print(f'考公爬虫配置数: {count_kaogong}')
"
```

## ⚙️ 配置选项

### 核心配置

```yaml
# config/volcengine_config.yaml

version: "1.0"
provider: "volcengine_coding_plan"

api:
  key: "your_api_key_here"          # 必须替换为真实密钥
  model: "deepseek-chat"            # 模型选择
  temperature: 0.7                   # 创造力 (0-1)
  max_tokens: 2000                  # 响应最大长度
  timeout: 30                       # 超时时间(秒)

scheduling:
  # 紧急任务配置 (urgency > 0.7)
  high_priority:
    frequency: 5                     # 5分钟间隔
    timeout: 30                     # 30秒超时
    retry_times: 5                   # 重试5次
  
  # 重要任务配置 (urgency > 0.4)
  medium_priority:
    frequency: 15                    # 15分钟间隔
    timeout: 20                     # 20秒超时
    retry_times: 3                   # 重试3次
  
  # 普通任务配置
  low_priority:
    frequency: 30                   # 30分钟间隔
    timeout: 15                     # 15秒超时
    retry_times: 2                   # 重试2次

cache:
  enabled: true                     # 启用缓存
  default_ttl: 1800                 # 缓存30分钟
  max_size: 1000                    # 最大缓存条目数

monitoring:
  enabled: true                     # 启用监控
  log_level: "INFO"                 # 日志级别
  alerting: true                    # 启用告警
```

### 性能调优

```yaml
# 爬虫并发配置
concurrency:
  max_workers: 10                    # 最大工作线程数
  max_crawlers_per_user: 5           # 每个用户最多5个爬虫
  request_rate_limit: 10             # 每分钟最多10个请求
  delay_range: [0.5, 2.0]            # 随机延迟范围(秒)

# AI优化配置
ai_optimization:
  max_retries: 3                     # AI调用最大重试次数
  fallback_enabled: true            # 启用降级策略
  cache_ttl: 3600                    # AI结果缓存1小时
  confidence_threshold: 0.6          # 置信度阈值

# 网站匹配优化
matching:
  min_match_score: 0.5               # 最小匹配度
  max_websites_per_category: 3       # 每类最多3个网站
  score_weights:                     # 得分权重
      province: 0.3
      school: 0.4
      major: 0.2
      urgency: 0.1
```

## 📈 最佳实践

### 1. 需求收集优化

```python
# 优化需求收集流程
class OptimizedDemandCollector:
    
    def __init__(self):
        self.templates = {
            'kaoyan': {
                'prompt': "请描述你的考研需求，包括：\n1. 目标省份/地区\n2. 意向学校\n3. 专业方向\n4. 紧急程度\n5. 其他具体要求",
                'examples': [
                    "我想考北京大学计算机专业的研究生，需要及时了解招生信息",
                    "关注上海交通大学软件工程专业的研究生招生动态"
                ]
            },
            'kaogong': {
                'prompt': "请描述你的考公需求，包括：\n1. 目标地区\n2. 职位类型\n3. 专业要求\n4. 紧急程度\n5. 其他具体要求",
                'examples': [
                    "关注北京地区公务员税务局的招聘公告",
                    "紧急需要上海地区事业单位招聘信息"
                ]
            }
        }
    
    def collect_demand_with_guidance(self, category: str):
        template = self.templates.get(category)
        if not template:
            return "请描述你的具体需求"
        
        guidance = f"{template['prompt']}\n\n示例：\n"
        for example in template['examples']:
            guidance += f"  • {example}\n"
        
        return guidance
```

### 2. AI分析优化

```python
# 优化AI分析流程
class OptimizedAIAnalysis:
    
    async def analyze_with_context_enrichment(self, raw_demand: str, context: Dict):
        # 1. 上下文增强
        enriched_context = await self._enrich_context(context)
        
        # 2. 需求规范化
        normalized_demand = await self._normalize_demand(raw_demand, enriched_context)
        
        # 3. AI分析
        ai_analysis = await self._call_volcengine_ai(normalized_demand)
        
        # 4. 结果验证
        validated_analysis = await self._validate_analysis(ai_analysis, enriched_context)
        
        return validated_analysis
    
    async def _enrich_context(self, context: Dict) -> Dict:
        # 添加补充信息
        enriched = context.copy()
        enriched['analysis_timestamp'] = datetime.now().isoformat()
        enriched['session_id'] = f"session_{int(time.time())}"
        return enriched
```

### 3. 爬虫性能优化

```python
# 优化爬虫性能
class OptimizedCrawlerPerformance:
    
    async def run_optimized_crawlers(self, crawler_configs: List[Dict]):
        # 1. 任务分组
        grouped_tasks = await self._group_crawler_tasks(crawler_configs)
        
        # 2. 智能调度
        scheduled_tasks = await self._intelligent_scheduling(grouped_tasks)
        
        # 3. 并发执行
        results = await self._concurrent_execution(scheduled_tasks)
        
        # 4. 结果处理
        processed_results = await self._process_results(results)
        
        return processed_results
    
    async def _concurrent_execution(self, tasks: List[Dict]) -> List[Dict]:
        # 控制并发数
        semaphore = asyncio.Semaphore(5)
        
        async def run_task_with_limit(task: Dict):
            async with semaphore:
                return await self._execute_crawler(task)
        
        # 并发执行
        return await asyncio.gather(*[run_task_with_limit(task) for task in tasks])
```

## 🔧 故障排除

### 常见问题

#### 1. AI分析失败

**症状**：AI分析返回空结果或错误

**解决方法**：
```python
# 检查API密钥
import os
api_key = os.getenv('VOLCENGINE_API_KEY')
if not api_key or api_key == "your_volcengine_api_key_here":
    print("❌ 请配置API密钥")
    print("  1. 编辑 config/volcengine_config.yaml")
    print("  2. 替换 `your_volcengine_api_key_here` 为真实密钥")

# 测试连接
async def test_connection():
    try:
        # 测试请求
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ark.cn-beijing.volces.com/api/v3/chat/completions") as response:
                print(f"✅ 连接测试成功: {response.status}")
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
```

#### 2. 爬虫配置不生效

**症状**：配置了需求，但爬虫没有启动

**解决方法**：
```bash
# 检查用户订阅状态
python -c "
from backend.core.database import get_db
from models.users import UserSubscription

db = next(get_db(database=\"common\"))
active_subs = db.query(UserSubscription).filter(UserSubscription.status == 1).count()
print(f'活跃用户订阅数: {active_subs}')
"
```

#### 3. 网站匹配不准确

**症状**：推荐的网站不符合需求

**解决方法**：
```python
# 优化匹配权重
async def optimize_matching_weights(self):
    # 分析历史匹配数据
    history = await self._analyze_matching_history()
    
    # 根据历史调整权重
    optimized_weights = {
        'province': history.get('province_weight', 0.3),
        'school': history.get('school_weight', 0.4),
        'major': history.get('major_weight', 0.2),
        'urgency': history.get('urgency_weight', 0.1)
    }
    
    return optimized_weights
```

### 监控指标

#### 关键指标
1. **AI成功率**：≥ 85%
2. **AI响应时间**：≤ 2秒
3. **爬虫运行成功率**：≥ 80%
4. **信息准确率**：≥ 90%
5. **用户满意度**：≥ 85%

#### 告警阈值
- AI失败率 > 20%
- AI响应时间 > 5秒
- 爬虫成功率 < 70%
- 信息准确率 < 85%
- 用户满意度 < 80%

## 🎉 开始使用

你的考研考公双赛道情报监控系统现在已经集成了火山引擎AI！

### 快速启动命令
```bash
# 1. 配置API密钥
export VOLCENGINE_API_KEY="your_real_api_key_here"

# 2. 启动系统
python start_optimized_system.py

# 3. 监控状态
tail -f logs/optimized_start.log

# 4. 查看AI状态
python -c "
from backend.core.crawler_manager import get_volcengine_status
status = get_volcengine_status()
print(f'🚀 AI状态: {status.get(\"status\", \"unknown\")}')
"
```

**🦞 祝使用愉快！你的智能情报监控平台已经准备好为你服务！**</script>