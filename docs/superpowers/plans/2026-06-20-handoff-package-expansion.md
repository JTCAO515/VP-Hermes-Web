# VisePanda Handoff Package Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the repository handoff package with three new execution-oriented documents and link them into the existing handoff and README so a new owner can take over without relying on prior chat context.

**Architecture:** Keep `HANDOFF.md` as the main transfer entry point, keep `docs/2026-06-20-engineering-handoff-notes.md` as the deep engineering appendix, and add three new role-specific docs: first-week takeover, high-risk files, and production regression. Then wire these documents into `HANDOFF.md` and `README.md` through explicit links.

**Tech Stack:** Markdown, Git, existing repository docs

---

## File Map

- `docs/2026-06-20-first-week-takeover-checklist.md`
  - New onboarding doc for a developer’s first week
- `docs/2026-06-20-high-risk-files-guide.md`
  - New engineering risk guide focused on dangerous files and safe editing behavior
- `docs/2026-06-20-production-regression-manual.md`
  - New release / verification manual for desktop, mobile, assets, and core flows
- `HANDOFF.md`
  - Main handoff entry point; will link to the new docs in onboarding and index sections
- `README.md`
  - Will expose the new docs under `Planning Docs`

---

### Task 1: Add the first-week takeover checklist

**Files:**
- Create: `docs/2026-06-20-first-week-takeover-checklist.md`
- Test: `docs/2026-06-20-first-week-takeover-checklist.md`

- [ ] **Step 1: Write the new checklist file with the required structure**

```md
# VisePanda 接手首周清单

## 1. 文档目的

这份文档不是长期 roadmap，而是帮助新接手开发者在第一周建立正确的理解顺序，避免一上来就做高风险动作。

## 2. 接手前准备

- 先读 `HANDOFF.md`
- 再读 `docs/2026-06-20-engineering-handoff-notes.md`
- 再看 `README.md`
- 再看 `CHANGELOG.md`
- 确认当前部署仍是 `Vercel`

## 3. 第 1 天

- 本地跑起项目
- 跑 Python 与 Node 测试
- 只阅读主链路文件，不急着改

## 4. 第 2-3 天

- 对照线上站点走核心用户路径
- 记录文档与现实不一致的地方
- 区分主链路与兼容层

## 5. 第 4-5 天

- 只做小范围修复
- 先补测试，再动代码
- 优先用户可感知问题

## 6. 这一周不要做什么

- 不要先重构 `web/app.js`
- 不要先改部署
- 不要先删除 `static/*` 历史兼容层
- 不要未经验证修改 auth/chat 核心链路
```

- [ ] **Step 2: Run a content presence check**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('/workspace/VP-Hermes-Web/docs/2026-06-20-first-week-takeover-checklist.md').read_text()
required = [
    '## 1. 文档目的',
    '## 3. 第 1 天',
    '## 6. 这一周不要做什么',
    'web/app.js',
]
missing = [item for item in required if item not in text]
print('missing:', missing)
PY
```

Expected:

- Output is `missing: []`

- [ ] **Step 3: Commit the first-week checklist**

```bash
git add docs/2026-06-20-first-week-takeover-checklist.md
git commit -m "docs: add first-week takeover checklist"
```

---

### Task 2: Add the high-risk files guide

**Files:**
- Create: `docs/2026-06-20-high-risk-files-guide.md`
- Test: `docs/2026-06-20-high-risk-files-guide.md`

- [ ] **Step 1: Write the file guide with a fixed structure per file**

```md
# VisePanda 高风险文件修改指南

## 1. 文档目的

这份文档帮助新接手开发者识别高风险文件，理解为什么危险，以及修改前后至少要确认什么。

## 2. `web/app.js`

### 负责什么

当前前端主逻辑入口，负责 bootstrap、auth、chat、cities、trips、tools、view navigation。

### 为什么危险

这是当前最重的前端文件，多个功能耦合在一起，小改也可能影响多个视图。

### 修改前先确认什么

- 改动是否涉及 nav / auth / bootstrap
- 是否会影响已有 view state
- 是否有对应前端测试

### 修改后至少测什么

- `node --test web/tests/*.test.js`
- 首页 / Chat / Cities / Trips / Tools

## 3. `api/auth.py`

### 负责什么

当前活跃的登录、session、profile、trip、chat history、admin 数据链路。

### 为什么危险

登录、用户态和历史记录都依赖它，改错容易产生连锁问题。
```

- [ ] **Step 2: Include all required high-risk files and a safe-zone section**

```md
## 4. `web/app.css`
## 5. `web/index.html`
## 6. `api/chat.py`
## 7. `api/index.py`

## 8. 相对安全的改动区

- 低风险文案修正
- 非核心展示层样式
- 某些独立数据文件
- 非主链路工具文案
```

- [ ] **Step 3: Run a content presence check**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('/workspace/VP-Hermes-Web/docs/2026-06-20-high-risk-files-guide.md').read_text()
required = [
    '## 2. `web/app.js`',
    '## 3. `api/auth.py`',
    '## 8. 相对安全的改动区',
    'node --test web/tests/*.test.js',
]
missing = [item for item in required if item not in text]
print('missing:', missing)
PY
```

Expected:

- Output is `missing: []`

- [ ] **Step 4: Commit the high-risk guide**

```bash
git add docs/2026-06-20-high-risk-files-guide.md
git commit -m "docs: add high-risk files guide"
```

---

### Task 3: Add the production regression manual

**Files:**
- Create: `docs/2026-06-20-production-regression-manual.md`
- Test: `docs/2026-06-20-production-regression-manual.md`

- [ ] **Step 1: Write the regression manual with desktop and mobile coverage**

```md
# VisePanda 线上回归检查手册

## 1. 文档用途

这份文档用于发布前后和线上复测时做人工回归，不替代自动化测试。

## 2. 回归前提

- 线上地址：`https://www.go2china.space`
- 本地测试命令：

```bash
python3 -m unittest discover -s tests -v
node --test web/tests/*.test.js
```

## 3. 桌面端核心回归

- 首页是否正常加载
- `Sign in` 是否正常触发
- Chat 是否正常响应
- Cities 是否可进入
- Trips 是否可进入
- Tools 是否可进入

## 4. 移动端核心回归

- bottom nav 是否可见
- tab 是否可点击
- safe-area 是否正确
- 页面是否被遮挡
- 输入区是否被挤压
```

- [ ] **Step 2: Add troubleshooting hints and release threshold**

```md
## 5. 资源与性能观察点

- 图片是否加载失败
- 页面切换是否缺乏反馈
- 是否出现空白或卡死感
- 控制台是否报错

## 6. 如果发现问题先怀疑哪里

- `Sign in` 异常：先看 `web/app.js` 的 bootstrap 与 auth trigger
- 图片异常：先看图片路径、fallback 和 `static/img`
- 移动端 nav 异常：先看 `web/app.css` 的 safe-area 和 `.bottom-nav`

## 7. 发布前最低通过线

- 首页、Sign in、Chat、Cities、Trips、Tools 全部可进入
- 手机端 bottom nav 可见可点
- 图片没有大面积失败
- 回归命令通过
```

- [ ] **Step 3: Run a content presence check**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('/workspace/VP-Hermes-Web/docs/2026-06-20-production-regression-manual.md').read_text()
required = [
    '## 3. 桌面端核心回归',
    '## 4. 移动端核心回归',
    'Sign in',
    'web/app.js',
    'web/app.css',
]
missing = [item for item in required if item not in text]
print('missing:', missing)
PY
```

Expected:

- Output is `missing: []`

- [ ] **Step 4: Commit the regression manual**

```bash
git add docs/2026-06-20-production-regression-manual.md
git commit -m "docs: add production regression manual"
```

---

### Task 4: Wire the new docs into `HANDOFF.md` and `README.md`

**Files:**
- Modify: `HANDOFF.md`
- Modify: `README.md`

- [ ] **Step 1: Add the new docs to `HANDOFF.md` onboarding guidance**

```md
## 10. 接手建议

1. 先读 `HANDOFF.md`
2. 再读 [docs/2026-06-20-engineering-handoff-notes.md](docs/2026-06-20-engineering-handoff-notes.md)
3. 再读 [docs/2026-06-20-first-week-takeover-checklist.md](docs/2026-06-20-first-week-takeover-checklist.md)
4. 再读 [docs/2026-06-20-high-risk-files-guide.md](docs/2026-06-20-high-risk-files-guide.md)
5. 最后参考 [docs/2026-06-20-production-regression-manual.md](docs/2026-06-20-production-regression-manual.md)
```

- [ ] **Step 2: Add the new docs to `HANDOFF.md` and `README.md` indexes**

```md
| [docs/2026-06-20-first-week-takeover-checklist.md](docs/2026-06-20-first-week-takeover-checklist.md) | 新接手开发者首周进入清单 |
| [docs/2026-06-20-high-risk-files-guide.md](docs/2026-06-20-high-risk-files-guide.md) | 高风险文件修改指南 |
| [docs/2026-06-20-production-regression-manual.md](docs/2026-06-20-production-regression-manual.md) | 发布前后回归手册 |
```

```md
## Planning Docs

- [Commercial Upgrade Plan](docs/2026-06-20-commercial-upgrade-plan.md)
- [Engineering Handoff Notes](docs/2026-06-20-engineering-handoff-notes.md)
- [First-Week Takeover Checklist](docs/2026-06-20-first-week-takeover-checklist.md)
- [High-Risk Files Guide](docs/2026-06-20-high-risk-files-guide.md)
- [Production Regression Manual](docs/2026-06-20-production-regression-manual.md)
```

- [ ] **Step 3: Run a final link presence check**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
handoff = Path('/workspace/VP-Hermes-Web/HANDOFF.md').read_text()
readme = Path('/workspace/VP-Hermes-Web/README.md').read_text()
checks = {
    'handoff->first-week': 'docs/2026-06-20-first-week-takeover-checklist.md' in handoff,
    'handoff->risk-guide': 'docs/2026-06-20-high-risk-files-guide.md' in handoff,
    'handoff->regression': 'docs/2026-06-20-production-regression-manual.md' in handoff,
    'readme->first-week': 'First-Week Takeover Checklist' in readme,
    'readme->risk-guide': 'High-Risk Files Guide' in readme,
    'readme->regression': 'Production Regression Manual' in readme,
}
print(checks)
PY
```

Expected:

- All values are `True`

- [ ] **Step 4: Commit the index-link pass**

```bash
git add HANDOFF.md README.md
git commit -m "docs: link expanded handoff package"
```

---

## Self-Review

### Spec coverage

- First-week onboarding doc: Task 1
- High-risk file guide: Task 2
- Production regression manual: Task 3
- Handoff/README link integration: Task 4

### Placeholder scan

- No `TODO` / `TBD`
- Every new file has required section content
- Every validation step has an exact command

### Type consistency

- File paths are consistent across all tasks:
  - `docs/2026-06-20-first-week-takeover-checklist.md`
  - `docs/2026-06-20-high-risk-files-guide.md`
  - `docs/2026-06-20-production-regression-manual.md`
  - `docs/2026-06-20-engineering-handoff-notes.md`

