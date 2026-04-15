export default async function ReportPage({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = await params;

  // 构建报告的原始 URL（从 GitHub 仓库获取）
  const repoOwner = process.env.REPO_OWNER || 'clawdbot502';
  const repoName = process.env.REPO_NAME || 'seo-audit-platform';
  const reportUrl = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/main/seo-audit-engine/reports/${name}`;

  return (
    <div className="min-h-screen bg-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-6">
          <a
            href="/"
            className="inline-flex items-center text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            ← 返回首页
          </a>
          <h1 className="text-2xl font-bold text-slate-100 mt-4">
            {decodeURIComponent(name)}
          </h1>
        </div>

        {/* Report iframe */}
        <div className="bg-white rounded-lg shadow-2xl overflow-hidden">
          <iframe
            src={reportUrl}
            className="w-full h-screen border-0"
            title="SEO Audit Report"
          />
        </div>
      </div>
    </div>
  );
}
