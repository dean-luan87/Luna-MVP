# Scene-Task Model Activation Governance Standard V1

**Standard ID:** `SceneTaskModelActivationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Scene-Task-Model-Activation-Planning-v1-001`  
**Also known as:** Model Work Admission Layer

## 目的

规划 **Scene-Task Model Activation** 层：中台在模型执行前先判断场景与任务，决定哪些模型有资格出场、哪些必须 no-op，避免 SAM / OCR / Detection / SLAM / VLM / Depth / Tracking 无差别同时动作。

**核心原则：** 不是模型看到图就工作，而是**中台批准模型在某个区域为某个任务工作**。

## 上游 GO

- Text-First Target Proposal Validation Planning GO  
- Dual Route Perception Validation Execution GO  
- Scene-Aware Segmentation Prompt Policy Execution GO  
- MobileSAM Single Model Execution Integration GO  

## 冻结链路

```
Image → scene_profile_candidate → task_intent_candidate
  → model_activation_plan_candidate → model_region_assignment
  → followup_runner_task_candidate
```

## 模型工作边界（摘要）

| 场景 / 任务 | 应激活 | 不应激活 |
|-------------|--------|----------|
| 店招 / 广告牌 | OCR text detector + recognizer | SLAM / Tracking / Depth 默认 |
| 地铁导视 | OCR；Detection 可选（安全） | SLAM 除非 navigation/spatial continuity |
| 街道路口 | Detection / Depth / Tracking；OCR 仅标识区 | 不全图 OCR |
| 走廊 / 路径 | Depth / SLAM | OCR 除非有文字区 |
| unknown | VLM route enhancer | 其他 pending / manual_review |

## 核心边界

- **场景决定任务候选；任务决定模型激活**  
- **文字任务不默认触发 SLAM**（`no_slam_for_text_task`）  
- **空间任务不默认触发 OCR**  
- **每个激活模型必须有 `activation_reason` 和 region assignment**  
- **每个未激活模型必须有 `noop_reason`**  
- **model_activation_plan_candidate ≠ fact**  
- **本阶段不接 runner、不写 fact、不做导航决策**（`no_navigation_decision`）  

## Negative Guards

- `no_slam_for_text_task`  
- `no_slam_text_detection`  
- `text_only_scene_activates_ocr_not_slam`  
- `shopfront_sign_noops_slam`  
- `subway_direction_sign_noops_slam_unless_navigation`  
- `noop_record_required_for_inactive_models`  
- `active_model_requires_activation_reason`  
- `active_model_requires_region_assignment`  
- `inactive_model_must_not_generate_task`  
- `no_blanket_model_activation`  
- `no_fact_write`  
- `no_runner_execution_in_planning`  
- `browser_runtime_guard_inherited`  

## 本阶段允许

- 规划 schema / policy / smoke / review  
- deterministic activation stub  
- UI 规划文档（不实现）  

## 本阶段禁止

- 真实 OCR / Detection / SLAM / VLM runner 执行  
- 写 fact / 导航决策  
- 全模型 blanket activation  
- 改变 Visual Expression boundary owner  

## 下一阶段

`Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001`
