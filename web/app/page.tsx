import AuditForm from './components/AuditForm';
import ReportList from './components/ReportList';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
            SEO Audit Platform
          </h1>
          <p className="text-slate-300 text-lg">
            AI 驱动的自动化 SEO 审计 - 支持多模型分析
          </p>
        </header>

        {/* Audit Form */}
        <section className="mb-12">
          <AuditForm />
        </section>

        {/* Report List */}
        <section>
          <ReportList />
        </section>
      </div>
    </div>
  );
}
