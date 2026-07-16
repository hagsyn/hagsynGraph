# Frontend Standards

## 1. Frontend Role

前端当前不是内容站点，也不是营销页，而是一个本地 Developer Tool / Workspace 壳。它的职责是：

- 承载产品级导航
- 展示工具目录
- 提供具体工具工作区
- 给出明确状态反馈
- 为后续知识模块预留稳定入口

所有前端改动都应优先维护这一定位。

## 2. Static Multi-File Rule

当前前端入口仍为 `frontend/index.html`，但不再把结构、样式、脚本堆在一个文件里。规范如下：

- 保持无构建静态前端，不引入打包器、框架或构建链
- `index.html` 负责产品壳与挂载点
- `assets/css/` 承接样式拆分
- `assets/js/` 使用浏览器原生 ES modules

推荐结构：

```txt
frontend/assets/js/
├── api/
├── state/
├── components/
├── views/
├── tools/
└── utils/
```

## 3. Product Shell First

当前页面采用统一产品壳，包含：

- 左侧导航
- 中央主工作区
- 主题切换
- 用户菜单
- Modal / Toast 状态反馈
- 管理员策略面板

新增功能时：

- 优先在现有壳中扩展
- 保持导航、标题、上下文与工作区整体一致性
- 不把单个功能做成脱离主壳的独立页面

## 4. Tools Workspace Pattern

`Tools` 是当前最重要的前端模块。标准交互模式为：

1. 工具列表展示真实可用工具
2. 用户点击进入具体工具工作区
3. 工作区内完成输入、执行、结果展示
4. 同页显示最近使用记录与结果下载入口

视频压缩、VTT 字幕生成、字幕烧录都应延续该模式，而不是另起一套交互体系。

## 5. State and API Split

前端默认采用以下分层：

- `config.js`: API 地址、主题、页面和工具常量
- `state/store.js`: 当前页面、当前工具、主题、结果态、用户态
- `api/**`: `fetch` 封装、工具接口、管理员接口
- `components/**`: modal、toast、theme switcher、user menu、settings panel
- `views/**`: dashboard / tools / nodes / graph / roadmaps
- `tools/**`: 各工具工作区模板
- `utils/**`: 路由、格式化、DOM 辅助

这样做的目的，是降低单文件脚本的职责堆叠，同时保持浏览器直接可运行。

## 6. State Feedback Standard

前端需要明确告诉用户当前处于什么状态：

- 等待输入
- 正在执行
- 已成功完成
- 执行失败

允许使用的主要反馈手段：

- 按钮 loading/disabled
- 结果卡片
- progress shell
- modal
- toast

避免只在控制台输出失败而界面无反馈。

## 7. Empty State Standard

当前 `Nodes / Graph / Roadmaps` 可以保留为空壳模块，但空状态必须诚实：

- 说明当前是预留模块
- 说明等待真实内容输入
- 给出下一步动作方向

不允许用伪数据制造“看起来很丰富”的假完成度。

## 8. API Integration Standard

前端通过固定 API 基址调用后端：

- 默认地址 `http://127.0.0.1:8000`
- 默认 token `hagsyn-local-dev-token`
- 可通过 `localStorage` 覆盖本地调试配置

规范如下：

- 所有业务请求统一带 `Authorization` header
- 上传或下载文件时保持接口路径清晰可追踪
- 管理员接口与工具接口分模块封装
- 新接口接入前先核对后端真实路由，不凭页面猜测

## 9. Safe Change Standard

前端改动默认执行以下自检：

- `node --check` 覆盖拆分后的所有 JS modules
- 前端壳测试或结构断言通过
- 页面中的工具状态、模块状态、按钮文案、结果文案与真实可用性一致

如果需要新增较复杂的工具交互，优先贴着现有模块边界扩展，而不是再次把所有逻辑并回 `app.js`。
