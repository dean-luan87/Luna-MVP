# Phase-Voice-OutputGovernance-003
# Voice Output Mainline Wiring Contract v0（未来主链接线合同）

**目的**：把 Phase-002 的 governance 决策层“写死”为未来真实输出链的强制门，防止出现“真实 submit 绕过治理”的结构性风险。  
**边界**：本阶段只定义合同与静态验证；禁止把 Phase-002 skeleton 直接接入真实 submit 链。

---

## 1. 允许接线位置（候选）

候选允许位置（至少选择一个作为强制 gate）：

- **A. `dispatch_voice_final_text` 内 `_maybe_submit_real_output_v1` 之前**  
  - 优点：离“候选文本生成点”最近，能阻止旁路 submit helper 走漏。
- **B. `VoiceOutputPlane.submit` 入口内**  
  - 优点：所有模块统一出口处强制 gate，天然防旁路。
- **C. `tts_unified_entry` 之前**  
  - 仅允许作为“最后一道 provider readiness gate”，**不得**作为唯一治理 gate（太晚）。

**推荐**：必须至少在 **A 或 B** 之一存在强制 governance gate。不得仅放在 C。

---

## 2. 主链强制顺序（不得绕过）

未来真实链必须满足（与 Phase-002 一致）：

Voice final text / SpeechRequest candidate  
→ `VoiceOutputGovernanceInput` 构造  
→ `guard_v1_speakable_text`  
→ `SpeechGate`（最终裁决）  
→ expiry/stale/cancel/priority/interrupt  
→ provider health/readiness  
→ （allow）`VoiceOutputPlane.submit` / （deny）suppress  
→ 仅在 `real_playback` 且 env 明确允许时才进入 TTS/playback

---

## 3. “不得绕过治理”的强约束（硬规则）

- **任何真实输出提交路径**必须能证明“经过 governance decision”。  
  - 证明方式：TRW/trace 中存在 `voice_output_governance_decision_id`（或等价 ref）并可回溯到 audit envelope。
- **SpeechGate 不得旁路**：所有会产生真实播报的路径必须执行 SpeechGate 裁决并可观测 reason。
- **guard 不得旁路**：所有候选文本进入 submit 之前必须经过 speakable guard。

---

## 4. 审计硬字段（必须）

以下字段必须作为链级硬审计字段出现于 decision/audit/TRW：

- `real_tts_invoked: bool`
- `playback_invoked: bool`
- `provider_invoked: bool`
- `downstream_invocation_count: int`
- `navigation_action: null`（本 phase 与 Phase-002 都必须为 null）

---

## 5. 静态验收（Phase-003）

Phase-003 verifier 需要检查：

- 本合同存在且包含 “A/B 至少一个强制 gate” 的条款
- 明确禁止 “仅在 C gate”
- 明确 “不得绕过治理” 的可观测证明要求

