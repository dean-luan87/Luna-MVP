# Phase-Voice-OutputGovernance-006
# Voice Output Governance Regression Baseline v0（回归基线）

**目的**：冻结回归基线 roots、允许波动项与不允许波动项，支撑后续 closure 后的稳定回归。

---

## 1. Baseline roots（只读）

- 002：`logs/voice_output_governance_002_test_run`
- 004：`logs/voice_output_trw_adapter_004_test_run`
- 005：`logs/voice_output_request_trace_extractor_005_test_run`

---

## 2. 允许波动（允许）

- request_id 具体值
- trace line order
- reason 文本细节
- candidate_text 内容
- `trace_id/session_id` 仍为空（直到未来主链注入）

---

## 3. 不允许波动（禁止）

- missing guard
- missing SpeechGate
- missing final decision
- missing hard audit fields
- `real_tts_invoked=true`
- `playback_invoked=true`
- `provider_invoked=true`
- `navigation_action` 非空
- `downstream_invocation_count>0`
- 真实 submit wiring 发生变化
- env semantics 发生变化
- legacy voice 被删除

