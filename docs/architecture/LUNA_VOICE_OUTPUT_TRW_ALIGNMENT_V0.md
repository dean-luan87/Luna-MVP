# Phase-Voice-OutputGovernance-003
# Voice Output TRW Alignment v0（字段对齐）

**目标**：将 Phase-002 的 `decision/audit/trace/replay/whitebox` 字段，映射到既有 Voice 白盒/TRW（Request Trace / Whitebox）体系，确保未来接线时不会出现“治理骨架有了，但白盒看不见/字段不统一”。  
**边界**：本阶段只做字段对齐文档与静态验证；不接真实 submit、不真实播报、不执行真实 TTS。

---

## 0. 上游与输入

- **Phase-002 output_root（基线样本）**：`logs/voice_output_governance_002_test_run`
- **Phase-002 产物（关键）**：
  - `voice_output_governance_decisions.json`
  - `voice_output_audit_envelopes.json`
  - `voice_output_trace.jsonl`
  - `voice_output_replay.jsonl`
  - `voice_output_whitebox.jsonl`
- **既有 TRW/白盒字典**：
  - `docs/architecture/voice/LUNA_VOICE_WHITEBOX_FIELD_DICTIONARY_V1.md`
  - `docs/architecture/voice/LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md`
  - `docs/architecture/voice/LUNA_VOICE_REQUEST_TRACE_EXTRACTION_RULES_V1.md`

---

## 1. 对齐原则（必须）

- **request_id 是主键**：Phase-002 产物必须可用 `request_id` 对齐到 TRW 的 `RequestTraceChain.request_id`。
- **trace_id / session_id 可选但推荐**：Phase-003 只定义映射；Phase-004/真实接线时要求从主链注入。
- **治理不变量必须进入 TRW**：`real_tts_invoked/playback_invoked/provider_invoked/downstream_invocation_count` 必须可见。
- **治理结论必须可解释**：suppressed/cancelled/expired/stale/interrupt_denied/provider_blocked 的原因必须在 whitebox 侧可展示。

---

## 2. 字段映射表（Phase-002 → TRW/Whitebox）

> 说明：TRW 体系以 `RequestTraceChain / RequestTraceSummary / RequestTraceIssue` 为主；Phase-002 当前是“离线治理决策层”，因此映射采用“新增 stage + whitebox 扩展字段”的方式对齐，而不是硬塞为 provider/playback 失败。

| Phase-002 字段 | 目标 TRW 字段/位置 | 说明 |
|---|---|---|
| `request_id` | `RequestTraceChain.request_id` | 主键对齐 |
| `trace_id`（未来） | `RequestTraceChain.trace_id` | Phase-002 样本未覆盖；未来主链注入 |
| `session_id`（未来） | `RequestTraceChain.session_id` | Phase-002 样本未覆盖；未来主链注入 |
| `candidate_text` | Whitebox 扩展字段（输出治理视图） | 不要求进入简洁模式；用于专业模式解释 |
| `candidate_text_hash`（未来） | Whitebox 扩展字段 | Phase-003 定义；Phase-004 可实现 hash 统一 |
| `priority_result.priority` | Whitebox 字段 +（可选）stage key_fields | 统一 priority 标签（safety/navigation/task/chat/debug） |
| `priority_result.interrupt_allowed` | Whitebox 字段 | 对齐 “why_interrupt_allowed/denied” 展示 |
| `expiry_result.expires_at` | Whitebox 字段 | 过期窗口解释 |
| `guard_result.*` | stage `governance_guard` 的 key_fields | guard_name/speakable/reason/profile/degraded |
| `speech_gate_result.*` | stage `speech_gate` 的 key_fields | gate_invoked/allowed/reason/owner |
| `expiry_result.*` | stage `expiry` 的 key_fields | expired/stale_suppressed/reason |
| `cancel_result.*` | stage `cancellation` 的 key_fields | cancel_requested/cancelled |
| `suppression_result.*` | stage `suppression` 的 key_fields | suppressed/suppression_reason |
| `provider_health_result.*` | stage `provider_health` 的 key_fields | provider_status/fallback_required/reason |
| `final_action` | `RequestTraceChain.chain_type` / `RequestTraceSummary.status`（映射规则） | `accepted_dry_run`→success-like；`suppressed/cancelled`→suppressed_chain；`fallback_candidate`→degraded_success-like（但不执行） |
| `governance.real_tts_invoked` | Whitebox & Audit hard field | 必须为 false（dry/shadow） |
| `governance.playback_invoked` | Whitebox & Audit hard field | 必须为 false |
| `governance.provider_invoked` | Whitebox & Audit hard field | 必须为 false |
| `governance.downstream_invocation_count` | Whitebox & Audit hard field | 必须为 0 |
| `audit_envelope_ref` | `raw_observation_refs` 或 whitebox link | Phase-003 先定义 ref；未来可导出为可跳转链接 |

---

## 3. TRW “新增治理阶段”命名空间（建议）

为保持与既有 `TraceStageRecord.stage_name` 一致性，建议新增以下 stage 名称（Phase-003 仅定义，不落实现接线）：

- `voice_output_governance_input`
- `voice_output_guard`
- `voice_output_speech_gate`
- `voice_output_expiry`
- `voice_output_priority_interrupt`
- `voice_output_cancellation`
- `voice_output_suppression`
- `voice_output_provider_health`
- `voice_output_audit_envelope`

---

## 4. 最小展示语句（whitebox）

Phase-002 已存在 whitebox JSONL 的原因字段；未来对齐到 TRW 展示建议：

- why_suppressed / why_expired / why_stale / why_cancelled
- why_interrupt_allowed / why_interrupt_denied
- why_provider_blocked
- why_guard_blocked

---

## 5. 本阶段产出声明（必须）

- 本阶段只做 TRW alignment 与合同：不真实播报、不执行真实 TTS、不接新 provider、不改 env 语义、不接真实 submit。

