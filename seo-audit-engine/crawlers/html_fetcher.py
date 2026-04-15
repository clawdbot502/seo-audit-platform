"""
HTML 抓取器
"""
import requests
from typing import Optional
from bs4 import BeautifulSoup

def fetch_html(url: str, timeout: int = 30) -> str:
    """
    抓取网页 HTML 内容

    Args:
        url: 目标网址
        timeout: 超时时间（秒）

    Returns:
        str: HTML 内容

    Raises:
        requests.RequestException: 请求失败
    """
    print(f"📥 Fetching HTML from: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        print(f"✓ HTML fetched successfully ({len(response.text)} bytes)")
        return response.text
    except requests.RequestException as e:
        print(f"❌ Failed to fetch HTML: {e}")
        raise

def extract_text_content(html: str) -> str:
    """
    从 HTML 中提取纯文本内容

    Args:
        html: HTML 内容

    Returns:
        str: 提取的文本
    """
    soup = BeautifulSoup(html, 'lxml')

    # 移除 script 和 style 标签
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator='\n', strip=True)
    return text

def extract_metadata(html: str) -> dict:
    """
    提取页面元数据

    Args:
        html: HTML 内容

    Returns:
        dict: 元数据字典
    """
    soup = BeautifulSoup(html, 'lxml')

    metadata = {
        'title': '',
        'description': '',
        'h1': [],
        'h2': [],
        'canonical': '',
        'lang': '',
        'og_title': '',
        'og_description': '',
        'og_image': ''
    }

    # Title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text(strip=True)

    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        metadata['description'] = meta_desc.get('content', '')

    # Headings
    metadata['h1'] = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
    metadata['h2'] = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]

    # Canonical
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        metadata['canonical'] = canonical.get('href', '')

    # Lang
    html_tag = soup.find('html')
    if html_tag:
        metadata['lang'] = html_tag.get('lang', '')

    # Open Graph
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        metadata['og_title'] = og_title.get('content', '')

    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc:
        metadata['og_description'] = og_desc.get('content', '')

    og_img = soup.find('meta', attrs={'property': 'og:image'})
    if og_img:
        metadata['og_image'] = og_img.get('content', '')

    return metadata
