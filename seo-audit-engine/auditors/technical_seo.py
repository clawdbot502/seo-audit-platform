"""
技术 SEO 审计器
"""
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient

class TechnicalSEOAuditor:
    """技术 SEO 审计器"""

    def __init__(self):
        self.llm = LLMClient()

    def audit(self, url: str, html_content: str, tech_checks: Dict) -> Dict:
        """
        执行技术 SEO 审计

        Args:
            url: 目标网址
            html_content: HTML 内容
            tech_checks: 技术初筛结果

        Returns:
            dict: 审计结果
        """
        print(f"🔧 Running Technical SEO audit...")

        system_prompt = """你是一位专业的技术 SEO 审计专家。你的任务是分析网站的技术 SEO 问题，并提供可执行的优化建议。

重点关注：
1. 爬取性和索引性（Crawlability & Indexation）
2. 页面性能和 Core Web Vitals
3. 移动端友好性
4. 结构化数据和 Schema markup
5. 安全性（HTTPS、安全头）
6. 站点架构和内部链接

请以 JSON 格式返回审计结果，包含：
- issues: 问题列表，每个问题包含 {severity, title, description, recommendation}
- score: 总体评分（0-100）
- summary: 简短总结

severity 级别：critical, high, medium, low"""

        user_prompt = f"""请审计以下网站的技术 SEO：

URL: {url}

技术检查结果：
- Robots.txt: {'存在' if tech_checks['robots_txt'].get('exists') else '不存在'}
- Sitemap: {'存在' if tech_checks['sitemap'].get('exists') else '不存在'}
- HTTPS: {'是' if tech_checks['ssl'] else '否'}
- 响应头: {tech_checks['response_headers']}

HTML 内容（前 5000 字符）:
{html_content[:5000]}

请返回 JSON 格式的审计结果。"""

        try:
            response = self.llm.call(system_prompt, user_prompt, temperature=0.3)
            # 尝试解析 JSON
            import json
            # 提取 JSON 部分（可能包含在 markdown 代码块中）
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                json_str = response.split('```')[1].split('```')[0].strip()
            else:
                json_str = response.strip()

            result = json.loads(json_str)
            print(f"✓ Technical SEO audit completed (score: {result.get('score', 'N/A')})")
            return result
        except Exception as e:
            print(f"❌ Technical SEO audit failed: {e}")
            # 返回默认结果
            return {
                'issues': [],
                'score': 0,
                'summary': f'审计失败: {str(e)}',
                'error': str(e)
            }
