# Phase-Voice-OutputGovernance-005
# Voice Output RequestTraceExtractor Shadow Integration v0

**目标**：把 Phase-004 的 `voice_output_governance_v0` stage records 转成 RequestTraceExtractor 兼容的 `RequestTraceChain`（shadow/offline），以便白盒/调试后台用统一请求链视图观察语音输出治理阶段。  
**边界**：本阶段只做 shadow/offline 转换与验证；不改真实抽链 runtime，不接真实 submit，不真实播报，不执行真实 TTS。

---

## 1. 输入与输出

- **输入根目录（Phase-004）**：`logs/voice_output_trw_adapter_004_test_run`
  - `voice_output_trw_records.json`
- **输出根目录（Phase-005）**：`logs/voice_output_request_trace_extractor_005_<timestamp>`
  - `voice_output_request_chains.json`（RequestTraceChain 列表）
  - `voice_output_request_stage_mapping.json`
  - `voice_output_request_chain_whitebox.json`
  - shadow trace/replay/whitebox JSONL

---

## 2. 集成策略（shadow）

- 不修改 `capabilities/voice/observations/request_trace_extractor.py` 的 runtime 行为。
- 通过离线工具把 governance records 转成 `RequestTraceChain` 的 `stages`（`TraceStageRecord`）。
- 使用 `request_trace.stage.voice_output.<stage>` 命名空间，使其与既有 TRW stage 展示一致。

---

## 3. 必须保留的硬审计字段

从 Phase-004 record 的 `hard_audit` 进入 RequestTraceChain 的 stage key_fields：

- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `downstream_invocation_count=0`
- `navigation_action=null`

---

## 4. 本阶段产出声明（必须）

- 本阶段只做 RequestTraceExtractor shadow integration：不真实播报、不执行真实 TTS、不接新 provider、不改 env 语义、不接真实 submit。

