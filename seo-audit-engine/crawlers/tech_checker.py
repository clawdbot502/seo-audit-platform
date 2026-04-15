"""
技术 SEO 初筛检查
"""
import requests
from urllib.parse import urlparse
from typing import Dict

def run_tech_checks(url: str) -> Dict:
    """
    运行技术 SEO 快速初筛

    Args:
        url: 目标网址

    Returns:
        dict: 技术检查结果
    """
    print(f"🔍 Running technical SEO checks for: {url}")

    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    results = {
        'robots_txt': check_robots_txt(base_url),
        'sitemap': check_sitemap(base_url),
        'response_headers': check_response_headers(url),
        'ssl': parsed.scheme == 'https'
    }

    print(f"✓ Technical checks completed")
    return results

def check_robots_txt(base_url: str) -> Dict:
    """检查 robots.txt"""
    robots_url = f"{base_url}/robots.txt"
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            return {
                'exists': True,
                'content': response.text[:500],  # 只保存前 500 字符
                'status_code': 200
            }
        else:
            return {
                'exists': False,
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'exists': False,
            'error': str(e)
        }

def check_sitemap(base_url: str) -> Dict:
    """检查 sitemap.xml"""
    sitemap_url = f"{base_url}/sitemap.xml"
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            # 简单统计 URL 数量
            url_count = response.text.count('<url>')
            return {
                'exists': True,
                'url_count': url_count,
                'status_code': 200
            }
        else:
            return {
                'exists': False,
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'exists': False,
            'error': str(e)
        }

def check_response_headers(url: str) -> Dict:
    """检查响应头"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        headers = response.headers

        return {
            'cache_control': headers.get('Cache-Control', ''),
            'content_type': headers.get('Content-Type', ''),
            'x_frame_options': headers.get('X-Frame-Options', ''),
            'strict_transport_security': headers.get('Strict-Transport-Security', ''),
            'server': headers.get('Server', ''),
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'error': str(e)
        }
