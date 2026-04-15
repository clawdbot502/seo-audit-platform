'use client';

import { useState } from 'react';

export default function AuditForm() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!url) {
      setMessage('请输入有效的 URL');
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
        setMessage(`✅ 审计已启动！Workflow Run ID: ${data.runId}`);
        setUrl('');
        // 刷新报告列表
        setTimeout(() => window.location.reload(), 2000);
      } else {
        setMessage(`❌ 启动失败: ${data.error}`);
      }
    } catch (error) {
      setMessage(`❌ 请求失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700">
      <h2 className="text-2xl font-semibold text-cyan-400 mb-6">开始新的审计</h2>

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
            className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold py-3 px-6 rounded-lg hover:from-cyan-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '启动中...' : '开始审计'}
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
          <li>支持任意公开访问的网站</li>
          <li>报告会自动保存到历史记录</li>
        </ul>
      </div>
    </div>
  );
}
