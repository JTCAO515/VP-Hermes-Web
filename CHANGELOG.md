# Changelog

## v4.0.3 — 2026-06-19

### Added
- B3: 城市对比模式 — `GET /api/cities/compare?cities=a,b` 后端端点
- B3: 前端对比弹窗渲染（Vibe / Best Season / Budget / Highlights 横向对比）
- B3: Chat 中自动检测「对比北京和成都」「compare beijing chengdu」触发对比
- B3: 缺字段显示 N/A，不崩不藏

## v4.0.2 — 2026-06-19

### Added
- B2: Trip Timeline 可视化 — `web/trip-timeline.js` + `web/trip-timeline.css`
- B2: AI 行程回复自动渲染为垂直时间线卡片（按活动类型颜色编码）
- B2: 一键复制行程（Timeline 上的 Copy 按钮）

## v4.0.1 — 2026-06-19

### Added
- B1a: Auth 系统加固 — `POST /api/auth/logout` 端点（后端删除 token）
- B1a: 前端登出 → 调用后端 API 销毁 token + 清 localStorage + reload

### Changed
- 版本号从 v3.x → v4.0.1
