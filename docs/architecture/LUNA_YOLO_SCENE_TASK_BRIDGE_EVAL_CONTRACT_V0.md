# LUNA — YOLO Shadow SceneTask Bridge Evaluation Contract v0 (Phase-ModelPerception-007)

## Scope
本 contract 仅约束 **离线桥接评测产物**，不产生任何 runtime 接入效力。

## Inputs (required)
每条样本输入必须来自：
- `perception_runtime_mode == "yolo_shadow_replacement"`（Phase-ModelPerception-006）

并保持证据边界：
- evidence_type == `phone_local_controlled_capture`
- controlled_live_stream == false
- phone_local_capture == true

## Outputs (required)
每条样本输出必须包含：
- `scene_state`（dict）
- `task_candidates`（list[dict]）
- `scene_type` / `scene_phase` / `scene_confidence`
- `task_candidate_count`

### scene_state minimum schema (hard)
`scene_state` 至少包含以下字段：
- scene_id
- scene_type
- scene_confidence
- scene_phase
- active_task_id
- task_status
- degraded_mode
- required_perception_signals（必须包含 5 类 perception signals）
- last_transition_reason

### task_candidate minimum schema (hard)
每个 candidate 必须包含：
- task_candidate_id
- task_type
- source_scene_id
- source_signal_ids
- confidence
- reason_codes
- allows_execute_now

## Candidate-only / safety (hard)
- 每个 task_candidate 必须 `allows_execute_now == false`
- 评测结果必须保持零泄漏：
  - execute leakage == 0
  - default-on leakage == 0
  - release/retry/reopen leakage == 0
  - forced_navigation_action_count == 0

## Unsupported capabilities respected (hard)
桥接评测不得“假装”下游已得到支持能力：
- OCR / dynamic 必须仍按 not_available 保守处理
- depth_unavailable / collision_risk_not_confirmed 必须被保守处理

## Non-goals (explicit)
- 不进入 Fusion/Output
- 不执行导航动作、不真实播报
- 不证明真实导航能力
- 不宣称 SceneContext gates 已 runtime 完整 enforce

