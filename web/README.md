# SEO Audit Platform - Web Frontend

Next.js 前端应用，用于触发 SEO 审计和查看历史报告。

## 环境变量配置

创建 `.env.local` 文件：

```bash
GITHUB_TOKEN=your_github_personal_access_token
REPO_OWNER=clawdbot502
REPO_NAME=seo-audit-platform
```

### 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：
   - `repo` (完整仓库访问)
   - `workflow` (触发 GitHub Actions)
4. 生成并复制 token

## 本地开发

```bash
npm install
npm run dev
```

访问 http://localhost:3000

## 部署到 Vercel

1. 连接 GitHub 仓库到 Vercel
2. 配置环境变量（同上）
3. 部署

## 功能

- ✅ 输入 URL 触发审计
- ✅ 查看历史报告列表
- ✅ 在线查看报告详情
- ✅ 响应式设计
- ✅ 深色主题
