# Phase-Voice-OutputGovernance-004
# Voice Output TRW Adapter v0（适配器定义）

**目标**：把 Phase-002/003 的治理产物转成统一的 extractor-friendly records 与 request-level timeline，使治理结果进入统一可观察面（TRW/白盒抽链规则可消费）。  
**边界**：只做 offline/shadow 适配；不接真实 submit；不真实播报；不执行真实 TTS。

---

## 1. 输入与输出

### 1.1 输入（Phase-002 output_root）

默认输入根目录：

- `logs/voice_output_governance_002_test_run`

读取文件：

- `voice_output_governance_decisions.json`
- `voice_output_audit_envelopes.json`
- `voice_output_trace.jsonl`
- `voice_output_replay.jsonl`
- `voice_output_whitebox.jsonl`

### 1.2 输出（Phase-004 adapter output_root）

- `voice_output_trw_records.json`（核心）
- `voice_output_stage_timeline.json`
- `voice_output_extractor_mapping_report.json`
- `voice_output_whitebox_extension.json`
- `voice_output_trw_adapter_trace.jsonl`
- `voice_output_trw_adapter_replay.jsonl`
- `voice_output_trw_adapter_whitebox.jsonl`

---

## 2. Stage Namespace（必须）

- `stage_namespace = "voice_output_governance_v0"`

Stage names（顺序固定）：

- candidate_input
- speakable_guard
- speech_gate
- expiry_check
- stale_check
- cancellation_check
- priority_check
- interruption_check
- suppression_check
- provider_health_check
- final_governance_decision
- audit_envelope

---

## 3. TRW Adapter Record（抽链友好记录）

记录对象（示意）：

`VoiceOutputTRWRecordV0`：

- request_id（主键）
- stage_namespace / stage_name / stage_order（用于 timeline）
- status / reason（用于抽链与归因）
- hard_audit（硬审计字段，必须可观测且保持不变量）
- whitebox_extension（用于解释“为什么被抑制/为什么不执行”）

---

## 4. 硬审计字段（必须）

必须存在并满足：

- real_tts_invoked=false
- playback_invoked=false
- provider_invoked=false
- downstream_invocation_count=0
- navigation_action=null

---

## 5. 本阶段产出声明（必须）

- 本阶段只做 TRW adapter / extractor mapping：不真实播报、不执行真实 TTS、不接新 provider、不改 env 语义、不接真实 submit。

