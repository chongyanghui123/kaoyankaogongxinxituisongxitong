import logging
from typing import List, Dict, Any
from datetime import datetime
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class KaogongCrawler(BaseCrawler):
    """考公信息爬虫"""
    
    async def crawl(self) -> List[Dict[str, Any]]:
        """爬取考公信息"""
        url = self.config.get('url', 'https://www.scs.gov.cn/')
        html = await self.fetch(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        info_list = []
        
        # 这里根据实际网站结构进行解析
        # 示例：解析国家公务员局网站的通知公告
        try:
            # 查找通知公告区域
            selector = self.config.get('selector', '.notice-list')
            notice_list = soup.select(selector)
            for notice in notice_list:
                # 查找标题和链接
                parse_rules = self.config.get('parse_rules', {})
                title_elem = notice.select_one(parse_rules.get('title', 'a.title'))
                link_elem = notice.select_one(parse_rules.get('link', 'a'))
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    link = link_elem.get('href')
                    if not link.startswith('http'):
                        link = url + link if not url.endswith('/') else url + link[1:]
                    
                    # 查找发布日期
                    date_elem = notice.select_one(parse_rules.get('time', '.publish-date'))
                    publish_date = date_elem.text.strip() if date_elem else datetime.now().strftime('%Y-%m-%d')
                    
                    # 构建信息字典
                    info = {
                        'title': title,
                        'url': link,
                        'source': '国家公务员局',
                        'publish_date': publish_date,
                        'province': '全国',
                        'position_type': '公务员',
                        'major': '全部',
                        'education': '不限',
                        'category': '考试公告',
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
        except Exception as e:
            logger.error(f"解析考公信息失败: {str(e)}")
        
        return info_list
    
    async def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理考公信息"""
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
            if '招考公告' in title or '招聘公告' in title:
                item['category'] = '招考公告'
            elif '职位表' in title or '岗位表' in title:
                item['category'] = '职位表'
            elif '报名' in title:
                item['category'] = '报名信息'
            elif '笔试' in title:
                item['category'] = '笔试信息'
            elif '面试' in title:
                item['category'] = '面试信息'
            elif '成绩' in title or '查分' in title:
                item['category'] = '成绩查询'
            elif '体检' in title:
                item['category'] = '体检信息'
            elif '录用' in title:
                item['category'] = '录用信息'
            else:
                item['category'] = '考试公告'
            
            processed_data.append(item)
        
        return processed_data
