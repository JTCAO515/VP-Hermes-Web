# VisePanda 工程接手附录

## 1. 文档目的

这份附录不是产品总览，而是给新开发者使用的详尽工程交接说明。
主交接文档仍然是 `HANDOFF.md`，这里负责补足：

- 当前活跃主链路
- 核心文件职责
- 前后端运行关系
- 测试入口
- 已知工程风险
- 不建议轻易改动的部分

适用对象：

- 新接手并需要先判断“当前代码到底以哪里为准”的开发者
- 需要快速定位主入口、活跃模块、测试入口与风险区域的维护者
- 计划继续做产品验证、稳定性修补、准商用迭代的工程同学

阅读顺序建议：

1. 先看 `HANDOFF.md` 理解项目现状和业务背景
2. 再看本文，建立当前代码主链路的工程地图
3. 再读 `README.md` 获取本地运行和 API 概览
4. 最后结合 `CHANGELOG.md` 和 `docs/2026-06-20-commercial-upgrade-plan.md` 判断后续优先级

## 2. 当前活跃主链路

### 前端主链路

- `web/index.html`：主 SPA 壳层、header、desktop/mobile nav、各 view 容器、聊天区、地图区、Trips 区、Cities 区、Tools 区，以及认证弹层/移动端 overlay 的挂载点。
- `web/app.js`：当前前端主逻辑入口，负责导航、聊天、auth、cities、trips、tools、map、runtime config、bootstrap。
- `web/app.css`：当前主样式系统，含桌面、移动端、overlay、安全区、工具与稳定性补丁。
- `web/trip-timeline.js` / `web/trip-timeline.css`：聊天结果中的 itinerary 时间线增强层，不是导航入口，但会被 `web/index.html` 直接加载并由 `web/app.js` 注入。
- `web/admin.html`：后台管理独立入口页，经 `/admin` 路由直接返回，不经过主 SPA 视图切换。

### 后端主链路

- `api/index.py`：WSGI 路由入口，负责 `/api/*` 分发、`/admin` 页面回退、静态文件兜底。
- `api/auth.py`：当前活跃的用户、session、trips、chat history、profile、admin 数据链路。
- `api/chat.py`：SSE 流式聊天，负责 FAQ 匹配、系统提示词构建、图片标记拆出、DeepSeek 调用。
- `api/cities.py`：城市列表、城市详情、城市对比、价格估算、行程校验。
- `api/tools.py`：工具数据路由，读取工具索引和详情。
- `api/visa.py`：签证政策查询与签证材料文案生成。
- `api/config.py`：前端运行时配置出口，主要给地图 key、Google 登录 client id、版本号。
- `api/common.py`：共享 JSON/静态文件/SSE/POST 解析能力，是全部 API 的底层公共层。

### 端到端主流程

#### 流程 A：用户打开站点

1. 浏览器访问 `/`
2. `api/common.py` 的静态文件逻辑返回 `web/index.html`
3. `web/index.html` 加载 `web/app.css`、`web/app.js`、`web/trip-timeline.js`
4. `web/app.js` 中 `init()` 按顺序执行 theme、runtime config、auth trigger、primary nav、chat input、startup state、hash navigation
5. 初始路由默认落到 `home`，并按需继续触发 `loadHomeCities()` / `attachImageFallbacks()`

#### 流程 B：用户在 Chat 中生成行程

1. `web/app.js` 的 `sendMessage()` 采集输入并把最近消息打包
2. 前端向 `POST /api/chat` 发起请求
3. `api/index.py` 将请求分发给 `api/chat.py`
4. `api/chat.py` 做 FAQ 匹配、拼装 system prompt、调用 DeepSeek SSE，并按 token / image / faq / done 事件持续输出
5. `web/app.js` 逐段消费流，更新 typing、分泡渲染、插图、FAQ badge
6. 若结果看起来像 itinerary，则触发 `autoSaveTrip()`；登录用户走 `/api/trips`，游客落本地 `localStorage`
7. 若页面加载了时间线增强脚本，则由 `TripTimeline.inject()` 对结果做二次可视化

#### 流程 C：用户登录后查看 Trips / Chat 历史

1. 前端认证态由 `localStorage.vp_token` + `/api/auth/me` 恢复
2. `web/app.js` 的 auth 模块统一处理登录、注册、登出、忘记密码、Google 登录、profile 更新
3. Trips 视图通过 `/api/trips` 读取 recent / saved 数据
4. Chat 历史通过 `/api/auth/chat-history` 和 `/api/auth/chat/:id` 读取
5. 上述数据全部由 `api/auth.py` 背后的 SQLite 存储提供

## 3. 前端结构

### 3.1 页面层级

`web/index.html` 是当前唯一主站入口，核心 view 包括：

- `#view-home`：Editorial Atlas 首页，负责 Hero、Trust Layer、City Rail、Planner Entry
- `#view-chat`：SSE 聊天主视图，含建议区、行动 rail、输入区、停止流式按钮
- `#view-trips`：行程库，分 recent 与 saved archive
- `#view-map`：全国城市地图与城市详情面板
- `#view-cities`：城市卡片列表、筛选轨道、城市详情
- `#view-tools`：Packing / Pricing / Visa / Phrases / Emergency 工具页

额外前端入口：

- `web/admin.html`：后台管理页
- `web/manifest.json`、`web/sw.js`：PWA 相关资源
- `static/img/*`：首页、城市、食物与品牌静态图

### 3.2 `web/app.js` 的职责分块

虽然 `web/app.js` 只有一个主文件，但实际上同时承载多个子系统：

- 导航与视图切换：`navigate()`、`initHashNavigation()`、`bindPrimaryNav()`
- 启动保护：`safeInitStep()`、全局 loading / error state
- 首页与城市浏览：城市卡片、筛选 rail、城市详情、图片 fallback
- 聊天：`sendMessage()`、`stopStreaming()`、typing、多 bubble 输出、FAQ badge、图片 bubble
- Trips：自动保存、最近/已保存分组、复制时间线、重载已有行程
- 地图：`initMap()`、AMap/Leaflet 双通路、marker detail、从地图跳转聊天
- Auth：会话恢复、登录/注册/重置密码、Google 登录、profile 更新、我的聊天/我的行程
- UI 细节：主题切换、安全区、移动端聊天 overlay、scroll helper

这意味着它是事实上的前端编排层。当前阶段可以继续在其内部做局部增强，但不建议在没有拆分测试与模块边界前做大范围文件分裂。

### 3.3 当前前端的实际边界

- 主站当前以 `web/*` 为准，不是 `static/*.js`
- `static/auth.js`、`static/chat.js`、`static/trips.js`、`static/profile.js`、`static/map.js`、`static/landing.js` 更像历史兼容层/旧路径残留
- 若要判断“今天用户实际走哪条前端路径”，优先看 `web/index.html` 和 `web/app.js`
- 若要判断某个 UI 改动是否会破坏移动端，必须同时检查桌面 header 导航、底部导航、overlay、safe-area 样式

## 4. 后端结构

### 4.1 路由总入口

`api/index.py` 是所有运行时入口的总调度器，路由顺序本身有工程含义：

- `/api/health`：健康检查
- `/api/chat`：流式聊天
- `/api/cities/compare`：必须先于 `/api/cities` catch-all
- `/api/cities*`：城市数据
- `/api/tools*`：工具数据
- `/api/estimate` / `/api/validate`：估价与校验
- `/api/visa/*`：签证链路
- `/api/map` / `/api/config`：运行时配置
- auth/admin/trips/chat-history：统一交给 `api/auth.py`
- `/admin`：直接返回 `web/admin.html`
- 其余路径：交给静态文件服务和 404 fallback

任何改动都要注意顺序依赖，尤其是带有前缀 catch-all 的路由。

### 4.2 认证与持久化中心：`api/auth.py`

这是当前后端最关键、也最容易形成连锁反应的文件。它同时承担：

- 用户注册、登录、登出、会话校验
- Google 登录验证
- Trips 增删查
- Chat 会话保存、历史列表、详情读取
- Profile 更新、忘记密码、密码重置
- Admin 用户列表、详情、删除、更新、聊天查看、统计
- SQLite 初始化与迁移

当前表结构集中在同一文件初始化，包括：

- `users`
- `sessions`
- `trips`
- `chat_conversations`
- `chat_messages`
- `password_reset_tokens`

存储策略：

- 本地开发默认使用 `data/users.db`
- Vercel 环境因文件系统只读，默认改到 `/tmp/users.db`
- 也可通过 `AUTH_DB_PATH` 覆盖数据库路径

### 4.3 内容与工具型接口

- `api/chat.py`：DeepSeek SSE 出口，依赖 `DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL`、`DEEPSEEK_BASE_URL`
- `api/cities.py`：读 `data/cities.json`、`data/food.json`、`data/hotels.json`、`data/tips.json`，同时内嵌 `_MAP_DATA` 与 `ESTIMATE_DATA`
- `api/tools.py`：读 `data/tools.json`
- `api/visa.py`：读 `data/visa_policies.json`，并把行程内容整理成签证申请文本
- `api/config.py`：输出 `AMAP_KEY`、`AMAP_SECURITY_CODE`、`GOOGLE_CLIENT_ID`、版本号

### 4.4 静态与基础设施层

`api/common.py` 负责：

- JSON 输出
- POST body 读取
- JSON 文件读取
- `web/` 与 `static/` 双目录静态文件服务
- SSE event 格式包装

它虽然不大，但一旦改错会同时影响：

- 前端首屏资源返回
- 静态图片缓存
- SSE 事件格式
- 所有 JSON API 响应基础行为

## 5. 数据与资源

### 5.1 当前仓库内数据源

主数据目录为 `data/`，活跃资源包括：

- `data/cities.json`：城市基础档案
- `data/food.json`：城市美食数据
- `data/hotels.json`：住宿数据
- `data/tips.json`：本地提示
- `data/faq.json`：FAQ 分类与 prompt hint
- `data/tools.json`：工具页详情
- `data/visa_policies.json`：签证政策
- `data/city_images.json`：城市图片映射

补充知识源还在：

- `data/knowledge/*.py`
- `data/tools/*.py`

这部分更像知识组织层/历史沉淀层，不是当前线上接口的第一读路径；排查运行结果时优先看 JSON 数据是否已被 API 直接引用。

### 5.2 静态资源

- `static/img/*`：站点品牌图、城市图、美食图、灵感图、OG 图
- `web/icon-*.png`、`web/manifest.json`：PWA 图标与安装元数据
- `static/icon.svg`：站点图标资源

前端聊天中的 `[img:...]` 标记会尝试映射到 `static/img` 下的图片，因此图片命名约定本身属于运行时契约的一部分。

### 5.3 外部依赖与环境变量

当前工程真正依赖的外部配置主要有：

- `DEEPSEEK_API_KEY` / `LLM_API_KEY` / `AESCULAP_DEEPSEEK_KEY`
- `DEEPSEEK_MODEL`
- `DEEPSEEK_BASE_URL`
- `AMAP_KEY`
- `AMAP_SECURITY_CODE`
- `GOOGLE_CLIENT_ID`
- `ADMIN_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `AUTH_DB_PATH`

其中最先影响线上可用性的通常是 LLM、地图、Google 登录和数据库路径。

## 6. 修改时的高风险区域

### `web/app.js`

这是当前最重的前端文件。不要在未理解入口顺序之前直接做大规模重构。

风险点：

- 启动流程集中在 `init()`，顺序打乱会引发视图、主题、配置、hash 导航异常
- chat / auth / trips / map / city detail 共用同一个状态面和 DOM 选择方式
- 登录态、游客态、流式状态、自动保存逻辑彼此交织
- 某些行为依赖 DOM 结构和 element id，重命名 HTML 容器会直接破坏运行时

### `api/auth.py`

当前活跃数据链路集中在这里，涉及登录、行程、聊天历史和后台权限。

风险点：

- 改响应字段会同时影响 Python contract tests 与 `web/app.js` 登录态恢复
- 改 SQLite schema 或初始化逻辑要同时考虑本地开发与 Vercel `/tmp` 行为
- Admin、Trips、Chat History 复用同一套 token/user lookup，局部修改容易造成横向回归

### `api/index.py`

路由分发顺序有实际业务含义，不要把前缀路由随意前后调换。

尤其要注意：

- `/api/cities/compare` 必须先于 `/api/cities`
- auth catch-all 之前的显式路由优先级
- `/admin` 与静态资源兜底的关系

### `api/common.py`

这是静态资源与 API 基础响应层。这里的变更会放大到全站。

### `static/*`

这批文件里有历史兼容层，不要默认它们都是当前主路径。
判断是否能删、能改，先确认 `web/index.html` 是否仍直接引用。

## 7. 测试入口

### Python

```bash
python3 -m unittest discover -s tests -v
```

当前 Python 合同测试重点文件：

- `tests/test_auth_contract.py`
- `tests/test_admin_contract.py`
- `tests/test_config_contract.py`
- `tests/test_trips_contract.py`

### Node

```bash
node --test web/tests/*.test.js
```

当前前端结构/回归测试重点文件：

- `web/tests/auth-state.test.js`
- `web/tests/chat-stream.test.js`
- `web/tests/stability-ui.test.js`
- `web/tests/view-registry.test.js`

建议执行顺序：

1. 改动认证、Trips、配置、后台时先跑 Python tests
2. 改动 `web/index.html`、`web/app.js`、关键 UI 结构时跑 Node tests
3. 涉及聊天流、地图、移动端安全区时，除了自动化测试还应手动过一遍页面

## 8. 当前工程风险

### 8.1 单文件过重

`web/app.js` 既是入口又是实现层，维护成本会持续上升。短期内可继续承载小步修改，但中长期应拆到至少按 chat / auth / trips / cities / map 分区。

### 8.2 前端现实与历史资产并存

仓库同时存在 `web/*` 和 `static/*.js` 两套前端痕迹。当前线上主路径明显偏向 `web/*`，但历史文件仍在仓库中，容易让新接手者误判“哪一套才是当前主实现”。

### 8.3 数据入口分散但未完全模块化

城市、FAQ、工具、签证、图片分别落在多个 JSON 文件和部分 Python 常量中；结构清晰，但并未形成统一的数据层 schema 约束，新增字段时容易前后端不一致。

### 8.4 Serverless 持久化能力有限

当前持久化核心是 SQLite。对本地和轻量验证足够，但在 Vercel serverless 场景下，`/tmp` 可写、实例生命周期短，天然不适合作为长期稳定主数据库。

### 8.5 外部服务可用性直接影响主体验

- DeepSeek 不可用时，Chat 主链路受影响最大
- 地图 key 缺失时，需要依赖 Leaflet fallback
- Google 登录配置不完整时，认证体验会分叉

### 8.6 产品文案与实际数据规模存在偏差风险

README 与页面文案中可见 33/36 城市表述并存，属于接手后应尽快核对的一类“非致命但会影响可信度”的一致性问题。

## 9. 接手第一周建议

### 第 1 天：建立真实运行认知

- 通读 `HANDOFF.md`、本文、`README.md`
- 本地启动服务并访问首页、聊天、地图、Trips、Cities、Tools、Admin
- 记录哪些是当前活跃路径，哪些只是历史遗留

### 第 2 天：跑通测试与关键接口

- 运行 `python3 -m unittest discover -s tests -v`
- 运行 `node --test web/tests/*.test.js`
- 手动调用 `/api/health`、`/api/config`、`/api/cities`、`/api/chat`、`/api/trips`

### 第 3 天：梳理数据与配置

- 核对 `data/*.json` 与前端展示字段是否对齐
- 核对 LLM、地图、Google、Admin、数据库路径等环境变量
- 明确本地、预览、线上三种环境下的配置差异

### 第 4-5 天：做低风险收敛

- 优先修正文案、数据映射、异常提示、空状态、测试稳定性这类低风险问题
- 暂时不要先做 `web/app.js` 大拆分，也不要马上替换数据库方案
- 如果要继续产品验证，优先保障登录、聊天、Trips、城市详情四条主路径稳定

### 第一周结束时建议形成的产物

- 一份“当前线上/预览环境实际依赖配置清单”
- 一份“主路径人工回归 checklist”
- 一份“`web/app.js` 可拆分边界草案”
- 一份“SQLite 在 serverless 下的替代路线评估”
