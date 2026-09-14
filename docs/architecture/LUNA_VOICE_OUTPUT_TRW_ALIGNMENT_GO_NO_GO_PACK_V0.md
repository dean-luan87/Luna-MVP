# Phase-Voice-OutputGovernance-003
# Voice Output TRW Alignment & Mainline Wiring Contract Go/No-Go Pack v0

**目标**：把 Phase-002 治理产物字段对齐到既有 TRW/白盒体系，并把未来主链接线位置与“不得绕过治理”写死。  
**边界**：本阶段只做文档与静态 verifier；不接真实 submit、不真实播报、不执行真实 TTS。

---

## 1. GO 条件

- Phase-002 output_root 可读：`logs/voice_output_governance_002_test_run`
- TRW 字段映射完整：覆盖要求字段（见 `LUNA_VOICE_OUTPUT_TRW_ALIGNMENT_V0.md`）
- mainline wiring contract 完整：允许接线位置 A/B/C，且明确 “至少 A 或 B 强制 gate”
- runtime mode policy 完整：dry_run/shadow/governed_submit/real_playback；默认不为 real_playback
- audit field mapping 完整：硬审计字段映射明确
- 静态 verifier 通过并落盘
- 未接真实 runtime，未真实播报，未改 env 语义

---

## 2. CONDITIONAL_GO

- 某些旧 TRW/whitebox 字段命名需要后续 adapter 才能完全一致，但合同已写死“新增治理阶段命名空间 + 映射表”，且静态 verifier 覆盖 required fields。

---

## 3. NO_GO 条件

- 未定义主链接线位置或未禁止“仅在 C gate”
- 未定义 runtime mode 或默认允许 real_playback
- 未定义 `real_tts_invoked/playback_invoked/provider_invoked/downstream_invocation_count` 的硬审计字段
- 本阶段接入真实 submit 或真实播报
- 绕过 SpeechGate
- 删除 legacy voice 或修改 env 语义

---

## 4. 验收输出

- 新增文档齐全（5 份）
- `tools/verify_voice_output_trw_alignment_v0.py` 输出：
  - `logs/voice_output_trw_alignment_003_<timestamp>/verification_result.json`

