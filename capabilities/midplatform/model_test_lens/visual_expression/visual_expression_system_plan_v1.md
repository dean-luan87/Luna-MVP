# Visual Expression System V1 — Planning Document

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-Planning-v1-001`  
**System ID:** `LunaModelTestLensVisualExpressionSystemV1`  
**Status:** Planning only（本阶段不实现 UI、不调用 runner、不改 attention engine、不改 schema）

## 上游

- Luna Observation Lens V1 Closure GO  
- Human Correction Layer UI Execution GO  
- Observation Attention Layer Planning GO + UI Execution GO  
- Observation Attention Overlay Semantic Separation Patch v1-002（已暴露表达混叠问题，本规划上升为体系层）

## 问题陈述

当前 Model Test Lens 图像区域出现 **表达混叠**：

1. **两套空间边界**：MobileSAM segmentation boundary 与 Observation Attention / selected / priority overlay 边界并存；点击右侧观察项时一层边界隐藏或变形，说明 UI 状态机将 segmentation 与 attention 混为一体。  
2. **图标化过度**：P0/P1 角标、小圆点、模型图标、编号并存但缺少自解释语义，审查效率低于可读短标签。

**核心判断：** 这不是「线条变淡」或「标签避让」问题，而是 **图形化表达体系未分层**。后续 Detection / OCR / Tracking / Depth / SLAM 接入时，若每模型层都在主图叠加框线，UI 将退化为调试噪声墙。

## 终结形态原则

| # | 原则 |
|---|------|
| 1 | **主图**只表达「区域在哪里」 |
| 2 | **右侧面板**表达「为什么优先看、优先级、后续用什么模型看」 |
| 3 | **底部摘要**表达「本帧整体观察调度结论」 |
| 4 | **hover / selected**表达「当前区域与记录如何对应」 |
| 5 | Observation Attention **不得**在主图绘制第二套完整 box / boundary |
| 6 | 不同模型层 **不得**同时在主图叠加各自框线系统 |

## 四层表达分工

```
┌─────────────────────────────────────────────────────────────┐
│ 主图 Canvas          │ 右侧 Panel        │ 底部 Dock       │
│ 空间定位              │ 观察判断           │ 全局摘要         │
│ segmentation owner   │ attention owner   │ scheduling stats │
└─────────────────────────────────────────────────────────────┘
         ▲ click/hover/selected 双向映射 ▲
```

### 主图（Canvas）— Segmentation Overlay Owner

- **唯一**空间边界 owner：`region_id` → 一条 segmentation boundary  
- 可显示：region 编号、P0/P1 轻量文字浮标（`① P0 道路`）  
- **不可**表达：priority 语义色框、route、tracking/OCR/depth 图标墙、完整原因、candidate_only 文案  
- selected：仅对 **已有** boundary 做描边增强 / mask 高亮，不新增、不隐藏、不 clone

### 右侧（Panel）— Observation Attention Primary Expression

- 「优先观察」队列为调度 **主入口**  
- 每条 record 与主图编号一致，包含：编号、priority、短标签、observation_type、为什么优先、recommended_followup_model、candidate_only / not_fact、correction boost 说明  
- 完整模型路线、长解释 **默认只在右侧**

### 底部（Dock）— Frame Scheduling Summary

- 示例：`本帧建议优先观察 4 个区域：P0 结构候选 2 个，P1 需跟踪复核 1 个，P1 静态候选 1 个。`  
- 不参与图像遮挡

### 交互（Interaction）— Mapping Layer

- 点击右侧 → 主图 region 高亮，boundary 不变  
- 点击主图 → 右侧滚动选中 record；无 record 时显示「该区域暂无优先观察建议」  
- hover 主图 → 一行轻量提示，非完整路线  
- hover 右侧 → 主图轻微高亮，不改变 segmentation visibility

## 视觉层 Owner 矩阵

| Layer | Canvas Boundary | Canvas Float Marker | Panel | Summary |
|-------|-----------------|---------------------|-------|---------|
| Segmentation (MobileSAM) | ✓ owner | 编号（可选） | 对象列表 | — |
| Observation Attention | ✗ | P0/P1 短浮标 | ✓ primary | ✓ |
| Follow-up Route | ✗ | hover/selected 一行 | ✓ full | — |
| Human Correction | ✗ | ✗ | boost 说明 | — |
| Detection/OCR/Tracking/Depth/SLAM（未来） | ✗ 默认 | 结果徽章（规划预留） | ✓ primary | 统计 |

## P0 / P1 / P2 / P3 展示策略

| 优先级 | 主图浮标（默认） | 右侧面板 | 底部摘要 |
|--------|------------------|----------|----------|
| P0 | ✓ 显示 | ✓ | ✓ 计入 |
| P1 | ✓ 显示 | ✓ | ✓ 计入 |
| P2 | ✗ 默认隐藏 | ✓ | 可选计入 |
| P3 | ✗ 默认隐藏 | ✓ | 通常忽略 |
| ignore | ✗ | 可选折叠 | ✗ |

用户开启「显示全部候选浮标」后，P2/P3 可在主图显示，但仍 **不得** 新增 boundary。

## 图标策略

- **禁止**图标作为默认主表达（无说明的圆点、字母 T/O/D、模型 glyph）  
- **允许**可读中文短标签：`① P0 路牌`、`④ P1 车辆 · 跟踪候选`  
- 若保留符号，必须有图例；当前阶段优先文字浮标

## 当前阶段裁剪（下一执行阶段）

见 `visual_expression_current_slice_v1.md`。本规划完成后，下一执行阶段仅做 Observation Attention visual expression correction，不接 runner。

## Schema / Policy 产物

| 文件 | 用途 |
|------|------|
| `schemas/visual_expression/visual_layer_ownership_policy_v1.json` | 层 owner 与 boundary 冲突规则 |
| `schemas/visual_expression/canvas_panel_interaction_policy_v1.json` | click/hover/selected 状态机 |
| `schemas/visual_expression/observation_attention_visual_expression_policy_v1.json` | Attention 图形表达格式 |
| `visual_expression_current_slice_v1.md` | 当前可执行剥离方案 |

## 禁止矩阵（规划期冻结）

- 不改 Observation Attention priority 计算  
- 不改 motion_state_candidate 规则  
- 不改 schema  
- 不调用 Detection/OCR/Tracking/Depth/SLAM runner  
- 不写 fact、不触发导航  
- 不把 prompt_label 升级为事实类别  
- 不把 Human Correction 升级为 ground truth  
- 不新增第二套图像空间边界系统  

## TestBoard

本阶段规划产物写入 TestBoard（`model_governance`），受 TestBoardProtectedArtifactRuleV1 保护，non-deletable。

## 推荐下一执行阶段

`Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-And-Post-Review-v1-001`

（在 Semantic Separation Patch v1-002 基础上，按本规划做体系级 UI 收口与 post-review）
