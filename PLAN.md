# PLAN.md — VisePanda v3.0.3 迭代路线图

> PM视角 · 持续迭代 · 从v2.x到v3全面重构

---

## 当前项目状态

| 指标 | 数据 |
|------|------|
| 当前版本 | v2.x（Iter 124，FastAPI + Supabase + GLM-5.1） |
| 目标版本 | v3.0.1（WSGI + stdlib + DeepSeek V4 Flash + 熊猫中国风） |
| 后端行数 | 2,388 行（单文件 FastAPI）→ **重构为 WSGI ~500 行** |
| 前端 JS | 7 个文件 ~6,900 行 → **1 个 app.js** |
| 知识库 | 33 城（景点/美食/贴士）— 保留 |
| 设计系统 | 水墨暗色（DESIGN.md）— 升级为熊猫中国风 |
| LLM | GLM-5.1 → DeepSeek V4 Flash |
| 外部依赖 | 8 个 pip 包 → **零依赖（stdlib only）** |
| 数据库 | Supabase Postgres → **项目数据库 JSON** |
| 部署 | Vercel FastAPI → **Vercel WSGI** |

## 技术栈

```
前端: HTML/CSS/JS (单页) — 熊猫 × 中国风, 暗色/亮色双主题
后端: Vercel Python (stdlib only) — WSGI handler
LLM: DeepSeek V4 Flash (OpenAI 兼容 SSE 流式)
数据: 33 城知识库 JSON + 项目数据库 JSON
部署: Vercel Serverless (@vercel/python)
参考设计: popular-web-designs (Linear/Vercel/Apple 等 54 套模板)
```

## 已完成迭代（v2.x 时期 — 保留的知识资产）

| # | 内容 | 复用方式 |
|:--:|------|---------|
| Iter 0-14 | 基础搭建：FastAPI + SSE聊天 + 暗色主题 + 用户系统 + 行程 | 功能参考，代码重构 |
| Iter 107-112 | 美观+速度 Phase 1：字体优化/脚本按需/CSS动画/微交互/骨架屏 | 设计参考 |
| Iter 113-115 | Panda Logo + Bento网格 + Chat气泡 | 保留 Panda SVG + 设计思路 |
| Iter 116-119 | Service Worker + 缓存 + GZip | 后续参考 |
| Iter 120-121 | Bug修复 + 英文化 | 英文问题模型当时未解决 |
| Iter 122 | 城市图片化 | 保留 23 张城市 JPG |
| Iter 123 | 暗色/亮色主题切换 | 设计思路保留 |
| Iter 124 | 移动端深度适配 | 适配经验保留 |

## Completed Iterations

| Iter | Version | Module | Description |
|:----:|:-------:|--------|-------------|
| 1 | v3.0.1 | 🏗️ WSGI Skeleton | `api/index.py` + `vercel.json` + SPA entry |
| 2 | v3.0.1 | 📚 Knowledge Base | 36 cities, food, hotels, tips → JSON migration |
| 3 | v3.0.1 | 💬 Prompt + UI | System prompt injection + city cards + hero |
| 4 | v3.0.1 | 🎨 Markdown + Modal | MD renderer, stop button, city detail modal, chat history |
| 5 | v3.0.1 | ✨ Polish + Responsive | Card animations, light theme, responsive, multi-turn |
| 6 | v3.0.1 | 💾 Trip Persistence | Save/load/share trips, price estimate, trip validation |
| 7 | v3.0.1 | 🗺️ Maps + Smart | Leaflet dark maps, POI markers, smart prompt enhancement |
| 8 | v3.0.2 | 🔍 FAQ Matching | 10-category FAQ engine, query expansion, match badge |
| 9 | v3.0.3 | 🗺️ Map Tab | Full China overview map, 36-city coordinates, AMap/Leaflet |

## v3.1 迭代计划

| 方向 | 内容 | 时机 |
|------|------|------|
| 社交分享 | 行程 → Twitter/小红书格式导出 | Phase 4 |
| 知识扩充 | 50+ 城知识库 | Phase 4 |
| PWA | 离线访问 + 缓存策略 | Phase 4 |
| 多端 | 微信小程序 / Telegram Bot | 远期 |
| 商业化 | 基于行程的增值服务 | 远期 |

---

## 保留资产 vs 重构资产

### 🔄 保留（直接复用）

| 资产 | 路径 | 说明 |
|------|------|------|
| 城市知识库 | `data/knowledge/` | 33 城景点/美食/酒店/贴士 → JSON |
| 旅行工具箱 | `data/tools/` | 打包/价格/签证/语言/紧急 |
| 城市图片 | `static/img/` | 23 张 JPG 城市/美食图 |
| Panda SVG | `static/icon.svg` | 品牌 Logo |

### 🆕 新建（v3.0.1）

| 资产 | 说明 |
|------|------|
| `api/index.py` | WSGI handler（~500 行，stdlib only） |
| `web/index.html` | 单页前端入口 |
| `web/app.css` | 熊猫中国风样式 |
| `web/app.js` | 前端逻辑（聊天 + 导航 + 主题） |
| `data/cities.json` | 33 城知识库（JSON 版） |
| `data/tools.json` | 工具箱（JSON 版） |
| `data/projects/` | 项目数据库目录 |

---

## 验证方式

| 阶段 | 验证项 | 标准 |
|------|--------|------|
| 每次 commit | Python 语法检查 | `python -c "compile(...)"` |
| 每次 commit | 前端 HTML 格式 | 无语法错误 |
| Iter 1 | Vercel 部署 | `curl` 返回 200 |
| Iter 3 | SSE 聊天 | 流式返回，首 token < 2s |
| Iter 6 | 全量测试 | 所有 API 端点 200 |
| Iter 11 | Lighthouse | Performance ≥ 85 |
| Iter 15 | 功能完整度 | 所有 Phase 1-3 功能可用 |

---

*创建日期：2026-06-14*
*当前状态：Phase 3 完成（Iter 7 — 地图视图/价格估算/Chat增强）*
*后续：Phase 4 社交分享/知识扩充/PWA/多端*
