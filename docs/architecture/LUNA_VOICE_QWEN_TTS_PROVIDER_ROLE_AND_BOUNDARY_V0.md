# LUNA Voice — Qwen-TTS Provider Role & Boundary v0（Phase-Voice-Qianwen-001）

**冻结类型**：能力与职责边界声明（policy / contract）；**不写实现**；**不改变默认运行时**。  
前置：`Phase-Voice-Qianwen-000` → **CONDITIONAL_GO**。

---

## 1. `LUNA_VERIFIER_ANCHOR: QW001_ROLE_TEXT_TO_AUDIO_NOT_EXPRESSION`

`QwenTTSProvider`（`capabilities/voice/providers/qwen_tts_provider.py`）在工程语义上定位为 **文本到音频的合成器（synthesizer）**，即 **provider 类型：`text→audio`**。

- **必须**：在给定 **`provider_input_text`**（由上游 governance 允许的字符串）下进行合成，不向调用方回填「改写后的可读文本」。  
- **禁止**：将该适配器与用户可见「表达语义」的改写/润色/补全混淆；不得在架构文档中称其为 **expression model**。

## 2. Provider 优先级（不改变默认）

在 **运行时模式模板** **`online_prefer_qwen`** 下，`QwenTTSProvider` 可作为 **在线首选的合成 provider**；`Piper` / 既有本地 `TTS` 链可作为 **fallback**（优先级与链路细节见 **`LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md`**）。

**仓库默认工程基线**仍为 **`offline_only` + Piper-only + `local_runtime.qwen.enabled: false`**，本阶段文档 **不请求**更改该默认值。

---

## 3. `LUNA_VERIFIER_ANCHOR: QW001_ROLE_EXPRESSION_SEPARATE_CHAIN`

若将来接入会进行 **语义改写 / 文案生成 / 润色表达** 的 Qianwen 能力，必须通过 **独立于 `qwen-tts` 的合成链路径**接入，并由专门的 **Expression Governance Contract** 治理（与本次 **GovernedVoiceProviderEntry** 合同区分）。不得将「表达改写」混入 `qwen-tts` 适配器语义。

参阅：`docs/architecture/LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`（§ expression 分叉）。

---

## 4. 与治理的关系

在进入任何 **Qwen / Piper / Fish / legacy `TTS` 的合成执行**之前，文本与权限状态必须经 **`voice_output_governance_v0`（或等价物）形成可记录的决策**；`run_tts_unified_entry` **不得被定义为可绕过 governance 的特权入口**。见 **`LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`**。

文本侧 **原文 vs 实际播报载荷**的审计字段见 **`LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md`**。

---

## 5. 关联冻结文档

| 文档 | 用途 |
|------|------|
| `LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md` | GovernedVoiceProviderEntry 合同 |
| `LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md` | diff 审计 schema |
| `LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md` | Qwen-first / TTS-fallback 策略分层 |

---

## 一句话

**Qwen 可以作为在线音频合成的首选 provider，但 `qwen-tts` 不是表达改写模型；表达治理必须另一条链。**（`QW001_ROLE_TEXT_TO_AUDIO_NOT_EXPRESSION`）
