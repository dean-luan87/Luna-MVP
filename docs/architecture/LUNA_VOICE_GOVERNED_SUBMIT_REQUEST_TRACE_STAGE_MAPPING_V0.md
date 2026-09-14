# Phase-Voice-OutputGovernance-008

# Governed Submit RequestTrace Stage Mapping v0

## 新增 stage（统一命名）

`request_trace.stage.output.voice.governed_submit_shadow_gate`

- **stage_namespace（key_fields）**：`voice_output_governance_v0`（与 Phase-005 一致）
- **短名（key_fields.stage_name）**：`governed_submit_shadow_gate`
- **完整名（key_fields.stage_name_full）**：与上行 `stage_name` 字段一致

## key_fields 最小集

| 字段 | 说明 |
|------|------|
| `source_submit_shadow_decision_id` | Phase-007 `submit_shadow_decision_id` |
| `source_governance_decision_id` | Phase-007 |
| `submit_gate_position` | `_maybe_submit_real_output_v1_pre` \| `VoiceOutputPlane.submit_entry` |
| `submit_shadow_result` | allowed / blocked / expired / cancelled / fallback_candidate（*_shadow） |
| `submit_allowed` | bool |
| `submit_block_reason` | 可空 |
| `hard_audit` | 含 `real_submit_invoked` 等不变量 |
| `whitebox_extension` | 解释 why_*（见主集成文档） |

## Whitebox 键

- `why_submit_allowed_shadow`
- `why_submit_blocked_shadow`
- `why_submit_expired_shadow`
- `why_submit_cancelled_shadow`
- `why_submit_fallback_candidate_shadow`
- `why_no_real_submit_invoked`
- `why_gate_position_safe`
