"""
内容 SEO 审计器
"""
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_client import LLMClient
from crawlers.html_fetcher import extract_metadata, extract_text_content

class ContentSEOAuditor:
    """内容 SEO 审计器"""

    def __init__(self):
        self.llm = LLMClient()

    def audit(self, url: str, html_content: str) -> Dict:
        """
        执行内容 SEO 审计

        Args:
            url: 目标网址
            html_content: HTML 内容

        Returns:
            dict: 审计结果
        """
        print(f"📝 Running Content SEO audit...")

        # 提取元数据和文本内容
        metadata = extract_metadata(html_content)
        text_content = extract_text_content(html_content)

        system_prompt = """你是一位专业的内容 SEO 和文案审计专家。你的任务是分析网站的内容质量、文案效果和 on-page SEO 优化情况。

重点关注：
1. On-Page SEO（标题、描述、H1-H6 层级、关键词优化）
2. 文案质量（清晰度、说服力、行动号召）
3. 内容结构（段落组织、可读性、信息层次）
4. 用户体验（价值主张、信任信号、导航清晰度）
5. 可访问性（alt 文本、语义化标签）
6. Open Graph 和社交媒体优化

请以 JSON 格式返回审计结果，包含：
- issues: 问题列表，每个问题包含 {severity, title, description, recommendation}
- score: 总体评分（0-100）
- summary: 简短总结

severity 级别：critical, high, medium, low"""

        user_prompt = f"""请审计以下网站的内容 SEO 和文案质量：

URL: {url}

页面元数据：
- Title: {metadata['title']}
- Description: {metadata['description']}
- H1: {metadata['h1']}
- H2 数量: {len(metadata['h2'])}
- Canonical: {metadata['canonical']}
- Lang: {metadata['lang']}
- OG Title: {metadata['og_title']}
- OG Description: {metadata['og_description']}

页面文本内容（前 3000 字符）:
{text_content[:3000]}

请返回 JSON 格式的审计结果。"""

        try:
            response = self.llm.call(system_prompt, user_prompt, temperature=0.3)
            # 尝试解析 JSON
            import json
            # 提取 JSON 部分
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                json_str = response.split('```')[1].split('```')[0].strip()
            else:
                json_str = response.strip()

            result = json.loads(json_str)
            print(f"✓ Content SEO audit completed (score: {result.get('score', 'N/A')})")
            return result
        except Exception as e:
            print(f"❌ Content SEO audit failed: {e}")
            # 返回默认结果
            return {
                'issues': [],
                'score': 0,
                'summary': f'审计失败: {str(e)}',
                'error': str(e)
            }
