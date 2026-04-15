'use client';

import { useState, useEffect } from 'react';

interface AuditStatus {
  isRunning: boolean;
  status: string;
  conclusion?: string;
  runId?: number;
  createdAt?: string;
  updatedAt?: string;
}

export default function AuditForm() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [auditStatus, setAuditStatus] = useState<AuditStatus | null>(null);

  // 检查审计状态
  const checkAuditStatus = async () => {
    try {
      const response = await fetch('/api/audit-status');
      if (response.ok) {
        const data = await response.json();
        setAuditStatus(data);
      }
    } catch (error) {
      console.error('Failed to check audit status:', error);
    }
  };

  // 初始加载和定时轮询
  useEffect(() => {
    checkAuditStatus();
    const interval = setInterval(checkAuditStatus, 5000); // 每 5 秒检查一次
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!url) {
      setMessage('请输入有效的 URL');
      return;
    }

    if (auditStatus?.isRunning) {
      setMessage('已有审计任务正在进行中，请等待完成');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('/api/trigger-audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ 审计已启动！正在处理中...`);
        setUrl('');
        // 立即检查状态
        checkAuditStatus();
      } else {
        setMessage(`❌ 启动失败: ${data.error}`);
      }
    } catch (error) {
      setMessage(`❌ 请求失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = loading || auditStatus?.isRunning;

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700">
      <h2 className="text-2xl font-semibold text-cyan-400 mb-6">开始新的审计</h2>

      {/* 审计状态提示 */}
      {auditStatus?.isRunning && (
        <div className="mb-6 p-4 bg-yellow-900/30 border border-yellow-700 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-yellow-400"></div>
            <div>
              <p className="text-yellow-300 font-semibold">审计进行中...</p>
              <p className="text-yellow-400/80 text-sm mt-1">
                请等待当前任务完成后再提交新的审计请求
              </p>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-slate-300 mb-2">
            目标网址
          </label>
          <input
            type="url"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isDisabled}
          />
        </div>

        <button
          type="submit"
          disabled={isDisabled}
          className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold py-3 px-6 rounded-lg hover:from-cyan-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {auditStatus?.isRunning ? '审计进行中...' : loading ? '启动中...' : '开始审计'}
        </button>
      </form>

      {message && (
        <div className={`mt-4 p-4 rounded-lg ${
          message.startsWith('✅')
            ? 'bg-green-900/30 border border-green-700 text-green-300'
            : 'bg-red-900/30 border border-red-700 text-red-300'
        }`}>
          {message}
        </div>
      )}

      <div className="mt-6 text-sm text-slate-400">
        <p className="mb-2">💡 提示：</p>
        <ul className="list-disc list-inside space-y-1">
          <li>审计过程需要 2-3 分钟</li>
          <li>同一时间只能运行一个审计任务</li>
          <li>支持任意公开访问的网站</li>
          <li>报告会自动保存到历史记录</li>
        </ul>
      </div>
    </div>
  );
}
