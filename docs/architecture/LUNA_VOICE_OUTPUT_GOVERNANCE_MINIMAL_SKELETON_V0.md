# Phase-Voice-OutputGovernance-002
# Voice Output Governance Minimal Skeleton v0（最小骨架）

**目标**：在不真实播报、不执行真实 TTS 的边界下，把 voice output 从“能提交”升级为“提交前可治理、可过期、可取消、可打断、可审计”，并产出 trace/replay/whitebox。  
**硬边界**：不真实播报；不执行真实 TTS；不接新 provider；不改现有 env 开关语义；不进入导航/SceneTask/Fusion/Output；不写世界模型；不上载蜂巢；不接推荐系统。

---

## 1. 关键 required followups（来自 Phase-001-Fix）

- **`guard_v1_speakable_text` 必须可 import**：Phase-002 需要提供可定位实现或明确 alias/映射策略。
- **SpeechGate 必须纳入 skeleton 主链**：必须被调用，并在 trace/whitebox 可观测。

---

## 2. 最小骨架链路（必须经过）

1. candidate text
2. speakable guard（`guard_v1_speakable_text`）
3. SpeechGate（`SpeechGate.can_speak` dry-run 调用）
4. expiry / stale suppression
5. priority / interruption policy skeleton
6. cancellation
7. suppression decision
8. provider health / readiness skeleton（只产状态，不执行 provider）
9. output plane dry-run（不调用 playback，不调用 provider）
10. audit envelope + trace / replay / whitebox

---

## 3. 输出对象（核心）

- `VoiceOutputGovernanceDecisionV0`
- `VoiceProviderHealthStateV0`
- `VoiceOutputAuditEnvelopeV0`

关键硬审计字段（必须为 false）：

- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

---

## 4. 工具链

- evaluate：`tools/evaluate_voice_output_governance_v0.py`
- verify：`tools/verify_voice_output_governance_v0.py`
- sample：`datasets/voice_output_governance_samples_v0/sample_matrix.json`

---

## 5. 本阶段产出声明（必须）

- 本阶段只做最小骨架：不真实播报、不执行真实 TTS、不接新 provider、不删除 legacy voice、不改 env 语义。

