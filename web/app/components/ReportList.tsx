'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

interface Report {
  name: string;
  path: string;
  url: string;
  timestamp: string;
}

export default function ReportList() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch('/api/reports');
      const data = await response.json();
      setReports(data.reports || []);
    } catch (error) {
      console.error('Failed to fetch reports:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700">
        <h2 className="text-2xl font-semibold text-cyan-400 mb-6">历史报告</h2>
        <div className="text-center text-slate-400 py-8">加载中...</div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700">
      <h2 className="text-2xl font-semibold text-cyan-400 mb-6">历史报告</h2>

      {reports.length === 0 ? (
        <div className="text-center text-slate-400 py-8">
          <p>暂无审计报告</p>
          <p className="text-sm mt-2">提交第一个审计任务开始使用</p>
        </div>
      ) : (
        <div className="space-y-4">
          {reports.map((report, index) => (
            <div
              key={index}
              className="bg-slate-900/50 rounded-lg p-6 border border-slate-700 hover:border-cyan-500 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-slate-100 mb-2">
                    {report.url || '未知网址'}
                  </h3>
                  <p className="text-sm text-slate-400 mb-3">
                    📅 {report.timestamp}
                  </p>
                  <p className="text-xs text-slate-500 font-mono">
                    {report.name}
                  </p>
                </div>
                <Link
                  href={`/reports/${report.name}`}
                  className="ml-4 bg-cyan-500 hover:bg-cyan-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  查看报告
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
