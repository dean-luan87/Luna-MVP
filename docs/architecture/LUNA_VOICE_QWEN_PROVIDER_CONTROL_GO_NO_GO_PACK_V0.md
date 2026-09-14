# LUNA Voice — Qwen Provider Control Go / No-Go Pack v0（Phase-Voice-Qianwen-001）

**阶段**：Phase-Voice-Qianwen-001 — **Governed Qwen/TTS Unified Entry Contract v0**  
**仅限**：文档合同 + **静态 verifier**；**不改变**默认 provider、`voice_tts_config.yaml` 语义、env 开关语义。

`**LUNA_VERIFIER_ANCHOR: QW001_GO_PACK_PHASE_001_SCOPE**`

---

## GO（本阶段收口）

以下条件 **全部**满足：

1. **H-001** 已从盘点缺口升格为可读合同：**`LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`** 明示 **governance-before-`run_tts_unified_entry`**。  
2. **H-002** 已升格：**`LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md`** 给出 **`source_text` / `spoken_text` / `provider_input_text` / `provider_output_audio_ref` / `text_diff_audit**。  
3. **QwenTTSProvider** 边界写清：**`LUNA_VOICE_QWEN_TTS_PROVIDER_ROLE_AND_BOUNDARY_V0.md`**。  
4. **Qwen-first / Piper-fallback** 仅在 **policy 模板层**写明，默认 **offline** 不变：**`LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md`**。  
5. **`tools/verify_voice_qwen_governed_entry_contract_v0.py`** → **`verification_result.json`** 判定 **`ok: true`。  
6. 无真实调用 / 播报（脚本与新增文档均为离线静态）。

---

## NO_GO

任一成立即 NO_GO：

- 文档将 **`qwen-tts`/QwenTTSProvider** 描述为 **会改写可读内容的 expression model**。  
- 通过改 **默认 provider**、`voice_tts_config.yaml` **顶层离线基线**、或语义漂移 **env** 来完成本阶段「假 GO」。  
- 合同明示或暗示 **`run_tts_unified_entry` 可绕过 governance**。  
- **缺少** `source_text/spoken_text` 与 **`text_diff_audit`** 的合同定义或 verifier **未通过**。  
- 本 verifier 或其它新增代码中包含 **真实 Qwen / DashScope / TTS playback**。

---

## 推荐下一步（非本 Phase）

在保证默认基线不受影响的前提下：**实现单一权威接线点**，强制 **GovernedVoiceProviderEntry**，再将 **diff audit payload** 接入 Phase-009 统一视图与 RequestTrace/TRW stages。
