export default async function ReportPage({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = await params;

  // 通过 API 代理获取报告内容
  const reportUrl = `/api/report-content/${name}`;

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

        {/* Report iframe using API proxy */}
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
