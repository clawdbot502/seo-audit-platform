import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { url } = await request.json();

    if (!url) {
      return NextResponse.json(
        { error: '缺少 URL 参数' },
        { status: 400 }
      );
    }

    // 验证 URL 格式
    try {
      new URL(url);
    } catch {
      return NextResponse.json(
        { error: '无效的 URL 格式' },
        { status: 400 }
      );
    }

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

    // 触发 GitHub Actions workflow
    const response = await fetch(
      `https://api.github.com/repos/${repoOwner}/${repoName}/actions/workflows/seo-audit.yml/dispatches`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${githubToken}`,
          'Accept': 'application/vnd.github+json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ref: 'main',
          inputs: {
            target_url: url,
          },
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error('GitHub API error:', errorText);
      return NextResponse.json(
        { error: `GitHub API 调用失败: ${response.status}` },
        { status: response.status }
      );
    }

    return NextResponse.json({
      success: true,
      message: '审计任务已启动',
      runId: 'pending',
    });

  } catch (error) {
    console.error('Trigger audit error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}
