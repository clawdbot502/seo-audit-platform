import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // 获取环境变量
    const githubToken = process.env.GITHUB_TOKEN;
    const repoOwner = process.env.REPO_OWNER || 'clawdbot502';
    const repoName = process.env.REPO_NAME || 'seo-audit-platform';

    if (!githubToken) {
      return NextResponse.json(
        { error: '未配置 GITHUB_TOKEN' },
        { status: 500 }
      );
    }

    // 获取 reports 目录内容
    const response = await fetch(
      `https://api.github.com/repos/${repoOwner}/${repoName}/contents/seo-audit-engine/reports`,
      {
        headers: {
          'Authorization': `Bearer ${githubToken}`,
          'Accept': 'application/vnd.github+json',
        },
        cache: 'no-store',
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        // reports 目录不存在，返回空列表
        return NextResponse.json({ reports: [] });
      }
      return NextResponse.json(
        { error: `GitHub API 调用失败: ${response.status}` },
        { status: response.status }
      );
    }

    const files = await response.json();

    // 过滤 HTML 文件并解析信息
    const reports = files
      .filter((file: any) => file.name.endsWith('.html'))
      .map((file: any) => {
        // 解析文件名：seo-audit-{domain}-{timestamp}.html
        const match = file.name.match(/seo-audit-(.+)-(\d{8}-\d{6})\.html/);

        let url = '';
        let timestamp = '';

        if (match) {
          url = match[1];
          const dateStr = match[2];
          // 格式化时间戳：20260415-123456 -> 2026-04-15 12:34:56
          timestamp = `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)} ${dateStr.slice(9, 11)}:${dateStr.slice(11, 13)}:${dateStr.slice(13, 15)}`;
        }

        return {
          name: file.name,
          path: file.path,
          url: url || file.name,
          timestamp: timestamp || '未知时间',
        };
      })
      .sort((a: any, b: any) => b.timestamp.localeCompare(a.timestamp)); // 按时间倒序

    return NextResponse.json({ reports });

  } catch (error) {
    console.error('Fetch reports error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}
