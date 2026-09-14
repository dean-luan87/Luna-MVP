# LUNA 主线 Runtime Wiring Candidate Matrix v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**性质**：**仅登记可接线点**，本 Phase **不执行接线**。每项默认 **disabled**，且须 **env 闸 + shadow 对比 + abort 开关**。

机器可读完整表：`logs/mainline_runtime_readiness_001_<timestamp>/mainline_runtime_wiring_candidate_matrix.json`（由 `run_mainline_runtime_readiness_review_v0.py` 生成）。

---

## YOLO

| wiring_point | bypass_risk | notes |
|--------------|-------------|-------|
| frame_ingestion_point | high | 必须注入 trace/session，否则 Core View 断裂。 |
| detector_invocation_point | high | 推理输出须带 RequestTrace stage 与硬审计占位。 |
| observation_loop_or_offline_mainline_equivalent | medium | 在线 tick 与离线回放对齐前须 shadow diff。 |
| request_trace_stage_emission_point | high | 禁止私有并行通道。 |

---

## OCR

| wiring_point | bypass_risk | notes |
|--------------|-------------|-------|
| ocr_source_policy_selector | medium | 策略旁路 → 不可审计源。 |
| yolo_to_ocr_bridge_proposal_point | medium | 仅提案；下游显式接纳。 |
| ocr_provider_invocation_point | high | 无 TRW → 不可比 shadow。 |
| midplatform_evidence_input_point | medium | 证据泄漏须 kill switch 阻断下游。 |
| request_trace_stage_emission_point | high | 与 YOLO/Voice 共用 namespace。 |

---

## Qwen Voice / TTS governed entry

| wiring_point | bypass_risk | notes |
|--------------|-------------|-------|
| before_run_tts_unified_entry | high | 真实链最后一道闸；未接线前保持 dry-run。 |
| before_voice_output_plane_submit | high | governance + hard_audit 必备。 |
| before_actual_provider_invocation | high | health/timeout/fallback 必须可观测。 |
| after_voice_output_governance_decision | high | 决策为合法文本源之一。 |
| governed_provider_entry_dry_run_point | low | Shadow 已闭合；下一跳为显式 trial。 |
| request_trace_stage_emission_point | medium | 与 Phase-Qianwen 映射一致。 |

---

## 通用字段（生成 JSON 中每项均包含）

- `allowed_in_next_phase`：是否允许在 **下一专门接线 Phase** 讨论（非本 Phase）。
- `default_enabled`：**false**。
- `requires_env_flag` / `requires_shadow_compare` / `requires_abort_switch`：**true**。
