# Phase-Voice-OutputGovernance-007
# Governed Submit Shadow Readiness v0

**阶段定位**：在不真实播报、不执行真实 TTS、不接真实 submit 的前提下，把 `closed_v0` 的语音输出治理链推进到“接近真实 submit 前”的 shadow readiness 验证层。

**关键目标**：验证未来如果把治理 gate 放在 `_maybe_submit_real_output_v1` 前或 `VoiceOutputPlane.submit` 入口，能否产生一致的拦截/放行决策、审计与回放产物（shadow-only）。

---

## 1. 输入 roots（只读）

- Phase-002 governance outputs root（示例）：`logs/voice_output_governance_002_test_run`
- Phase-005 request trace shadow root（示例）：`logs/voice_output_request_trace_extractor_005_test_run`

---

## 2. 输出（output_root）

工具：`tools/evaluate_voice_governed_submit_shadow_v0.py`

- `voice_governed_submit_shadow_summary.json`
- `voice_governed_submit_shadow_inputs.json`
- `voice_governed_submit_shadow_decisions.json`
- `voice_submit_gate_audit_envelopes.json`
- `voice_governed_submit_shadow_trace.jsonl`
- `voice_governed_submit_shadow_replay.jsonl`
- `voice_governed_submit_shadow_whitebox.jsonl`
- `evaluation_notes.md`

---

## 3. 两个主链接线位置（只模拟，不接线）

输出中必须记录：
- `_maybe_submit_real_output_v1_pre`
- `VoiceOutputPlane.submit_entry`

> 本阶段只做 shadow readiness，不修改真实主链代码，不修改 env 开关语义。

---

## 4. Hard Audit 不变量（必须）

- `real_submit_invoked=false`
- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

---

## 5. 边界声明（必须）

- 不真实播报、不执行真实 TTS、不接新 provider
- 不删除 legacy voice，不改现有 env 开关语义
- 不把治理链接入真实 submit
- 不进入导航/SceneTask/Fusion/Output，不执行导航动作
- 不写世界模型，不上传蜂巢，不接推荐系统

