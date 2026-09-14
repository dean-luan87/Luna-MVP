# Phase-Voice-OutputGovernance-003
# Voice Output Governance Audit Field Mapping v0（审计字段映射）

**目的**：定义 `VoiceOutputAuditEnvelope` 与 TRW/白盒字段对齐表，保证未来接线后可以做“可追溯、可回放、可解释”的审计闭环。  
**边界**：本阶段只定义映射，不修改任何 runtime。

---

## 1. 源对象（Phase-002）

- `voice_output_audit_envelopes.json` 中的 `VoiceOutputAuditEnvelopeV0`
- `voice_output_governance_decisions.json` 中的 `VoiceOutputGovernanceDecisionV0`

---

## 2. 审计字段映射（最小必须）

| Audit/Decision 字段 | 目标 TRW/白盒字段 | 说明 |
|---|---|---|
| `audit_id` | `raw_observation_refs` 或审计链接字段 | 用于回溯 |
| `request_id` | `RequestTraceChain.request_id` | 主键 |
| `created_at` | `RequestTraceChain.started_at`（或 stage timestamp） | 近似；真实接线时以观测时间为准 |
| `governance_version` | Whitebox 元数据 | 版本识别 |
| `invariants.real_tts_invoked` | Whitebox hard field | 必须明确 |
| `invariants.playback_invoked` | Whitebox hard field | 必须明确 |
| `invariants.provider_invoked` | Whitebox hard field | 必须明确 |
| `invariants.downstream_invocation_count` | Whitebox hard field | 必须明确 |
| `decision_ref` | `voice_output_governance_decision_id` | 必须可回链 |
| `trace_ref/replay_ref/whitebox_ref` | 对应产物引用 | 必须存在且可追溯 |

---

## 3. 未来补充（非本阶段）

- `candidate_text_hash` 的统一算法与落点
- `trace_id/session_id` 的主链注入与跨系统对齐
- `RequestTraceExtractor` 对 governance stages 的正式映射规则

