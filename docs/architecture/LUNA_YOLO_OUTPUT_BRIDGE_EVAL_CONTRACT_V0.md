# LUNA — YOLO Shadow Output Bridge Evaluation Contract v0 (Phase-ModelPerception-009)

## Scope
本 contract 仅约束 **离线 Output bridge 评测产物**，不产生任何 runtime 接入效力。

## Inputs (required)
每条样本输入必须来自 Phase-ModelPerception-008，并至少包含：
- `fusion_decision_candidate`（含 `fusion_candidate_id`）
- `source_attribution`（含 yolo_source 或可追溯到 yolo_source）
- 证据边界布尔：
  - evidence_type_preserved=true
  - controlled_live_stream_false=true
  - phone_local_capture_true=true

## Outputs (required)
每条样本必须生成：
- `navigation_output_candidate`（dict）

### navigation_output_candidate minimum schema (hard)
必须包含：
- output_candidate_id
- source_fusion_candidate_id
- source_type
- output_type
- priority
- message_template_id
- message_text_candidate
- generated_at_ms
- expires_at_ms
- validity_window_ms
- repeat_policy
- suppression_reason
- requires_user_confirmation
- requires_human_help
- confidence
- source_attribution（必须保留 yolo_source）
- reason_codes
- allows_execute_now
- real_tts_invoked

## Timing / priority / suppression (hard-structure)
必须提供 timing/priority/suppression 结构字段（不要求策略最优）：
- validity_window_ms > 0
- expires_at_ms > generated_at_ms
- priority 属于有限集合（critical/high/medium/low/silent）
- suppression_reason 为字符串
- repeat_policy 为字符串

## Candidate-only / No-real-TTS (hard)
- allows_execute_now == false
- real_tts_invoked == false

## Safety boundary (hard)
必须保持零泄漏，且禁止语义扫描为 0：
- execute/default-on/release-retry-reopen/side-effects/forced_action leakage == 0
- forbidden_output_semantic_count == 0

## Source attribution (hard)
必须保留最小可追溯性：
- source_fusion_candidate_id 非空
- source_attribution_present
- yolo_detection_source_preserved（yolo_invoked/detection_count/detected_classes 存在）

## Non-goals (explicit)
- 不进入真实 TTS / Output runtime
- 不执行导航动作、不真实播报
- 不证明真实导航能力
- 不宣称输出策略已充分验证（v0 仅最小规则）

