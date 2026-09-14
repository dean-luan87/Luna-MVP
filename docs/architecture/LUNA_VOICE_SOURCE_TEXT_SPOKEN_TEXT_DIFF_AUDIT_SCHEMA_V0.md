# LUNA Voice — source_text / spoken_text / Diff Audit Schema v0（Phase-Voice-Qianwen-001）

**冻结类型**：JSON 语义 schema（契约）；下一阶段再落代码与持久化。**本文件不触发任何 Qwen/TTS 调用**。  
对齐 inventory **H-002**：将「原文 vs 实际播报内容」升格为 **可导出、可回放**的结构化字段。

---

## 1. `LUNA_VERIFIER_ANCHOR: QW001_SCHEMA_VOICE_DIFF_AUDIT_V0`

### 1.1 顶层：`VoiceSpeakabilityAuditV0`

```json
{
  "schema_version": "voice_speakability_audit_v0",
  "request_id": "string",
  "utterance_id": "string",

  "source_text": "string",
  "spoken_text": "string",

  "provider_input_text": "string",
  "provider_kind": "qwen_tts | piper_tts | legacy_text_tts | legacy_text_tts | other",

  "provider_output_audio_ref": {
    "kind": "inline_sha256_hex | filepath | none",
    "value": "string"
  },

  "text_diff_audit": {
    "normalized_unicode": true,
    "equal_source_and_spoken": true,
    "equal_source_and_provider_input": true,
    "rewrite_source": "upstream_expression | downstream_template | governance_sanitize | manual_edit | none",
    "rewrite_allowed": false,
    "rewrite_reason_codes": [],
    "diff_algorithm": "unified_diff_placeholder_v0",
    "diff_summary_brief": "string"
  },

  "governance_decision_ref": {
    "voice_output_decision_id": "string",
    "governance_namespace": "voice_output_governance_v0"
  }
}
```

**字段必填规则（合同语义）**：`request_id`、`source_text`、`spoken_text`、`provider_input_text`、`provider_kind`、`text_diff_audit` 必填；音频若 dry-run / 被拒可为 `provider_output_audio_ref.kind=none`。

---

## 2. `LUNA_VERIFIER_ANCHOR: QW001_SCHEMA_PROVIDER_INPUT_AND_SPOKEN`

### 2.1 Qwen-TTS：**不得模型改写可读文本**

**`LUNA_VERIFIER_ANCHOR: QW001_SCHEMA_QWEN_TTS_INVARIANT_PROVIDER_INPUT_EQUALS_SOURCE`

对 **`provider_kind = qwen_tts`**：

- **`provider_input_text`** 必须由上游在进入合成前给定；SDK 返回值中的文本（若有）不得自动替代 `spoken_text`。  
- **`source_text`** 定义为 **语义来源侧**（编排/会话/确认的「应当依据的原文快照」）；  
- **`spoken_text`** 定义为 **已向用户履行的播报文本承诺**（在纯合成场景下必须与 **`provider_input_text`** 等价，除非记录了 **explicit** 的政策化替换）。  

若 **`spoken_text ≠ source_text`** 或 **`spoken_text ≠ provider_input_text`**，则 **`text_diff_audit.rewrite_allowed` 必须为 `true`**（若策略禁止改写却出现差异 → **合规失败**，由下一阶段实现报错/阻断），且必须填写 **`rewrite_source` / `rewrite_reason_codes`**。

对 **纯正 `qwen-tts`** 的常见不变式（合同）：**`spoken_text === provider_input_text`**；若有差异则视为 **链路 bug 或未经允许的上游改写**，不得在审计上静默通过。

---

## 3. 与 governed entry 的对齐

- `governance_decision_ref` **必须**能关联到 **`voice_output_governance_v0`** 产出的决策 id（与 Phase-009 导出兼容）。  
- **`real_tts_invoked`** 等硬审计占位仍遵从既有 governance 语义；本文档不负责放宽。

---

## 4. Expression provider（将来）

当上存在 **expression upstream**（润色模型）导致 **`spoken_text`** 可能与 **`source_text`** 有意分歧时：**必须** `rewrite_allowed=true` 且 **`rewrite_source=upstream_expression`**，并挂载 **单独的 expression contract**。

---

一句话：**先锁「原文快照 / 播报承诺 / provider 入口文本 / diff 归因」四口一致；qwen-tts 路径默认三口一致且不暗改。**（`QW001_SCHEMA_VOICE_DIFF_AUDIT_V0`）
