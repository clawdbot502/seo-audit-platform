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
    const reportsMap = new Map<string, any[]>();

    files
      .filter((file: any) => file.name.endsWith('.html'))
      .forEach((file: any) => {
        // 解析文件名：seo-audit-{domain}-{timestamp}.html
        const match = file.name.match(/seo-audit-(.+)-(\d{8}-\d{6})\.html/);

        if (match) {
          const urlPart = match[1];
          const dateStr = match[2];
          
          // 格式化时间戳：20260415-123456 -> 2026-04-15 12:34:56 (UTC)
          const year = dateStr.slice(0, 4);
          const month = dateStr.slice(4, 6);
          const day = dateStr.slice(6, 8);
          const hour = dateStr.slice(9, 11);
          const minute = dateStr.slice(11, 13);
          const second = dateStr.slice(13, 15);
          
          // 创建 UTC 时间并转换为上海时间 (UTC+8)
          const utcDate = new Date(`${year}-${month}-${day}T${hour}:${minute}:${second}Z`);
          const shanghaiDate = new Date(utcDate.getTime() + 8 * 60 * 60 * 1000);
          
          const timestamp = shanghaiDate.toISOString().slice(0, 19).replace('T', ' ');

          // 按 URL 分组
          if (!reportsMap.has(urlPart)) {
            reportsMap.set(urlPart, []);
          }

          reportsMap.get(urlPart)!.push({
            name: file.name,
            path: file.path,
            urlPart,
            timestamp,
            sortKey: dateStr,
          });
        }
      });

    // 为每个 URL 的报告添加版本号
    const reports: any[] = [];
    
    reportsMap.forEach((urlReports, urlPart) => {
      // 按时间倒序排序
      urlReports.sort((a, b) => b.sortKey.localeCompare(a.sortKey));
      
      // 添加版本号
      urlReports.forEach((report, index) => {
        const version = urlReports.length > 1 ? ` V${urlReports.length - index}` : '';
        reports.push({
          name: report.name,
          path: report.path,
          url: urlPart + version,
          timestamp: report.timestamp,
          sortKey: report.sortKey,
        });
      });
    });

    // 全局按时间倒序排序
    reports.sort((a, b) => b.sortKey.localeCompare(a.sortKey));

    return NextResponse.json({ reports });

  } catch (error) {
    console.error('Fetch reports error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}
