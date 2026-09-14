# LUNA Voice — Qwen-first / TTS-fallback Policy v0（Phase-Voice-Qianwen-001）

**冻结类型**：运行模式口径 + 三层分离说明；**不修改**仓库默认 **`offline_only`** 基线。**本阶段不产生真实音频、不启用网络/SDK。**

---

## 1. `LUNA_VERIFIER_ANCHOR: QW001_POLICY_TEMPLATE_ONLINE_PREFER_QWEN`

### 1.1 模板层：`online_prefer_qwen`

在 `capabilities/voice/config/voice_tts_config.yaml` 的 **`runtime_modes.online_prefer_qwen`** 中定义：

| 语义 | 值 |
|------|-----|
| **首选合成 provider（在线可得时）** | `qwen` |
| **fallback 次级（本地/离线合成）** | `piper`（及既有 legacy 链路依配置追加） |

该模式表达的 **仅是策略模板**：是否激活取决于运行态如何把 `tts_runtime_mode`/`offline_only`/密钥/网络对齐到模板（实现不在本 Phase）。

---

## 2. `LUNA_VERIFIER_ANCHOR: QW001_POLICY_DEFAULT_BASELINE_OFFLINE_ONLY_PIPER`

### 2.1 默认工程基线（签入快照，保持不修改）

`**LUNA_VERIFIER_ANCHOR: QW001_POLICY_DEFAULT_RUNTIME_UNCHANGED_BY_PHASE_001**`

以下条件为本仓库 **意图保留的默认值**（verifier 与运维以此对齐）：

- **`tts_runtime_mode: offline_only`**
- **顶层 `provider_order: [piper]`**，**`active_provider: piper`**
- **`offline_only: true`**（离线 gate）
- **`local_runtime.qwen.enabled: false`**（qwen 不在默认开箱路径启用）

Phase-001 **不**通过改配置、「悄然切默认」来获得 GO。

---

## 3. Provider role 分层（精确表述）

为避免「Qwen 首选」被误读为「全局默认主链已是 Qwen」，采用三层：

| 层级 | 含义 |
|------|------|
| **模板 / policy** | `online_prefer_qwen` → **`qwen` first, `piper` fallback** |
| **默认基线（仓库）** | **`offline_only` / Piper-only / qwen disabled** |
| **governed runtime（目标）** | 任何模板路径下，必须先 **GovernedVoiceProviderEntry**，再进入 **provider 执行**（见 `LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`） |

---

## 4. 与 QwenTTSProvider 边界

`qwen-tts` 为 **text→audio** 合成器，非表达改写模型；若存在表达改写，则走 **expression contract**，不得借道本 policy 将语义混写进 `qwen-tts` 文档。见 `LUNA_VOICE_QWEN_TTS_PROVIDER_ROLE_AND_BOUNDARY_V0.md`。

---

## 5. 关联文档

- `LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`
- `LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md`
