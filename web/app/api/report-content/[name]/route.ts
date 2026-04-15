import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ name: string }> }
) {
  try {
    const { name } = await params;
    const repoOwner = process.env.REPO_OWNER || 'clawdbot502';
    const repoName = process.env.REPO_NAME || 'seo-audit-platform';
    
    // 直接从 GitHub raw 获取 HTML 内容
    const reportUrl = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/main/seo-audit-engine/reports/${name}`;
    
    const response = await fetch(reportUrl, {
      cache: 'no-store',
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: '报告不存在' },
        { status: 404 }
      );
    }

    const html = await response.text();

    // 返回 HTML 内容
    return new NextResponse(html, {
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
      },
    });

  } catch (error) {
    console.error('Fetch report error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}
