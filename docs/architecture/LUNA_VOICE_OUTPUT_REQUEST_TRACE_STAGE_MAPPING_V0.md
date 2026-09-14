# Phase-Voice-OutputGovernance-005
# Voice Output Request Trace Stage Mapping v0（阶段映射）

**目标**：定义 `voice_output_governance_v0` → `request_trace.stage.voice_output.*` 的 stage 映射规则，确保 governance 阶段进入统一请求链视图。

---

## 1. 映射规则（固定）

- `voice_output_governance_v0.candidate_input`
  → `request_trace.stage.voice_output.candidate_input`
- `voice_output_governance_v0.speakable_guard`
  → `request_trace.stage.voice_output.speakable_guard`
- `voice_output_governance_v0.speech_gate`
  → `request_trace.stage.voice_output.speech_gate`
- `voice_output_governance_v0.expiry_check`
  → `request_trace.stage.voice_output.expiry_check`
- `voice_output_governance_v0.stale_check`
  → `request_trace.stage.voice_output.stale_check`
- `voice_output_governance_v0.cancellation_check`
  → `request_trace.stage.voice_output.cancellation_check`
- `voice_output_governance_v0.priority_check`
  → `request_trace.stage.voice_output.priority_check`
- `voice_output_governance_v0.interruption_check`
  → `request_trace.stage.voice_output.interruption_check`
- `voice_output_governance_v0.suppression_check`
  → `request_trace.stage.voice_output.suppression_check`
- `voice_output_governance_v0.provider_health_check`
  → `request_trace.stage.voice_output.provider_health_check`
- `voice_output_governance_v0.final_governance_decision`
  → `request_trace.stage.voice_output.final_governance_decision`
- `voice_output_governance_v0.audit_envelope`
  → `request_trace.stage.voice_output.audit_envelope`

---

## 2. stage key_fields 最小要求

每个 stage 的 `key_fields` 应至少包含：

- `stage_namespace`
- `stage_name`
- `stage_order`
- `adapter_status`
- `adapter_reason`
- `decision_ref`
- `audit_envelope_ref`
- `hard_audit`
- `whitebox_extension`

