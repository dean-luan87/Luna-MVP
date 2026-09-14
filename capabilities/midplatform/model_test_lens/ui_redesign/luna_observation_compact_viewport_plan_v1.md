# Luna Observation Lens — Compact Viewport Plan V1

Phase: `Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Compact-Viewport-Planning-v1-001`  
Status: **Planning only** — no page implementation.

## 1. 核心问题

当前页面是**纵向报告流**（结论 → HUD → 洞察 → 问题 → 条形图 → 详细指标 → Debug），用户需滚动 **5 屏** 才能看完主要信息。

**Compact Viewport** 目标：将默认页面压缩为 **1 屏观察台**（最多 1.5 屏），用户无需长距离滚动即可同时看到：

- 主观察画面（HUD）
- 识别结果
- Luna 解释
- 核心指标摘要
- 高级/开发者入口（折叠）

> Luna Observation Lens 是观察台，不是报告页。

## 2. 与 UI Redesign 合并

本规划作为 **Luna Observation UI Redesign Execution** 的强制约束，执行阶段合并为：

`Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Compact-UI-Execution-And-Post-Review-v1-001`

## 3. 一屏仪表盘结构

```
┌──────────────────────────────────────────────────────────────┐
│ Luna Observation Lens   [选择文件] [开始观察] [HUD] [开发者] │
├───────────┬───────────────────────────────┬──────────────────┤
│ 能力栏     │        主观察画面              │ Luna 解释面板      │
│ 图像分割   │  原图 / 对比 / HUD（默认）      │ 当前任务           │
│ OCR       │                               │ 我看到了什么       │
│ SLAM      │  大图，占页面核心空间            │ 我不确定什么       │
├───────────┴───────────────────────────────┴──────────────────┤
│ 指标摘要：综合分 100% · 成功 20/20 · 主要风险：无显著失败      │
│ [指标详情] [高级流程] [开发者 JSON] [白盒链路]                │
└──────────────────────────────────────────────────────────────┘
```

## 4. 最大滚动深度

| 规则 | 值 |
|------|-----|
| 默认主要观察 | **1 屏内** |
| 小屏/低分辨率上限 | **1.5 屏** |
| 允许内部滚动 | 右侧解释面板、底部 drawer 内容 |
| 禁止 | 页面主体长滚动、指标条形图占整屏 |

## 5. 区域规格

| 区域 | 尺寸建议 | 内容 |
|------|----------|------|
| 顶部任务栏 | 64–88px 固定 | 标题、状态、文件、开始观察、视图切换、高级/开发者 |
| 左侧能力栏 | 220–260px | 文件摘要、能力卡片（可测试/实验中/未接入） |
| 中央观察区 | 55–65% 宽度 | 默认机器人视角 HUD，可切换原图/对比 |
| 右侧解释面板 | 300–380px | 五块压缩卡片，每块 1–3 条，内部滚动 |
| 底部指标摘要 | 72–120px | 综合分、成功/尝试、主要风险 + Tab/Drawer |

## 6. 信息收纳（见 compression rules）

结论、洞察、问题 → 右侧面板；条形图、详细指标 → 底部 drawer；manifest/job/JSON → 高级/开发者 drawer。

## 7. 禁止的页面形态

- 纵向堆叠：结论 → HUD → 洞察 → 问题 → 条形图 → 指标 → Debug
- 指标条形图默认占整屏
- raw JSON / manifest / job / bridge 默认显示
- 右侧说明空置而中间长滚动

## 8. Whitebox Slot

底部 drawer 或右侧 tab：**Luna 解释 | 白盒链路 | 指标 | 开发者**  
本阶段不接真实 runtime trace。

## 9. 治理边界

页面不执行模型；执行仅 8787 runner bridge；不写 fact/semantic/registry；不触发 navigation/speech。
