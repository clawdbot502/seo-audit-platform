# SEO Audit Platform

自动化 SEO 审计平台 - 支持多模型 AI 驱动的技术和内容 SEO 分析

## 功能特性

- ✅ **完全自动化**：用户输入 URL，自动完成完整审计流程
- ✅ **多模型支持**：支持 OpenAI、Anthropic、Google、DeepSeek 等任意大模型
- ✅ **双维度审计**：技术 SEO + 内容 SEO 全面分析
- ✅ **美观报告**：深色主题 HTML 报告，响应式设计
- ✅ **历史记录**：所有报告存储在 GitHub，可随时查看
- ✅ **零成本部署**：基于 GitHub Actions + Vercel 免费额度

## 架构设计

```
用户浏览器
    ↓ (输入 URL)
Next.js Web 应用 (Vercel)
    ↓ (调用 GitHub API)
GitHub Actions Workflow
    ↓ (执行审计)
Python 审计脚本 + LiteLLM
    ↓ (调用 AI 模型)
OpenAI / Anthropic / Google / 其他
    ↓ (生成报告)
GitHub 仓库 /reports 目录
    ↓ (自动部署)
Vercel 展示报告页面
```

## 快速开始

### 1. 配置 GitHub Secrets

在仓库设置中添加以下 Secrets（Settings → Secrets and variables → Actions）：

**必需配置：**
- `MODEL_PROVIDER`: 模型提供商（`openai` / `anthropic` / `google` / `deepseek`）
- 对应的 API Key：
  - `OPENAI_API_KEY`: OpenAI API Key（如果使用 OpenAI）
  - `ANTHROPIC_API_KEY`: Anthropic API Key（如果使用 Claude）
  - `GOOGLE_API_KEY`: Google API Key（如果使用 Gemini）
  - `DEEPSEEK_API_KEY`: DeepSeek API Key（如果使用 DeepSeek）

**使用 gh CLI 配置（推荐）：**
```bash
gh secret set MODEL_PROVIDER --body "openai"
gh secret set OPENAI_API_KEY --body "sk-..."
```

### 2. 部署 Web 应用到 Vercel

**方式 A：通过 Vercel Dashboard**
1. 访问 https://vercel.com/new
2. 导入 GitHub 仓库 `seo-audit-platform`
3. 设置 Root Directory 为 `web`
4. 配置环境变量：
   - `GITHUB_TOKEN`: GitHub Personal Access Token（需要 `repo` 和 `workflow` 权限）
   - `REPO_OWNER`: `clawdbot502`
   - `REPO_NAME`: `seo-audit-platform`
5. 点击 Deploy

**方式 B：通过 Vercel CLI**
```bash
cd web
npm install -g vercel
vercel --prod
```

### 3. 使用 Web 界面触发审计

1. 访问你的 Vercel 部署地址（如 `https://your-app.vercel.app`）
2. 在表单中输入目标 URL
3. 点击"开始审计"
4. 等待 2-3 分钟，审计完成后自动显示在历史记录中
5. 点击"查看报告"查看详细审计结果

### 4. 手动触发审计（可选）

如果不使用 Web 界面，也可以直接在 GitHub Actions 中触发：

1. 进入 GitHub 仓库的 **Actions** 标签
2. 选择 **SEO Audit** workflow
3. 点击 **Run workflow**
4. 输入目标 URL（如 `https://example.com`）
5. 点击 **Run workflow** 开始审计

### 5. 查看报告

审计完成后，报告会自动提交到 `/reports` 目录，文件名格式：
```
seo-audit-{domain}-{timestamp}.html
```

可以通过以下方式查看：
- **Web 界面**：在首页的历史记录列表中点击"查看报告"
- **GitHub**：直接访问 `https://github.com/clawdbot502/seo-audit-platform/tree/main/reports`
- **原始文件**：`https://raw.githubusercontent.com/clawdbot502/seo-audit-platform/main/reports/{filename}`

## 本地开发

### 安装依赖

```bash
cd seo-audit-engine
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```bash
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### 运行审计

```bash
cd seo-audit-engine
python main.py https://example.com
```

## 项目结构

```
seo-audit-platform/
├── .github/
│   └── workflows/
│       └── seo-audit.yml          # GitHub Actions workflow
├── seo-audit-engine/              # Python 审计引擎
│   ├── auditors/                  # 审计器
│   │   ├── technical_seo.py       # 技术 SEO 审计
│   │   ├── content_seo.py         # 内容 SEO 审计
│   │   └── merger.py              # 结果合并
│   ├── crawlers/                  # 爬虫
│   │   ├── html_fetcher.py        # HTML 抓取
│   │   └── tech_checker.py        # 技术检查
│   ├── utils/                     # 工具
│   │   ├── llm_client.py          # LLM 客户端
│   │   └── report_generator.py    # 报告生成器
│   ├── config.py                  # 配置文件
│   ├── main.py                    # 主程序
│   └── requirements.txt           # Python 依赖
├── web/                           # Next.js Web 应用
│   ├── app/
│   │   ├── api/                   # API Routes
│   │   │   ├── trigger-audit/     # 触发审计 API
│   │   │   └── reports/           # 获取报告列表 API
│   │   ├── components/            # React 组件
│   │   │   ├── AuditForm.tsx      # 审计表单
│   │   │   └── ReportList.tsx     # 报告列表
│   │   ├── reports/[name]/        # 报告详情页
│   │   └── page.tsx               # 主页
│   ├── package.json
│   └── README.md
├── reports/                       # 审计报告目录
└── README.md                      # 项目文档
```

## 审计流程

1. **Step 1**: 数据抓取 + 技术初筛
   - 抓取 HTML 内容
   - 检查 robots.txt、sitemap.xml
   - 检查响应头和 HTTPS

2. **Step 2**: 技术 SEO 审计
   - 爬取性和索引性
   - 页面性能
   - 结构化数据
   - 安全性

3. **Step 3**: 内容 SEO 审计
   - On-Page SEO（标题、描述、H1-H6）
   - 文案质量
   - 内容结构
   - 用户体验

4. **Step 4**: 合并审计结果
   - 去重
   - 按严重程度排序
   - 计算总体评分

5. **Step 5**: 生成 HTML 报告
   - 深色主题设计
   - 响应式布局
   - 详细问题列表和优化建议

## 支持的模型

| 提供商 | 模型 | 环境变量 |
|--------|------|----------|
| OpenAI | gpt-4-turbo-preview | `OPENAI_API_KEY` |
| Anthropic | claude-3-opus-20240229 | `ANTHROPIC_API_KEY` |
| Google | gemini/gemini-pro | `GOOGLE_API_KEY` |
| DeepSeek | deepseek/deepseek-chat | `DEEPSEEK_API_KEY` |

## 下一步计划

- [x] 开发 Next.js Web 应用前端
- [x] 实现历史报告列表页面
- [ ] 添加报告对比功能
- [ ] 支持批量审计
- [ ] 添加定时审计功能
- [ ] 添加审计进度实时显示
- [ ] 支持自定义审计配置

## 技术栈

**后端审计引擎：**
- Python 3.11+
- LiteLLM（多模型统一接口）
- BeautifulSoup4（HTML 解析）
- Requests（HTTP 请求）
- Jinja2（模板引擎）

**前端 Web 应用：**
- Next.js 14（App Router）
- TypeScript
- Tailwind CSS
- GitHub API

**部署和 CI/CD：**
- GitHub Actions（自动化审计）
- Vercel（Web 应用托管）
- GitHub Pages（报告展示）

## 常见问题

### Q: 如何切换 AI 模型？
A: 修改 GitHub Secrets 中的 `MODEL_PROVIDER` 值，支持：`openai`、`anthropic`、`google`、`deepseek`

### Q: 审计需要多长时间？
A: 通常 2-3 分钟，取决于网站大小和 AI 模型响应速度

### Q: 可以审计需要登录的页面吗？
A: 目前仅支持公开访问的页面，未来会添加认证支持

### Q: 报告可以导出吗？
A: 报告是独立的 HTML 文件，可以直接下载保存

### Q: 如何添加新的审计维度？
A: 修改 `seo-audit-engine/auditors/` 中的审计器代码，添加新的检查逻辑

## License

MIT
