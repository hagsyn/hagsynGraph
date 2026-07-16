# 2026-07-16 前端国际化测试报告

## 范围

本轮覆盖 Hagsyn 前端首版国际化能力：

1. `zh-CN / en` 双语支持
2. 浏览器语言默认判定
3. 顶栏语言切换控件
4. `localStorage` 语言持久化
5. 登录页、工具目录、工具工作区、用户菜单、设置面板等核心前端文案切换

本轮不包含：

- 后端接口错误文案国际化
- API schema 变化
- 数据库或认证逻辑变更

## 实现摘要

### 1. 新增前端 i18n 基础设施

- 新增 `frontend/assets/js/i18n/messages.js`
- 新增 `frontend/assets/js/i18n/index.js`
- 新增 `localStorage` 键：`hagsyn_locale`

### 2. 前端壳层接线

- 顶栏新增 `languageSwitcher`
- 导航、页面标题、副标题、主题切换、用户菜单、设置面板改为走字典文案

### 3. 工具工作区与状态保留

- `video-compress`
- `vtt-subtitle`
- `video-subtitle-burn`

切换语言后继续保留：

- 当前路由
- 当前打开的工具工作区
- 最近的结果卡片状态

同时补了本地前端状态字段，用于保留当前选择的模式/语言和已选文件名展示。

## 新增/更新的自动测试

### 前端结构检查

- 扩展 `frontend/tests/ui-shell.test.js`
  - 校验 `languageSwitcher` 挂载点
  - 校验 `assets/js/i18n/index.js`
  - 校验 `assets/js/i18n/messages.js`
  - 校验 `app.js` 已接入 locale 渲染与切换逻辑

### 前端行为测试

- 新增 `frontend/tests/i18n.test.mjs`
  - `zh-TW -> zh-CN`
  - 非中文浏览器语言 -> `en`
  - 本地持久化值优先
  - 非法持久化值回退
  - `setLocale()` 同步 `document.documentElement.lang`
  - `t(key, params)` 基本取值、插值和缺 key 回退

### 既有前端配置测试

- 继续验证 `frontend/tests/config.test.js`

## 执行结果

### 语法检查

运行：

```bash
find frontend/assets/js -name '*.js' -print0 | xargs -0 -n1 node --check
```

结果：

- 通过

### 前端结构测试

运行：

```bash
node frontend/tests/ui-shell.test.js
```

结果：

- `ui shell test passed`

### 前端 i18n 行为测试

运行：

```bash
node frontend/tests/i18n.test.mjs
```

结果：

- `i18n test passed`

### 前端配置测试

运行：

```bash
node frontend/tests/config.test.js
```

结果：

- `config test passed`

## 浏览器交互验证

验证时间：

- 2026-07-16

验证地址：

- `http://127.0.0.1:5173/?v=frontend-i18n-20260716`

### 登录页验证

验证项：

1. 页面可正常打开
2. 顶栏出现语言切换控件
3. 默认中文界面可见
4. 点击 `EN` 后：
   - 登录页标题切到英文
   - 顶栏文案切到英文
5. 页面刷新后：
   - 英文选择保留

结果：

- 通过

### 已登录工具页验证

验证路径：

1. 使用默认账号 `hagsyn / hagsyn123` 登录
2. 进入 `#tools/video-compress`
3. 点击 `中文`

验证项：

1. 登录成功后可进入 `Dashboard`
2. `#tools/video-compress` 可打开
3. 切换语言后仍停留在当前工具工作区
4. `视频压缩` 工作区按钮和标题同步变为中文

结果：

- 通过

## 当前状态

- 前端首版 i18n 已接入
- 登录壳、工具目录、三个真实工具工作区、用户菜单和设置面板已纳入双语切换
- 默认语言、手动切换与刷新保持已验证

## 当前限制

1. 后端错误消息仍保持原有返回，不做 locale 化
2. 当前只支持 `zh-CN` 与 `en`
3. 切换语言时使用整体重渲染策略，未引入更细粒度的局部文本替换机制
