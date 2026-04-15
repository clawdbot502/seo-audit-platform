"""
审计结果合并器
"""
from typing import Dict, List

def merge_audits(tech_results: Dict, content_results: Dict) -> Dict:
    """
    合并技术 SEO 和内容 SEO 审计结果

    Args:
        tech_results: 技术 SEO 审计结果
        content_results: 内容 SEO 审计结果

    Returns:
        dict: 合并后的审计结果
    """
    print(f"🔀 Merging audit results...")

    # 合并问题列表
    all_issues = []

    # 添加技术 SEO 问题
    for issue in tech_results.get('issues', []):
        issue['category'] = 'technical'
        all_issues.append(issue)

    # 添加内容 SEO 问题
    for issue in content_results.get('issues', []):
        issue['category'] = 'content'
        all_issues.append(issue)

    # 按严重程度排序
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 3))

    # 计算总体评分（加权平均）
    tech_score = tech_results.get('score', 0)
    content_score = content_results.get('score', 0)
    overall_score = int((tech_score * 0.5 + content_score * 0.5))

    # 统计问题数量
    issue_counts = {
        'critical': sum(1 for i in all_issues if i.get('severity') == 'critical'),
        'high': sum(1 for i in all_issues if i.get('severity') == 'high'),
        'medium': sum(1 for i in all_issues if i.get('severity') == 'medium'),
        'low': sum(1 for i in all_issues if i.get('severity') == 'low')
    }

    merged_result = {
        'overall_score': overall_score,
        'tech_score': tech_score,
        'content_score': content_score,
        'total_issues': len(all_issues),
        'issue_counts': issue_counts,
        'issues': all_issues,
        'tech_summary': tech_results.get('summary', ''),
        'content_summary': content_results.get('summary', '')
    }

    print(f"✓ Merge completed: {len(all_issues)} total issues, score: {overall_score}/100")
    return merged_result
