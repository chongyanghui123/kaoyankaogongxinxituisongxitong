import asyncio
import random
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
import ua_generator

logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """爬虫基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = None
        self.headers = {
            'User-Agent': ua_generator.generate(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.proxies = config.get('proxies', [])
        self.timeout = config.get('timeout', 30)
        self.retry_times = config.get('retry_times', 3)
    
    async def __aenter__(self):
        """进入上下文管理器"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        await self.close()
    
    async def initialize(self):
        """初始化爬虫"""
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
    
    async def close(self):
        """关闭爬虫"""
        if self.session:
            await self.session.close()
    
    async def fetch(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """获取页面内容"""
        for retry in range(self.retry_times):
            try:
                # 随机延迟，防止被反爬
                await asyncio.sleep(random.uniform(0.5, 2.0))
                
                # 随机选择代理
                proxy = random.choice(self.proxies) if self.proxies else None
                
                async with self.session.get(
                    url, 
                    params=params, 
                    proxy=proxy,
                    headers=self._get_random_headers(),
                    ssl=False  # 跳过SSL验证
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 429:
                        # 被限流，等待后重试
                        logger.warning(f"被限流，等待后重试: {url}")
                        await asyncio.sleep(random.uniform(5, 10))
                        continue
                    else:
                        logger.error(f"请求失败: {url}, 状态码: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"获取页面失败: {url}, 错误: {str(e)}")
                if retry < self.retry_times - 1:
                    await asyncio.sleep(random.uniform(1, 3))
                    continue
                return None
    
    def _get_random_headers(self) -> Dict[str, str]:
        """获取随机 headers"""
        headers = self.headers.copy()
        # 直接使用字符串形式的 User-Agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        headers['User-Agent'] = random.choice(user_agents)
        # 随机添加一些其他 headers
        if random.random() > 0.5:
            headers['Referer'] = 'https://www.baidu.com'
        if random.random() > 0.5:
            headers['Cache-Control'] = 'max-age=0'
        return headers
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """解析 HTML"""
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    async def crawl(self) -> List[Dict[str, Any]]:
        """爬取数据"""
        pass
    
    async def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理爬取的数据"""
        return data
    
    async def run(self) -> List[Dict[str, Any]]:
        """运行爬虫"""
        start_time = time.time()
        logger.info(f"开始爬取: {self.__class__.__name__}")
        
        try:
            if not self.session:
                await self.initialize()
            
            data = await self.crawl()
            processed_data = await self.process_data(data)
            
            end_time = time.time()
            logger.info(f"爬取完成: {self.__class__.__name__}, 耗时: {end_time - start_time:.2f}秒, 爬取数量: {len(processed_data)}")
            
            return processed_data
        except Exception as e:
            logger.error(f"爬虫运行失败: {str(e)}")
            return []
