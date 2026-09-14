# Visual Expression System Governance Standard V1

**Standard ID:** `VisualExpressionSystemGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-Planning-v1-001`

## 定位

Visual Expression System 为 Luna Model Test Lens 建立 **图形化表达分层体系**，防止分割、观察调度、后续模型结果在主图相互打架。

```
主图 = 空间定位 ｜ 右侧 = 观察判断 ｜ 底部 = 全局摘要 ｜ 交互 = 区域↔记录映射
```

## 核心规则

1. Segmentation 是 canvas **唯一** boundary owner。  
2. Observation Attention 是 annotation layer，**不画**第二套 box。  
3. Follow-up route 默认在 panel 展开，不在主图默认堆叠。  
4. Human Correction 仅 priority signal，不新增 canvas 框线，不升级 ground truth。  
5. 未来 Detection/OCR/Tracking/Depth/SLAM runner 默认 panel-first，不默认叠加 canvas boundary。  
6. 图标不可作为默认主表达；必须可读短标签或右侧解释。  
7. candidate_only / not_fact 约束保留在 panel/summary，不在主图重复。  
8. 单帧不得 confirmed_dynamic 图形断言。

## Negative Guard 矩阵（规划期）

| Guard | 含义 |
|-------|------|
| no_runner_execution | 交互不触发 runner |
| no_fact_write | 不写 fact |
| no_navigation_decision | 不做导航决策 |
| no_boundary_clone | 不 clone segmentation boundary |
| no_secondary_box_from_attention | Attention 不画第二套 box |
| no_ground_truth_from_human_correction | 纠错非 ground truth |
| no_prompt_label_fact_upgrade | prompt_label 不升级事实 |
| no_motion_confirmed_from_single_frame | 单帧不 confirmed_dynamic |

## Schema 注册

| Schema | Path |
|--------|------|
| Layer Ownership | `schemas/visual_expression/visual_layer_ownership_policy_v1.json` |
| Canvas-Panel Interaction | `schemas/visual_expression/canvas_panel_interaction_policy_v1.json` |
| Attention Visual Expression | `schemas/visual_expression/observation_attention_visual_expression_policy_v1.json` |

## 下游

- Visual Expression System UI Execution（收口 Semantic Separation Patch）  
- Detection/OCR Runner 接入须遵守 layer ownership  
- TestBoard protected artifacts
