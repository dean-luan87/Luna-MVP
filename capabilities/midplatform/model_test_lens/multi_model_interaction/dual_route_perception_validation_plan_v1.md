# Dual Route Perception Validation Plan V1

**Phase:** `Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Planning-v1-001`  
**System ID:** `LunaMidplatformDualRoutePerceptionValidationPlanningV1`  
**Status:** Planning only（不接真实模型、不写 fact、不改现有 MobileSAM/OCR runner 治理链）

## 背景

MobileSAM 固定语义 prompt 在跨场景时不稳定（地铁站图误标行人/地面）。根因是 SAM 不适合作为跨场景语义分类器。前置区域发现机制不稳时，继续接真实 OCR 会被错误区域拖死。

本阶段规划 **双路线对照验证框架**，决定后续优先接 Grounding、OCR text detector，还是 VLM route enhancer。

## 上游 GO

| 基线 | 决策 |
|------|------|
| Scene-Aware Segmentation Prompt Policy Planning | GO |
| MobileSAM Single Model Execution Integration | GO |
| MobileSAM → OCR Runner Sandbox Integration Execution | GO |
| Observation Attention Layer Planning | GO |

## 核心决策

1. **不使用 SLAM 找文字** — SLAM 不承担文字定位、识别、语义判断  
2. **文字相关任务**由 OCR text detector / Detection-Grounding / VLM route candidate 承担  
3. **SAM / MobileSAM** 仅作 region proposal 或 mask refine  
4. **VLM** 仅作 route candidate / attention candidate 来源，不写 fact  
5. **Route A 与 Route B 并行验证**，角色不同、互为对照组，非互斥  

| 方案 | 角色 | 偏向 |
|------|------|------|
| Route A | Detector / Grounding → SAM refine | 工程可控、结构化 |
| Route B | VLM → Midplatform route candidate | 语义适应、跨场景 |

## 本阶段终点

**dual_route_comparison_candidate** — 中台对 Route A / Route B 的比较候选，不是 fact，不触发 runner。

## 冻结链路

```
Image
  ├─ Route A: grounding_detection_candidate → bbox_candidate → sam_refine_mask_candidate
  └─ Route B: vlm_observation_candidate → scene_profile_candidate → attention_route_candidate
        ↓
  Midplatform Dual Route Comparison
        ↓
  dual_route_comparison_candidate   ← 本阶段终点
        ↓
  next_task_candidate（OCR / Detection / SAM — 未来受控执行）
```

## Route A：Detector / Grounding → SAM

```
Image → grounding_detection_candidate → bbox_candidate → sam_refine_candidate
      → mask_candidate → midplatform_route_candidate
```

**输出对象：** `grounding_detection_candidate`、`detected_region_candidate`、`bbox_candidate`、`sam_refine_mask_candidate`

**适合验证：** direction_sign、station_name_board、advertisement_panel、screen_door、person、vehicle、door、warning_line

**禁止：** detected_label 写 fact、grounding prompt 升级类别、SAM mask 升级对象、Route A 直调 OCR / navigation

## Route B：VLM → Route Candidate

```
Image → vlm_observation_candidate → scene_profile_candidate → attention_route_candidate
      → midplatform_route_candidate
```

**允许：** VLM 建议「该区域可能值得 OCR」「地铁站场景候选」「上方导视牌值得观察」  
**禁止：** VLM 确认路牌/文字、直调 OCR runner、直触发 navigation

## No-SLAM-for-Text Policy

见 `schemas/multi_model_interaction/no_slam_for_text_policy_v1.json`

| SLAM 允许 | SLAM 禁止 |
|-----------|-----------|
| spatial_reference_candidate | text_detection |
| walkable_area_reference | text_recognition |
| structure_reference | sign_identification |
| pose / map / geometry | OCR route direct generation |

## Midplatform Dual Route Comparison

比较维度：region_overlap、text_likelihood、route_agreement、route_conflict、trace_completeness、uncertainty、recommended_next_task

**禁止：** comparison 直接写 fact / 确认类别 / 确认文字 / 执行 OCR

### 对照示例

| 情况 | 处理 |
|------|------|
| Route A direction_sign bbox + Route B 上方导视牌 OCR 建议，区域重叠 | OCR task candidate priority +1 |
| Route A 漏检 sign，Route B 建议上方 OCR | manual_review / low_confidence candidate |
| Route A person vs Route B sign area 冲突 | conflict_candidate，降低自动准入 |

## Smoke Cases（4）

| Case | 输入 | 预期 |
|------|------|------|
| **A** 地铁站导视牌 | 嘉会湖站台图 | Route A direction_sign bbox；Route B subway + top sign OCR route；comparison → OCR task candidate；不执行 OCR |
| **B** 户外街景 | 街景图 | Route A sign/vehicle/ad；Route B road/sign/vehicle routes；comparison → OCR/Detection/Depth candidates |
| **C** A 漏检 B 命中 | 合成漏检 | 不信任 VLM；manual_review / low_confidence；不执行 OCR |
| **D** A/B 冲突 | person vs sign | conflict_candidate；降低准入；需复核 |

## UI 规划（本阶段不实现）

未来右侧「路线对照候选」：Route A 输出 / Route B 输出 / 中台 agreement-conflict。主图不新增两套 box，默认进右侧，选中时高亮。

## 本阶段禁止

- 真实 Detection / Grounding / VLM / OCR / SLAM runner 调用  
- 写 fact / 导航决策  
- 改变 MobileSAM/OCR runner sandbox 架构  
- VLM / Detector 输出升级 fact  
- SLAM 参与文字定位  

## 产出

见 `schemas/multi_model_interaction/` 与 `multi_model_interaction/dual_route_perception_types_v1.py`

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Execution-v1-001`
