import logging
from typing import List, Dict, Any
from datetime import datetime
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class KaoyanCrawler(BaseCrawler):
    """考研信息爬虫"""
    
    async def crawl(self) -> List[Dict[str, Any]]:
        """爬取考研信息"""
        url = self.config.get('url', 'https://yz.chsi.com.cn/')
        html = await self.fetch(url)
        if not html:
            logger.error(f"无法获取页面: {url}")
            return []
        
        soup = self.parse_html(html)
        info_list = []
        
        # 从爬虫名称中提取省份和学校信息
        province = '全国'
        school = '教育部'
        crawler_name = self.config.get('name', '')
        if '-' in crawler_name and not crawler_name.startswith('研招网') and not crawler_name.startswith('中国教育考试网'):
            parts = crawler_name.split('-')
            if len(parts) >= 2:
                province = parts[0]
                school = '-'.join(parts[1:])
        
        # 这里根据实际网站结构进行解析
        # 示例：解析研招网的通知公告
        try:
            # 打印网站标题，确认页面获取成功
            title = soup.title.string if soup.title else '无标题'
            logger.info(f"获取页面成功: {url}, 标题: {title}")
            
            # 查找通知公告区域
            selector = self.config.get('selector', 'div.news-list')
            logger.info(f"使用选择器: {selector}")
            notice_list = soup.select(selector)
            logger.info(f"找到 {len(notice_list)} 个通知项")
            
            # 如果没有找到，尝试其他选择器
            if not notice_list:
                logger.info("尝试使用其他选择器...")
                # 尝试查找所有的a标签
                notice_list = soup.find_all('a')
                logger.info(f"找到 {len(notice_list)} 个链接")
            
            for notice in notice_list:
                # 查找标题和链接
                parse_rules = self.config.get('parse_rules', {})
                title_elem = notice.select_one(parse_rules.get('title', 'h3 a'))
                link_elem = notice.select_one(parse_rules.get('link', 'h3 a'))
                
                # 如果没有找到，尝试直接从notice中获取
                if not title_elem or not link_elem:
                    title_elem = notice
                    link_elem = notice
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    link = link_elem.get('href')
                    if not link:
                        continue
                    
                    if not link.startswith('http'):
                        link = url + link if not url.endswith('/') else url + link[1:]
                    
                    # 查找发布日期
                    date_elem = notice.select_one(parse_rules.get('time', '.time'))
                    publish_date = date_elem.text.strip() if date_elem else datetime.now().strftime('%Y-%m-%d')
                    
                    # 构建信息字典
                    info = {
                        'title': title,
                        'url': link,
                        'source': school,
                        'publish_date': publish_date,
                        'province': province,
                        'school': school,
                        'major': '全部',
                        'category': '政策通知',
                        'content': ''
                    }
                    
                    # 获取详情页内容
                    detail_html = await self.fetch(link)
                    if detail_html:
                        detail_soup = self.parse_html(detail_html)
                        content_elem = detail_soup.select_one(parse_rules.get('content', '.summary'))
                        if content_elem:
                            info['content'] = content_elem.text.strip()
                    
                    info_list.append(info)
                    logger.info(f"添加信息: {title}")
        except Exception as e:
            logger.error(f"解析考研信息失败: {str(e)}")
        
        logger.info(f"爬取完成，共获取 {len(info_list)} 条信息")
        return info_list
    
    async def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理考研信息"""
        processed_data = []
        for item in data:
            # 标准化发布日期
            try:
                if isinstance(item['publish_date'], str):
                    # 尝试解析日期格式
                    for fmt in ['%Y-%m-%d', '%Y年%m月%d日', '%Y/%m/%d']:
                        try:
                            item['publish_date'] = datetime.strptime(item['publish_date'], fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        item['publish_date'] = datetime.now()
            except Exception as e:
                logger.error(f"处理日期失败: {str(e)}")
                item['publish_date'] = datetime.now()
            
            # 分类处理
            title = item['title'].lower()
            if '招生简章' in title or '招生章程' in title:
                item['category'] = '招生简章'
            elif '分数线' in title or '国家线' in title:
                item['category'] = '分数线'
            elif '复试' in title or '面试' in title:
                item['category'] = '复试信息'
            elif '调剂' in title:
                item['category'] = '调剂信息'
            elif '报名' in title or '网报' in title:
                item['category'] = '报名信息'
            elif '准考证' in title:
                item['category'] = '准考证'
            elif '成绩' in title or '查分' in title:
                item['category'] = '成绩查询'
            else:
                item['category'] = '政策通知'
            
            processed_data.append(item)
        
        return processed_data
