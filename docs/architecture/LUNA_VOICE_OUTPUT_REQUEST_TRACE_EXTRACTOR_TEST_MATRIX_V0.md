# Phase-Voice-OutputGovernance-005
# Voice Output RequestTraceExtractor Shadow Integration Test Matrix v0

**输入**：`logs/voice_output_trw_adapter_004_test_run`  
**输出**：`logs/voice_output_request_trace_extractor_005_<timestamp>`

---

## 覆盖点（必须）

- 每个 request 生成一条 `RequestTraceChain`
- stages 有序且包含必需阶段：
  - candidate_input / speakable_guard / speech_gate
  - expiry_check / cancellation_check
  - provider_health_check / final_governance_decision
- hard audit fields 在 final_governance_decision stage 可读取，且保持不变量
- shadow only：summary 中 `shadow_only=true`
- shadow trace/replay/whitebox JSONL 非空

