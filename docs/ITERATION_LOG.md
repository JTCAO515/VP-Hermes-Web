---
## Iteration 2 (跳过) — Supabase Postgres
**原因**: 缺少数据库密码，无法直连。
**替代**: SQLite /tmp 对 MVP 够用。
**待办**: 获取 Supabase DB password → `DATABASE_URL=postgresql://postgres:[PWD]@db.jdlinmdhmulozrjeseyc.supabase.co:5432/postgres`

---

## Iteration 3 — 首页改版 + 行程生成 Beta

**日期**: 2026-05-24
**目标**: 首页有推荐卡片，行程输出好看
**状态**: ✅ 完成

### 改动清单

| # | 改动 | 效果 |
|---|------|------|
| 1 | 卡片 CSS（.card/.cards/.card-emoji） | hover 上浮 + 发光边框 |
| 2 | 首页 3 个快捷卡片（北京/成都/云南） | 点击自动带 prompt 进聊天 |
| 3 | `goChat()` 函数 | 统一跳转逻辑 |
| 4 | 骨架屏 CSS（.skeleton + shimmer） | 等待 LLM 时的加载动画 |
| 5 | 行程卡片 CSS（.trip-card） | LLM 输出行程自动包裹高亮框 |
| 6 | `M()` 函数增强 | 检测 `**Day N**` → 自动套 trip-card |
| 7 | 发送按钮防重复 | 发送时 disabled + ...，完成恢复 |

### 测试结果（本地）

```
cards=4 | goChat=1 | skeleton=2 | trip=3 | btnDisable=2 | mobile=1
6/6 PASS
```

---

## Iteration 3 — 首页改版 + 行程生成 Beta

**日期**: 2026-05-24
**目标**: 首页有推荐卡片，行程输出好看
**状态**: ✅ 完成

| # | 改动 | 效果 |
|---|------|------|
| 1 | 卡片 CSS | hover 上浮 + 发光边框 |
| 2 | 首页 3 个快捷卡片 | 北京/成都/云南，点击自动带 prompt 进聊天 |
| 3 | `goChat()` 函数 | 统一跳转逻辑 |
| 4 | 骨架屏 CSS + shimmer 动画 | 等待 LLM 时显示加载条 |
| 5 | 行程卡片 `.trip-card` | LLM 输出行程自动高亮框 |
| 6 | `M()` 函数增强 | 检测 `**Day N**` → 套 trip-card |
| 7 | 发送按钮防重复 | disabled + "..." → 完成恢复 |

**测试**: 6/6 PASS

### 部署

- [x] 本地测试通过
- [ ] 待部署


---

## Iteration 4 — 聊天体验打磨

**日期**: 2026-05-24
**状态**: ✅ 完成

| # | 改动 | 效果 |
|---|------|------|
| 1 | 消息时间戳 | 每条消息右下角显示 HH:MM |
| 2 | `smartScroll()` | 用户在看历史时不强制滚动，靠近底部才自动滚 |
| 3 | `clearChat()` 按钮 | Header 新增 Clear 按钮，清空聊天 + localStorage |
| 4 | 游客 ID 持久化 | `vp_trip` 存 localStorage，刷新不丢 trip |

**测试**: 6/6 PASS

