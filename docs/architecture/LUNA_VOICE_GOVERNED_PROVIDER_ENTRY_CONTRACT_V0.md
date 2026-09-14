# LUNA Voice — Governed Provider Entry Contract v0（Phase-Voice-Qianwen-001）

**冻结类型**：主链语义合同（尚未要求本阶段接线代码变更）。  
边界：**不涉及导航 / SceneTask / Fusion / Output 编排**的实现扩展；仅限 **播报合成链路**的合同定义。

---

## 1. `LUNA_VERIFIER_ANCHOR: QW001_CONTRACT_GOVERNED_VOICE_PROVIDER_ENTRY`

### 1.1 定义：`GovernedVoiceProviderEntry`

**GovernedVoiceProviderEntry**：在任一 **voice provider（含 `qwen`、`piper`、`piper`、legacy 文本 TTS）** 被选定并执行合成 **之前**，必须完成的 **单次治理收口**，其输出为 **可记录的 governance decision**，并附带供 RequestTrace/TRW 使用的锚点字段。

最小合同要素：

| 要素 | 说明 |
|------|------|
| 输入候选 | `SpeechRequest`（或等价结构）所含 **`text_candidate`** 及对 priority/expiry/interrupt/context 的补充 |
| Guard | **`guard_v1_speakable_text`**（或通过合同声明的等价 guard） |
| SpeechGate | **SpeechGate** 合同（已由 `voice_output_governance_v0` 定义的 dry-run-safe 语义） |
| expiry / cancel / interrupt / suppression | **VoiceOutputGovernance v0** 已有评估器 |
| provider health | **provider_health**（含 fallback_candidate 语义） |
| 输出 | **final_action** 与附带的 trace/replay/whitebox/`real_tts_invoked` **硬审计占位**口径 |

Governance API 的稳定参考：`capabilities/voice/output/voice_output_governance_v0.build_voice_output_governance_decision_v0`（本阶段仅以 **语义引用**）。

---

## 2. `LUNA_VERIFIER_ANCHOR: QW001_CONTRACT_BEFORE_RUN_TTS_UNIFIED_ENTRY`

### 2.1 规则：governance-before-provider（针对 H-001）

**任何通往 `run_tts_unified_entry(...)` 的路径**在正常模式下必须满足：

1. 已构造 **允许的**播报候选（经 governance 或其等价决策记录为 `accepted_dry_run` / 允许合成的映射动作）。  
2. **禁止**：将 **`run_tts_unified_entry` / `tts_unified_entry` 定义为「可跳过 governance」的特权入口——若技术上仍需保留该模块名，则在实现阶段必须改名为 **GovernedVoiceProviderExecution** / 或在入口内强制执行 governance（下一阶段实现）。

> 已知现状（inventory）：`voice_output_plane_v1` 注释表明 execute_tts 路径 **仍不接** SpeechGate。本合同的 **语义目标**是让该状态在后续实现中与合同 **收敛**，而不是在合同中合法化绕道。

---

## 3. Qwen-first / Piper-fallback（角色不改变默认）

provider **角色**：在 **`online_prefer_qwen`** 模板下，`qwen` 为首选 **合成**，`piper` 为次级 **离线合成**；默认值仍 **`offline_only`**。详见 **`LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md`**。

---

## 4. RequestTrace / TRW 锚点

### 4.1 建议的阶段命名空间（占位，供下一阶段接线）

在 RequestTrace/TRW JSONL 中出现以下 **语义阶段**之一即视为与本合同对齐（可实现为 stage name 常量）：

| 阶段（建议） | 含义 |
|----------------|------|
| `voice_output_governance_v0`（已存在语义） | 治理决策已形成 |
| `voice_governed_provider_entry_v0` | 「GovernedVoiceProviderEntry」合同收口完成（实现阶段可拆分更细粒度） |
| `tts_provider_selection_v0` | provider chain 选择与 fallback 观测（与 unified entry 对齐） |
| `tts_synthesis_invoke_v0` | 单次 provider 调用（不改变 `real_tts_invoked` 硬审计语义） |

必须与 Phase-009 统一视图 **字段兼容**，不得引入与 `voice_output_governance_v0` 冲突的 **`real_tts_invoked=true`** shadow 漂移（除非在新的显式实验中单独登记）。

---

## 5. Expression provider 分叉（未来）

`**LUNA_VERIFIER_ANCHOR: QW001_CONTRACT_EXPRESSION_PROVIDER_SEPARATE**`

会进行 **可读文本生成/改写** 的路径必须遵守 **独立的 Expression Governance Contract**（文件名预留：`…EXPRESSION_PROVIDER_GOVERNANCE_CONTRACT_V?`），**不得**挂载在 `qwen-tts` 合成入口下，也不得与 **GovernedVoiceProviderEntry（合成前置）** 混名。

---

## 6. 关联文档

- `LUNA_VOICE_QWEN_TTS_PROVIDER_ROLE_AND_BOUNDARY_V0.md`
- `LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md`
- `LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md`
