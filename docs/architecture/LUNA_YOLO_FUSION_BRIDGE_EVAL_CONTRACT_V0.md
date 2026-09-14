# LUNA — YOLO Shadow Fusion Bridge Evaluation Contract v0 (Phase-ModelPerception-008)

## Scope
本 contract 仅约束 **离线 Fusion bridge 评测产物**，不产生任何 runtime 接入效力。

## Inputs (required)
每条样本输入必须来自 Phase-ModelPerception-007，并至少包含：
- `scene_state`（含 `scene_id`）
- `task_candidates`（含 `task_candidate_id/task_type/allows_execute_now`）
- 证据边界布尔：
  - evidence_type_preserved=true
  - controlled_live_stream_false=true
  - phone_local_capture_true=true

## Outputs (required)
每条样本必须生成：
- `fusion_decision_candidate`（dict）

### fusion_decision_candidate minimum schema (hard)
必须包含：
- fusion_candidate_id
- fusion_candidate_type
- confidence
- source_scene_id
- source_task_candidate_ids
- source_signal_ids
- source_attribution（必须包含上游 root + runtime_mode + yolo_source 元信息）
- conflict_detected / conflict_type / conflict_resolution
- degraded_or_uncertain_handling（结构存在）
- reason_codes
- allows_execute_now

## Candidate-only / safety (hard)
- `fusion_decision_candidate.allows_execute_now == false`
- 评测结果必须保持零泄漏：
  - execute leakage == 0
  - default-on leakage == 0
  - release/retry/reopen leakage == 0
  - side effects expansion == 0
  - forced_navigation_action_count == 0

## Source attribution (hard)
必须保留最小可追溯性：
- `source_scene_id` 非空
- `source_task_candidate_ids` 至少包含被选择的 task_candidate_id（非空列表）
- `source_attribution.yolo_source` 至少包含：
  - yolo_invoked
  - detection_count
  - detected_classes

## Conflict / degraded handling (hard-structure)
不要求冲突一定发生，但必须有结构字段：
- conflict_handling present（或等价结构）
- degraded_or_uncertain_handling present

## Non-goals (explicit)
- 不进入真实 Output runtime
- 不执行导航动作、不真实播报
- 不证明真实导航能力
- 不宣称融合策略已充分验证（v0 仅最小规则）

