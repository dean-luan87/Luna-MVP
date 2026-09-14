# Scene-Task Model Activation Plan V1

**Phase:** `Phase-P1-Midplatform-Scene-Task-Model-Activation-Planning-v1-001`  
**System ID:** `LunaMidplatformSceneTaskModelActivationPlanningV1`  
**Also known as:** Model Work Admission Layer  
**Status:** Planning only（不接模型、不跑 runner、不写 fact）

## 背景

治理链已建立 Observation → Attention → Task Candidate → Admission → Execution，但**模型调度不够克制**：

```
错误：Image → SAM / OCR / SLAM / Detection / VLM 全部试一遍
正确：Scene → Task → Model Activation → Region Assignment → Controlled Execution
```

**核心规则：** 不是模型看到图就工作，而是**中台批准模型在某个区域为某个任务工作**。

## 上游 GO

| 基线 | 决策 |
|------|------|
| Text-First Target Proposal Validation Planning | GO |
| Dual Route Perception Validation Execution | GO |
| Scene-Aware Segmentation Prompt Policy Execution | GO |
| MobileSAM Single Model Execution Integration | GO |

## 冻结链路

```
Image / Frame
  ↓
scene_profile_candidate
  ↓
task_intent_candidate
  ↓
model_activation_plan_candidate   ← 本阶段终点
  ↓
model_region_assignment
  ↓
followup_runner_task_candidate（未来受控执行）
```

## 三类输入 → 两类输出

**输入：** scene_profile、task_intent、observation_attention、region/text candidates、user_goal（可选）

**输出：**
- `activated_model_set` — 有资格出场的模型
- `model_noop_set` — 必须 no-op 的模型 + `noop_reason`
- `model_region_assignment` — 激活模型绑定的区域

## 模型工作边界（摘要）

| 场景 / 任务 | 应激活 | 不应激活 |
|-------------|--------|----------|
| 店招 / 广告牌 | OCR text detector + recognizer | SLAM / Tracking / Depth 默认 |
| 地铁导视 | OCR（导视区）；Detection 可选（人/门） | SLAM 除非 spatial continuity |
| 街道路口 | Detection / Depth / Tracking；OCR 仅标识区 | 不全图 OCR |
| 走廊 / 路径 | Depth / SLAM | OCR 除非有文字区 |
| unknown | VLM route enhancer | 其他 pending / manual_review |

**铁律：**
- 文字任务不默认触发 SLAM（`no_slam_for_text_task`）
- 空间任务不默认触发 OCR
- 每个激活必须有 `activation_reason`
- 每个未激活必须有 `noop_reason`

## Scene Profile Candidate

支持：`text_signage_scene`、`subway_platform`、`shopfront_sign`、`outdoor_street_crossing`、`indoor_navigation`、`corridor`、`unknown_scene`

## Task Intent Candidate

支持：`read_text`、`find_direction`、`identify_object`、`assess_walkable_area`、`track_dynamic_target`、`understand_scene`、`locate_place`、`manual_review`

## Smoke Cases（5）

| Case | 输入 | 预期 |
|------|------|------|
| A 店招 | 阿叔阿姨的店 | shopfront_sign + read_text → OCR activate；SLAM/Tracking/Depth no-op |
| B 地铁导视 | 嘉会湖站台 | subway + read_text/find_direction → OCR；SLAM no-op unless navigation |
| C 街道路口 | 街景 | assess_walkable + track → Detection/Depth/Tracking；OCR 仅 sign 区 |
| D 空间导航 | corridor | Depth/SLAM activate；OCR no-op unless text region |
| E unknown | 未知 | VLM route；其他 pending；no fact |

## UI 规划（本阶段不实现）

右侧「模型激活计划」：Activated / No-op / Region Assignment / reasons / candidate_only

## 本阶段禁止

- 真实 runner 执行（OCR / Detection / SLAM / VLM）
- 写 fact / 导航决策
- 全模型 blanket activation
- 改变 Visual Expression boundary owner（`no_visual_expression_mutation`）

## 下一阶段

`Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001`
