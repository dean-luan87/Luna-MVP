# Phase-Voice-OutputGovernance-001-Fix
# Speech Guard / Speech Gate Mainline Alignment Review v0（现状复盘与对齐策略）

**阶段定位**：本阶段只做 guard/gate 对齐的合同与静态验证；不改 runtime、不真实播报、不接新 provider、不改现有 env 开关语义、不删 legacy voice。  
**上游事实**：

- Phase-Voice-OutputGovernance-000（Existing Asset Inventory v0）= **GO**
- Phase-Voice-OutputGovernance-001（Runtime Health & Output Governance Definition v0）= **GO**

---

## 1. 盘点结论回放（与 hard blockers 对齐）

### 1.1 主链已存在（代码事实）

已有主链（V1）：

`VoiceInputSessionManager`  
→ `dispatch_voice_final_text`  
→ `_maybe_submit_real_output_v1`  
→ `VoiceOutputPlane.submit(SpeechRequest)`  
→ `tts_unified_entry` / playback executor（受开关控制）

### 1.2 hard blocker #1：`guard_v1_speakable_text` 命名/实现不一致

**现状**：

- 文档中多处引用 `guard_v1_speakable_text(...)` 作为“保守输出守卫 / No Fabrication guard”。
- 在当前仓库代码中未定位到 `guard_v1_speakable_text` 的同名函数定义。
- `voice_final_text_dispatcher.py::_maybe_submit_real_output_v1(...)` 内存在一个 **最小 token guard**（例如 `unknown/todo/placeholder` → 降级为“不能确定”），但它不是同名函数，也不是可复用的统一 guard API。

**风险**：

- 文档读者可能误以为主链已有统一的 `guard_v1_speakable_text`，从而在后续增强中“跳过守卫接线”。

**本阶段对齐策略（合同化，不落 runtime 行为）**：

- 将 `guard_v1_speakable_text` 定义为 **逻辑概念名（Guard Concept）**，不假装其代码实现已存在。
- 在 `LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md` 中明确：
  - 后续最小骨架必须提供 **可定位的 guard 接口**（函数/类均可），并在主链 submit 前调用；
  - 若暂不实现同名函数，则必须提供 **等价替代实现**，并给出“命名映射表”（旧名→新名）与静态验证规则。

### 1.3 hard blocker #2：SpeechGate 是否实际接入主链不明确

**现状**：

- `core/speech_gate.py` 中 `SpeechGate` 实现存在（含 can_speak / acquire / force_acquire / release）。
- 但当前 voice output 主链（submit helper/output plane/playback）中，SpeechGate 是否作为**输出前最终裁决**被调用，尚未形成可自动证明的接线证据。

**风险**：

- gate “存在但不生效”会导致输出治理成为空壳：任何优先级/过期/取消策略都可能被绕过或无统一裁决点。

**本阶段对齐策略（合同化，不落 runtime 行为）**：

- 在 `LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md` 中把 SpeechGate 定义为 **强制主链门**：
  - 明确其“应在何处生效”（在 output plane submit 前、或 plane 内部统一裁决等）。
  - 明确必须落可观测的 gate decision 证据（reason、owner、cooldown、dedup key 等）。
- 在静态 verifier 中做两件事：
  - 能自动检测到接线 → 记录为“已接入”；
  - 检测不到接线 → **不假装存在**，并要求合同文档标记为“必须接入（required）”。

---

## 2. 本阶段输出（deliverables）

- `docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md`
  - 约束：后续骨架必须经过 guard + gate，并给出可审计/可验证要求。
- `docs/architecture/LUNA_VOICE_OUTPUT_GUARD_GATE_ALIGNMENT_GO_NO_GO_PACK_V0.md`
  - 约束：本阶段 GO/NO-GO 与 hard blockers/soft follow-ups。
- `tools/verify_voice_output_guard_gate_alignment_v0.py`
  - 静态验证：扫描 guard/gate 资产与主链引用/接线证据，并落盘 `verification_result.json`。

---

## 3. Recommended next phase

在本阶段对齐补丁通过后进入：

- **Phase-Voice-OutputGovernance-002: Voice Output Governance Minimal Skeleton v0**
  - 在不真实播放、不执行真实 TTS 的边界下，落最小可运行治理骨架：`SpeechRequest` → expiry/priority/cancel/suppress/guard/gate/provider-health → audit envelope。

---

## 4. 本阶段产出声明（必须）

- 本阶段只做 guard/gate 对齐：**不改 runtime**、不真实播报、**不接新 provider**、不删除 legacy voice、**不改 env 开关语义**、不接导航/SceneTask/Fusion/Output 新链路。

