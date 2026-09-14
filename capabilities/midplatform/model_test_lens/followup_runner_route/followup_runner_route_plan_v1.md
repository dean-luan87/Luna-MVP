# Followup Runner Route Plan V1

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001`  
**System ID:** `LunaModelTestLensFollowupRunnerRouteV1`  
**Status:** Planning only（本阶段不调用 runner、不跑模型、不写 fact、不改 Visual Expression System）

## 上游

- Visual Expression System Planning GO + UI Execution GO + Post Review GO  
- Segmentation Boundary Contrast Restore GO（主图 boundary 视觉冻结）  
- Observation Attention Layer Planning GO + UI Execution GO  
- `followup_model_route_schema_v1.json`（route candidate 语义已定义）

## 问题陈述

Observation Attention 已能回答 **「哪里该看、为什么优先、建议用什么模型补测」**，但尚未定义：

> **什么条件下，允许将 followup_model_route_candidate 转为 runner_task_candidate？**

若跳过本规划直接接 Detection/OCR runner，极易退化为 **UI 按钮直连模型**，破坏中台治理与 Visual Expression System 分工。

## 核心链路（规划冻结）

```
Segmentation region (region_id, mask, prompt_label_candidate)
        ↓
Observation Attention record
  (priority_level, motion_state_candidate, ocr_required, tracking_required, …)
        ↓
followup_model_route_candidate  (per model_id, route_reason)
        ↓
runner_task_candidate           (admission-gated queue item)
        ↓
manual trigger / future scheduler trigger  (NOT in this phase)
        ↓
runner execution               (future phase only)
```

**本阶段终点：** `runner_task_candidate` 队列与准入策略定义完毕。  
**本阶段禁止：** runner 执行、模型调用、fact 写入、导航决策、自动触发。

## 与 Visual Expression System 的关系

| 层 | 职责 | 本阶段 |
|----|------|--------|
| 主图 Canvas | 空间定位（segmentation boundary） | **冻结，不修改** |
| 右侧面板 | 观察判断 + route 解释 | 只读 attention record |
| 底部摘要 | 本帧调度统计 | 不变 |
| Runner Route Queue | 任务候选队列（规划新增） | **本阶段定义** |
| Runner Execution | 模型执行 | **禁止** |

Follow-up route **不得**因本规划而在主图新增 boundary、图标墙或执行状态条。

## Route Candidate → Runner Task Candidate 映射

### 源：Observation Attention Record（已有）

| 源字段 | 用途 |
|--------|------|
| `attention_record_id` | 溯源 |
| `region_id` | 空间锚点 |
| `priority_level` | 队列准入 |
| `motion_state_candidate` | 路由规则 |
| `recommended_followup_model[]` | 展开为多条 route candidate |
| `followup_route_refs[]` | route 稳定引用 |
| `tracking_required` / `ocr_required` / `depth_required` / `detection_required` | 布尔门控 |
| `prompt_label_candidate` | **不得**升级为 fact |
| `_correction_boosted` | 仅提升 priority signal |
| `candidate_only` / `not_fact` | 任务候选边界 |

### 目标：Runner Task Candidate（本阶段新建 schema）

每条 `recommended_followup_model` 可生成 0..1 条 `runner_task_candidate`（按 admission policy 过滤）。

| 目标字段 | 来源 / 规则 |
|----------|-------------|
| `runner_task_candidate_id` | `rtc_{model_id}_{region_id}_{frame_ref}` |
| `source_attention_record_id` | `attention_record_id` |
| `source_region_id` | `region_id` |
| `target_model_id` | `detection` / `ocr` / `tracking` / `depth` / `slam` / … |
| `task_priority` | 映射自 `priority_level`（P0→P0, P1→P1, …） |
| `queue_admission` | `auto_eligible` / `manual_only` / `rejected` |
| `route_reason` | 由 mapping policy 推导 |
| `motion_state_candidate` | 透传，不得升级为 confirmed |
| `trigger_mode` | 默认 `manual_only`；禁止 `auto_execute` |
| `runner_task_candidate_only` | `true` |
| `not_runner_execution` | `true` |

## 模型路由规则（规划冻结）

### Detection

**服务：** object-like、label uncertain、correction boosted、dynamic/tracking 复核链  
**条件（任一）：**

- `detection_required === true`
- `motion_state_candidate` ∈ `{dynamic_candidate, needs_tracking_review}`
- `_correction_boosted === true` 且非纯 OCR 场景
- `prompt_label_candidate` 含 vehicle/sign/object 类且 confidence 偏低

**禁止：** 将 prompt_label 直接作为 detection ground truth 输入标签

### OCR

**服务：** static_candidate、text-likely region  
**条件（全部）：**

- `ocr_required === true`
- `motion_state_candidate` ∈ `{static_candidate, unknown_motion_state}`（单帧不得 confirmed_dynamic）
- region 标签含 sign / text / advertisement / screen

**禁止：** OCR 结果在本阶段写入 fact；单帧不得断言已确认文字内容

### Tracking

**服务：** needs_tracking_review、dynamic_candidate（多帧上下文）  
**条件：**

- `tracking_required === true`
- `motion_state_candidate` ∈ `{needs_tracking_review, dynamic_candidate}`
- `video_or_single_frame_context !== single_frame` **或** 标记为「需多帧复核候选」

**单帧：** 仅生成 `manual_only` 队列项，标注 `needs_multi_frame_review`

### Depth / SLAM

**服务：** road / walkable / structure candidate  
**条件：**

- `depth_required === true` 或 followup 含 `slam` / `slam_reference`
- `motion_state_candidate === scene_structure_candidate`
- 标签含 road / crosswalk / walkable / plane / building（building 偏 `slam_reference`）

## 队列准入（P0–P3）

| priority_level | 默认队列行为 |
|----------------|--------------|
| P0_immediate_attention | `auto_eligible` — 可进入默认任务候选队列 |
| P1_high_attention | `auto_eligible` |
| P2_medium_attention | `manual_only` — 仅面板展示 + 人工加入队列 |
| P3_low_attention | `manual_only` 或 `rejected`（默认不进入自动队列） |
| ignore_for_now | `rejected` |

**P2/P3 不得**在默认配置下自动触发 runner 任务生成（可手动 pin）。

## Human Correction 边界

- Correction 仅作为 **priority signal**（`_correction_boosted`）  
- 可提升 `task_priority` 与 `queue_admission` 至 `auto_eligible`  
- **不得**作为 ground truth、训练标签或 runner 输入 fact  
- 不得将 `motion_state_candidate` 从单帧升级为 `confirmed_dynamic`

## Runner Task Candidate ≠ Runner Execution

| 概念 | 含义 |
|------|------|
| `followup_model_route_candidate` | 「建议用什么模型看」— 观察调度输出 |
| `runner_task_candidate` | 「允许排入队列的任务草案」— 准入后产物 |
| `runner_job` / `runner_execution` | 真正调用模型 — **后续阶段** |

UI 未来可提供「加入补测队列」「手动触发」按钮，但必须经过 admission policy，且本阶段不实现。

## 当前切片（Planning Slice）

**包含：**

- 字段映射 schema + mapping policy + admission policy  
- 治理标准与 negative guards  
- 与现有 `ObservationAttentionEngine` 字段对齐（只读，不改 engine）

**不包含：**

- Detection/OCR/Tracking/Depth/SLAM runner 调用  
- 队列 UI、执行进度条、主图执行态  
- fact admission、navigation、output adapter  
- Visual Expression System 任何变更

## 推荐下一执行阶段

`Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001`

（队列面板 + 手动 pin + candidate 列表；仍不自动执行 runner）

## 验收（Planning）

1. route → task candidate 字段映射完整  
2. P0/P1 默认 `auto_eligible`，P2/P3 默认 `manual_only`  
3. OCR / Detection / Tracking / Depth-SLAM 路由规则可审计  
4. Human Correction 非 ground truth  
5. 全部 negative guards 通过  
6. 不改变 Visual Expression System
