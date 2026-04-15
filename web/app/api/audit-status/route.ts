import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const githubToken = process.env.GITHUB_TOKEN;
    const repoOwner = process.env.REPO_OWNER || 'clawdbot502';
    const repoName = process.env.REPO_NAME || 'seo-audit-platform';

    if (!githubToken) {
      return NextResponse.json(
        { error: '未配置 GITHUB_TOKEN' },
        { status: 500 }
      );
    }

    // 获取最近的 workflow 运行记录
    const response = await fetch(
      `https://api.github.com/repos/${repoOwner}/${repoName}/actions/workflows/seo-audit.yml/runs?per_page=1`,
      {
        headers: {
          'Authorization': `Bearer ${githubToken}`,
          'Accept': 'application/vnd.github+json',
        },
        cache: 'no-store',
      }
    );

    if (!response.ok) {
      return NextResponse.json(
        { error: `GitHub API 调用失败: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    const latestRun = data.workflow_runs?.[0];

    if (!latestRun) {
      return NextResponse.json({
        isRunning: false,
        status: 'idle',
      });
    }

    const isRunning = latestRun.status === 'in_progress' || latestRun.status === 'queued';

    return NextResponse.json({
      isRunning,
      status: latestRun.status,
      conclusion: latestRun.conclusion,
      runId: latestRun.id,
      createdAt: latestRun.created_at,
      updatedAt: latestRun.updated_at,
    });

  } catch (error) {
    console.error('Check audit status error:', error);
    return NextResponse.json(
      { error: '服务器错误' },
      { status: 500 }
    );
  }
}
