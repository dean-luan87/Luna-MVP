# Followup Runner Route Governance Standard V1

**Standard ID:** `FollowupRunnerRouteGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001`

## 定位

将 Observation Attention 的 **followup_model_route_candidate** 规划为 Detection/OCR/Tracking/Depth/SLAM **runner 任务候选队列** 的来源。本阶段终点为 `runner_task_candidate`，不是 runner 执行。

## 核心边界

| 概念 | 允许 | 禁止 |
|------|------|------|
| followup_model_route_candidate | 观察输出 | 立即执行 |
| runner_task_candidate | 队列草案 | 等同 runner job |
| runner execution | — | 本阶段 |
| auto runner trigger | — | 默认禁止 |
| Human Correction | priority signal | ground truth |
| prompt_label | candidate | fact 类别 |

## Schema 注册

| Schema | Path |
|--------|------|
| Runner Task Candidate | `schemas/followup_runner_route/followup_runner_task_candidate_schema_v1.json` |
| Route Mapping Policy | `schemas/followup_runner_route/runner_route_mapping_policy_v1.json` |
| Route Admission Policy | `schemas/followup_runner_route/runner_route_admission_policy_v1.json` |

## 队列准入

- P0 / P1 → `auto_eligible`
- P2 / P3 → `manual_only`
- ignore_for_now → `rejected`

## Visual Expression 保护

不得修改主图 boundary、不得恢复 Attention 第二套 box、不得在主图展示 runner 执行态。

## Negative Guards

`no_runner_execution`, `no_model_call`, `no_fact_write`, `no_navigation_decision`, `no_auto_runner_trigger`, `no_human_correction_ground_truth`, `no_prompt_label_fact_upgrade`, `no_motion_confirmed_from_single_frame`, `no_visual_expression_mutation`
