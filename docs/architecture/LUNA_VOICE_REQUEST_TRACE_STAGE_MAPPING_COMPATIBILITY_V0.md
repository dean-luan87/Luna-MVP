# Phase-CoreCapability-TRW-Unified-001
# Voice RequestTrace Stage Mapping Compatibility v0（与现有 voice_output_governance_v0 兼容）

**目的**：将既有 `voice_output_governance_v0` stage namespace 与统一 `request_trace.stage.output.voice.*` 对齐，明确兼容关系与不得破坏的硬审计字段。  
**范围**：只定义兼容映射；不改现有 voice 链路实现。

---

## 1. 现有（已闭包）stage namespace

- `voice_output_governance_v0`（Phase-Voice-OutputGovernance 002–005 已用于 RequestTraceChain shadow mapping）

---

## 2. 统一目标 stage（v0）

将 voice output governance stages 统一呈现为：

- `request_trace.stage.output.voice.candidate_input`
- `request_trace.stage.output.voice.speakable_guard`
- `request_trace.stage.output.voice.speech_gate`
- `request_trace.stage.output.voice.expiry_check`
- `request_trace.stage.output.voice.stale_check`
- `request_trace.stage.output.voice.cancellation_check`
- `request_trace.stage.output.voice.priority_check`
- `request_trace.stage.output.voice.interruption_check`
- `request_trace.stage.output.voice.suppression_check`
- `request_trace.stage.output.voice.provider_health_check`
- `request_trace.stage.output.voice.final_governance_decision`
- `request_trace.stage.output.voice.audit_envelope`

---

## 3. 兼容映射规则（必须）

### 3.1 规范映射（统一命名空间）

- `voice_output_governance_v0.<stage>` → `request_trace.stage.output.voice.<stage>`

### 3.2 历史命名兼容（已有产物不得破坏）

Phase-005 的 shadow 产物使用了历史命名：

- `request_trace.stage.voice_output.<stage>`

统一阶段后续应收敛到：

- `request_trace.stage.output.voice.<stage>`

**硬规则**：

- 不得直接改写/破坏历史产物与旧 stage 名称。
- 必须通过“映射层/adapter”实现迁移展示（例如：在 extractor view 上把旧名 alias 到新名，或并行输出两套 stage_name）。

---

## 4. 硬审计字段（不得丢失）

以下字段必须贯通 decision/audit/TRW/RequestTrace：

- `real_tts_invoked`
- `playback_invoked`
- `provider_invoked`
- `navigation_action`
- `downstream_invocation_count`

并在 offline/shadow scope 下保持：

- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

