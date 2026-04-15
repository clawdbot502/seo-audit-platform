"""
SEO 审计主程序
"""
import sys
import os
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawlers.html_fetcher import fetch_html
from crawlers.tech_checker import run_tech_checks
from auditors.technical_seo import TechnicalSEOAuditor
from auditors.content_seo import ContentSEOAuditor
from auditors.merger import merge_audits
from utils.report_generator import generate_html_report

def main(target_url: str):
    """
    主审计流程

    Args:
        target_url: 目标网址
    """
    print("=" * 60)
    print(f"🚀 SEO Audit Platform")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Target: {target_url}")
    print("=" * 60)

    try:
        # Step 1: 数据抓取 + 技术初筛
        print("\n[Step 1/5] 数据抓取和技术初筛...")
        html_content = fetch_html(target_url)
        tech_checks = run_tech_checks(target_url)

        # Step 2: 技术 SEO 审计
        print("\n[Step 2/5] 技术 SEO 审计...")
        tech_auditor = TechnicalSEOAuditor()
        tech_results = tech_auditor.audit(target_url, html_content, tech_checks)

        # Step 3: 内容 SEO 审计
        print("\n[Step 3/5] 内容 SEO 审计...")
        content_auditor = ContentSEOAuditor()
        content_results = content_auditor.audit(target_url, html_content)

        # Step 4: 合并审计结果
        print("\n[Step 4/5] 合并审计结果...")
        merged_report = merge_audits(tech_results, content_results)

        # Step 5: 生成 HTML 报告
        print("\n[Step 5/5] 生成 HTML 报告...")
        report_path = generate_html_report(target_url, merged_report)

        print("\n" + "=" * 60)
        print(f"✅ 审计完成！")
        print(f"📊 总体评分: {merged_report['overall_score']}/100")
        print(f"📝 发现问题: {merged_report['total_issues']} 个")
        print(f"📄 报告路径: {report_path}")
        print("=" * 60)

        return report_path

    except Exception as e:
        print(f"\n❌ 审计失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python main.py <target_url>")
        print("示例: python main.py https://example.com")
        sys.exit(1)

    target_url = sys.argv[1]
    main(target_url)
