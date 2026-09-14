# Luna Observation Lens V1 Template Standard

**Standard ID:** `LunaObservationLensV1TemplateStandard`  
**Frozen:** 2026-07-02  
**Supersedes:** ad-hoc per-model test pages (planning intent only; no page deletion in closure phase)

## 定位

> 查看 Luna 如何看见、标注、判断和解释当前画面。

Luna Observation Lens V1 是所有 Model Test Lens 模型测试页面的 **默认 UI 模板**。新模型（Detection / OCR / SLAM / Depth / ASR / TTS / Speaker / VLM）必须复用本模板，仅通过 **model adapter slot** 扩展 HUD、对象胶囊与 drawer 内容。

## 布局（冻结）

```
┌─────────────────────────────────────────────────────────────┐
│ 顶栏：选择文件 · 开始观察 · 原图/对比/HUD · 更多 · 状态    │
├────┬──────────────────────────────────────┬───────────────┤
│左侧│           中央 HUD 主画面             │ Luna 观察面板 │
│抽屉│     线框 · 编号 · 短标签 · 置信度      │ 任务/观察/风险 │
├────┴──────────────────────────────────────┴───────────────┤
│ 对象胶囊条：① 路牌 · 80% · OCR  …（横向滚动）                │
├─────────────────────────────────────────────────────────────┤
│ 摘要：综合分｜成功｜风险/不确定｜仅模型评估                  │
│ Tab：指标｜对象｜高级｜开发者｜白盒｜记录（默认折叠）        │
└─────────────────────────────────────────────────────────────┘
```

## 七区组件契约

| 区域 | 模块 | 默认行为 |
|------|------|----------|
| 顶栏 | `luna_topbar_compact_actions_v1` | 单行；工程入口进「更多」 |
| 左侧 | `luna_left_capability_drawer_v1` + `luna_capability_grid_trigger_v1` | 窄栏 + 九宫格展开 |
| 中央 | `perception_hud_view_v1` + `hud_hidpi_renderer_v1` | HUD 最大区域；HiDPI |
| 胶囊 | `hud_object_chip_bar_v1` | 横向 chip；详情按需 |
| 右侧 | `hud_reasoning_compression_v1` | 结论优先；过程折叠 |
| 摘要 | `luna_bottom_drawer_tabs_v1` | 一行摘要 |
| Drawer | `luna_bottom_drawer_state_guard_v1` | fixed overlay；默认关闭 |

## 信息优先级（默认首屏）

1. 中央 HUD 主画面  
2. 图内编号 / 短标签  
3. 右侧整体判断  
4. 对象胶囊条  
5. 底部摘要  
6. Drawer 内容（点击后）

## 禁止默认展示

manifest · job request · runner bridge · envelope · adapter · artifact_ref · phase_ref · raw JSON · TestBoard 路径 · 完整推理过程 · 大对象详情卡片 · 指标条形图占主视口

## 治理边界

- candidate-only · 非运行态 · 非 fact · 非 semantic · 非 navigation · 非 speech  
- 页面不执行模型；执行仅经 `127.0.0.1:8787` Local Runner Bridge  
- 允许：canvas 渲染 · 本地 artifact 读取 · drawer 折叠 UI

## 后续模型接入

见 `luna_observation_lens_v1_model_adapter_slot_contract.json` 与 `closure/luna_observation_lens_v1_followup_routes.json`。

## 引用

- Model Test Lens UI Standard V1  
- Perception HUD UI Template Standard V1  
- `luna_observation_lens_v1_component_contract.json`
