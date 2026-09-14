# Runner Manual Trigger Governance Standard V1

**Standard ID:** `RunnerManualTriggerGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-Planning-v1-001`

## 定位

规划从 **pinned `runner_task_candidate`** 到 **`runner_invocation_request`** 的手动触发链路，为 Detection / OCR runner 接入建立执行前准入门禁。本阶段终点为 `runner_invocation_request`，不是 runner 执行。

## 三层关系（不可混用）

| 层 | 语义 | 本阶段 |
|----|------|--------|
| `runner_task_candidate` | 可以考虑做什么 | 上游 GO |
| `runner_invocation_request` | 准备申请执行什么 | **本阶段规划** |
| `runner_execution` | 真正跑模型 | **禁止** |

## Schema 注册

| Schema | Path |
|--------|------|
| Runner Invocation Request | `schemas/runner_manual_trigger/runner_invocation_request_schema_v1.json` |
| Manual Trigger Admission | `schemas/runner_manual_trigger/manual_runner_trigger_admission_policy_v1.json` |
| Detection/OCR Route Policy | `schemas/runner_manual_trigger/detection_ocr_manual_trigger_route_policy_v1.json` |

## 准入门禁

- 仅 **pinned** `runner_task_candidate` 可生成 request  
- `excluded` / `blocked_by_policy` 禁止  
- `stale_candidate` 须重新确认  
- `candidate` 须先 pin  
- Detection request ↔ detection route；OCR request ↔ ocr route  
- 禁止 bypass task candidate  

## 状态边界

**admission_status:** `pending_admission` | `admitted` | `rejected` | `cancelled`  
**execution_status（本阶段）：** 仅 `not_executed`  
**禁止：** `running`, `executed`, `completed`, `fact_written`, `navigation_decided`

## Visual Expression 保护

不得因 request 规划修改主图 boundary、不得新增 runner box、不得在 canvas 展示执行态。

## 浏览器守卫继承

- `app.js` 禁止裸 `global`  
- `browser_runtime_guard_v1.js` 继续有效  
- 未来 UI 实现须使用 `window.xxx`

## Negative Guards

`no_runner_execution`, `no_model_call`, `no_fact_write`, `no_navigation_decision`, `no_auto_runner_trigger`, `no_running_state_allowed`, `no_executed_state_allowed`, `no_completed_state_allowed`, `invocation_request_not_execution`, `invocation_request_requires_pinned_task_candidate`, `excluded_task_cannot_generate_request`, `stale_task_requires_reconfirmation`, `blocked_task_cannot_generate_request`, `no_orphan_invocation_request`, `request_traceable_to_runner_task_candidate`, `request_traceable_to_attention_record`, `request_traceable_to_region_id`, `detection_request_requires_detection_route`, `ocr_request_requires_ocr_route`, `no_prompt_label_fact_upgrade`, `no_human_correction_ground_truth`, `no_motion_confirmed_from_single_frame`, `candidate_only_not_executed_not_fact_preserved`, `no_visual_expression_mutation`, `browser_runtime_guard_inherited`
