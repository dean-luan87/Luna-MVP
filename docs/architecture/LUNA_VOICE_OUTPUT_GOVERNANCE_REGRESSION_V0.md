# Phase-Voice-OutputGovernance-006
# Voice Output Governance Regression v0（回归记录）

**目的**：对 Voice Output Governance Phase 000–005 的离线/影子链路做回归验收，确认治理链闭环、TRW 适配闭环、RequestTraceChain shadow 视图闭环，并保持硬审计不变量。  
**边界**：回归只读既有 output roots；不接真实 submit、不真实播报、不执行真实 TTS。

---

## 1. Regression inputs（只读 roots）

- Phase-002 governance root：`logs/voice_output_governance_002_test_run`
- Phase-004 TRW adapter root：`logs/voice_output_trw_adapter_004_test_run`
- Phase-005 RequestTrace shadow root：`logs/voice_output_request_trace_extractor_005_test_run`

---

## 2. Regression tools

- `tools/run_voice_output_governance_regression_v0.py`
- `tools/verify_voice_output_governance_regression_v0.py`

---

## 3. Hard gates（必须）

- decisions generated
- TRW records generated
- request chains generated
- ordered stages present
- guard stage present
- SpeechGate stage present
- expiry/cancel/priority/provider health/final decision present
- hard audit fields preserved
- 不变量：
  - `real_tts_invoked=false`
  - `playback_invoked=false`
  - `provider_invoked=false`
  - `navigation_action=null`
  - `downstream_invocation_count=0`

---

## 4. Closure statement（重要）

本回归与 closure 只冻结 **offline/shadow governance chain**。  
它 **不等于** 真实播报链接入；真实 submit/playback 仍明确禁止（见 boundary register）。

