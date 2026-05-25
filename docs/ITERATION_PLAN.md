# VisePanda 迭代规划 v3.0

> 路线图：美观 → 知识库 → Prompt → UI布局 → 地图 → 主动提问
> 自动化迭代模式（无需人工确认）

---

## 🏗️ 版本路线图

```
v2.x (当前)               v3.0 知识库+Prompt       v3.1 UI重构+地图         v3.2 美观收尾
  中国风UI (初版)     ──→   结构化旅行知识库     ──→    Landing/聊天重排版   ──→   动画过渡润色
  建筑剪影背景               LLM System Prompt     地图路线交互增强         颜色/字体微调
  红金配色                  主动提问机制           分享页改进                PWA优化
```

---

## Iter 1 — 知识库搭建 + LLM Prompt 重构

**目标**：让 AI 能说出有据可查的中国旅行建议，而非泛泛而谈

### In Scope
- 创建 `data/knowledge/` 旅行知识库（城市/景点/美食/交通/省钱技巧）
- 重写 system prompt（结构化输出、主动提问、中文优先）
- AI 在对话前主动问用户偏好（预算/风格/人数/季节）

### 模块

| # | 模块 | 文件 | 说明 |
|---|------|------|------|
| 1.1 | 城市知识 | `data/knowledge/cities.py` | 15+ 热门城市基本信息 |
| 1.2 | 景点知识 | `data/knowledge/attractions.py` | 各城市主要景点 + 特点 |
| 1.3 | 美食知识 | `data/knowledge/food.py` | 地方特色美食 + 推荐 |
| 1.4 | 旅行贴士 | `data/knowledge/tips.py` | 省钱/交通/季节/注意事项 |
| 1.5 | Prompt 引擎 | `api/prompt.py` | System Prompt + 主动提问逻辑 |
| 1.6 | 集成 | `api/index.py` | 将知识注入 LLM 调用 |

---

## Iter 2 — UI 重新排版 + 地图增强

**目标**：信息层级更清晰，地图交互更丰富

### In Scope
- Landing 页重新布局（Hero → 推荐路线 → 城市卡片）
- Chat 页重构（左侧行程面板 + 右侧聊天）
- 地图增强（多路线、POI 标记、Day 切换动画）
- 分享页优化

### Out of Scope
- 数据库迁移（需密码）
- 用户手机号/短信（需阿里云 Key）

---

## Iter 3 — 美观收尾

**目标**：像素级打磨

### In Scope
- 动画过渡（页面切换、消息出现）
- 字体系统（中文字体加载）
- 微交互（按钮反馈、加载态）
- 移动端适配 final pass

---

## 已知跳过项（需人工）

| # | 项 | 原因 |
|---|-----|------|
| S1 | Supabase DATABASE_URL 配置 | 需 Supabase 数据库密码 |
| S2 | 阿里云短信 Key | 需阿里云 AccessKey |
| S3 | Google OAuth 验证 | 需用户走一遍流程确认 |
