# Product Task Routing SOP

## 适用场景

当任务涉及产品方向、模块边界、UI 结构、工具接入、Knowledge 模块取舍或多步骤 Hagsyn 开发决策时使用。

## 前置检查

1. 识别当前任务是否属于 Hagsyn 产品开发主线
2. 判断任务主要落在哪些 lane：
   - `product`
   - `standards`
   - `ux`
   - `tools`
   - `knowledge`
   - `docs`
3. 确认是否需要读取现有文档与项目内 skill

## 执行步骤

1. 先读取：
   - `docs/product/**`
   - `docs/standards/**`
   - `docs/ux/**`
2. 判断当前变更优先影响的是：
   - 产品边界
   - 实现规则
   - 视觉/交互
3. 决定是否需要触发下层 skill：
   - 产品边界风险 -> `hagsyn-product-guard`
   - 前端工作区风险 -> `hagsyn-ui-workspace-pattern`
4. 决定执行顺序：
   - 先定边界
   - 再查标准
   - 再查 UX
   - 再决定写文档还是改代码
5. 若任务改动长期规则，先同步文档再声称对齐完成

## 自校验步骤

1. 是否已经明确任务所属 lane，而不是直接开干
2. 是否查阅了对应主线文档
3. 是否在需要时调用了下层 skill
4. 是否保持 `Tools` 为当前真实价值中心
5. 是否避免把 `Knowledge` 过早做重

## 常见失败点

- 直接改页面，不先查 `docs/ux/**`
- 直接扩展 Knowledge 模块，没有真实场景支撑
- 把产品做回 demo 驱动
- 忘记先同步文档就宣称方向已经稳定
