"""
HTML 报告生成器
"""
from typing import Dict
from datetime import datetime
from urllib.parse import urlparse
import os

def generate_html_report(url: str, audit_data: Dict) -> str:
    """
    生成 HTML 审计报告

    Args:
        url: 目标网址
        audit_data: 合并后的审计数据

    Returns:
        str: 报告文件路径
    """
    print(f"📄 Generating HTML report...")

    # 生成报告文件名
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"seo-audit-{domain}-{timestamp}.html"
    filepath = os.path.join('..', 'reports', filename)

    # 确保 reports 目录存在（仓库根目录的 reports/）
    os.makedirs(os.path.join('..', 'reports'), exist_ok=True)

    # 生成 HTML 内容
    html_content = generate_html_template(url, audit_data)

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Report saved to: {filepath}")
    return filepath

def generate_html_template(url: str, data: Dict) -> str:
    """生成 HTML 模板"""

    issues_html = ""
    for issue in data.get('issues', []):
        severity = issue.get('severity', 'low')
        category = issue.get('category', 'general')
        title = issue.get('title', 'Unknown Issue')
        description = issue.get('description', '')
        recommendation = issue.get('recommendation', '')

        issues_html += f"""
        <div class="issue-card {severity}">
            <div class="issue-header">
                <div class="issue-title">{title}</div>
                <div class="badges">
                    <span class="badge badge-priority {severity}">{severity.upper()}</span>
                    <span class="badge badge-category">{category.upper()}</span>
                </div>
            </div>
            <div class="issue-section">
                <h4>问题描述</h4>
                <p>{description}</p>
            </div>
            <div class="issue-section">
                <h4>优化建议</h4>
                <p>{recommendation}</p>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO 审计报告 - {url}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            padding: 24px;
            line-height: 1.6;
            min-height: 100vh;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        header {{
            background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
            padding: 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
        h1 {{
            font-size: 2.2em;
            margin-bottom: 8px;
            background: linear-gradient(45deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        h2 {{ color: #38bdf8; margin-bottom: 12px; font-size: 1.4em; }}
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .meta-card {{
            background: rgba(255,255,255,0.05);
            padding: 14px;
            border-radius: 8px;
            border-left: 4px solid #38bdf8;
        }}
        .summary {{
            background: rgba(30, 41, 59, 0.7);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.05);
            padding: 18px 12px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{ font-size: 2.2em; font-weight: bold; color: #38bdf8; }}
        .score-card {{
            background: rgba(30, 41, 59, 0.7);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            text-align: center;
        }}
        .score-number {{
            font-size: 4em;
            font-weight: bold;
            background: linear-gradient(45deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .issue-card {{
            background: rgba(30, 41, 59, 0.7);
            padding: 22px;
            border-radius: 12px;
            margin-bottom: 18px;
            border-left: 5px solid;
        }}
        .issue-card.critical {{ border-left-color: #f87171; }}
        .issue-card.high {{ border-left-color: #fbbf24; }}
        .issue-card.medium {{ border-left-color: #facc15; }}
        .issue-card.low {{ border-left-color: #60a5fa; }}
        .issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 12px;
        }}
        .issue-title {{ font-size: 1.2em; flex: 1; color: #f8fafc; }}
        .badges {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .badge {{
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 0.8em;
            font-weight: 600;
        }}
        .badge-priority {{ background: #f87171; color: #fff; }}
        .badge-priority.high {{ background: #fbbf24; color: #0f172a; }}
        .badge-priority.medium {{ background: #facc15; color: #0f172a; }}
        .badge-priority.low {{ background: #60a5fa; color: #fff; }}
        .badge-category {{ background: rgba(255,255,255,0.1); color: #e2e8f0; border: 1px solid rgba(255,255,255,0.15); }}
        .issue-section {{ margin: 14px 0; }}
        .issue-section h4 {{ color: #38bdf8; margin-bottom: 6px; font-size: 0.95em; text-transform: uppercase; letter-spacing: 0.3px; }}
        .issue-section p {{ color: #cbd5e1; line-height: 1.7; }}
        footer {{
            text-align: center;
            margin-top: 40px;
            opacity: 0.5;
            font-size: 0.85em;
            padding: 16px;
        }}
        @media (max-width: 640px) {{
            h1 {{ font-size: 1.6em; }}
            .issue-header {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SEO 审计报告</h1>
            <p style="opacity:0.8">自动化 SEO 审计平台</p>
            <div class="meta-info">
                <div class="meta-card"><strong>URL:</strong><br>{url}</div>
                <div class="meta-card"><strong>审计时间:</strong><br>{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div class="meta-card"><strong>发现问题:</strong><br>{data.get('total_issues', 0)}</div>
                <div class="meta-card"><strong>总体评分:</strong><br>{data.get('overall_score', 0)}/100</div>
            </div>
        </header>

        <div class="score-card">
            <h2>总体评分</h2>
            <div class="score-number">{data.get('overall_score', 0)}</div>
            <p style="opacity:0.8; margin-top:8px">技术 SEO: {data.get('tech_score', 0)}/100 | 内容 SEO: {data.get('content_score', 0)}/100</p>
        </div>

        <div class="summary">
            <h2>问题统计</h2>
            <div class="stats-grid">
                <div class="stat-box"><div class="stat-number" style="color:#f87171">{data.get('issue_counts', {}).get('critical', 0)}</div><div>Critical</div></div>
                <div class="stat-box"><div class="stat-number" style="color:#fbbf24">{data.get('issue_counts', {}).get('high', 0)}</div><div>High</div></div>
                <div class="stat-box"><div class="stat-number" style="color:#facc15">{data.get('issue_counts', {}).get('medium', 0)}</div><div>Medium</div></div>
                <div class="stat-box"><div class="stat-number" style="color:#60a5fa">{data.get('issue_counts', {}).get('low', 0)}</div><div>Low</div></div>
            </div>
        </div>

        <h2 style="margin: 24px 0 16px 0;">发现的问题</h2>
        {issues_html}

        <footer>
            <p>由 SEO 审计平台自动生成 | Powered by AI</p>
        </footer>
    </div>
</body>
</html>"""

    return html
