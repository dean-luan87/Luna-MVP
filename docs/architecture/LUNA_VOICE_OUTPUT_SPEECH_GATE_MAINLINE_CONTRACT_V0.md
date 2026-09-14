# Phase-Voice-OutputGovernance-001-Fix
# Voice Output Speech Guard + Speech Gate Mainline Contract v0（主链对齐合同）

**目的**：把两个“硬风险”（`guard_v1_speakable_text` 命名/实现不一致、SpeechGate 接线不明）变成**可验收的合同**，为后续 Phase-002 最小治理骨架提供硬门槛。  
**本阶段边界**：合同 + 静态验证；不改 runtime、不真实播报、不执行真实 TTS、不接新 provider、不改现有 env 开关语义。

---

## 1. 定义：两个不同的“门”

### 1.1 Speakable Guard（可播报文本守卫）

**定义**：对“候选播报文本”做保守守卫，禁止把不确定/占位/幻觉包装成确定事实输出。  
**输入**：candidate text + minimal context（output_category/source_module/risk_level 等）  
**输出**：

- `allowed: bool`
- `guard_reason: str`（规则命中原因）
- `normalized_text: str`（允许时可裁剪/降级后的文本）
- `guard_profile: str`（用于分场景规则集）

**命名约束（解决 hard blocker #1）**：

- 文档中历史名称 `guard_v1_speakable_text` 被视为 **概念名**。
- 后续实现允许三种落地方式（二选一即可）：
  1. **同名函数落地**：提供 `guard_v1_speakable_text(...)` 并作为主链唯一 guard。
  2. **新名实现 + 映射表**：提供 `guard_*` 新 API，但必须在本合同中维护“旧名→新名”的映射条目，并确保静态 verifier 可定位到新 API。
  3. **临时替代（token guard）**：允许短期使用 token guard，但必须显式标记为 `deprecated_candidate`，且 Phase-002 必须升级为可复用 guard API。

### 1.2 Speech Gate（发言权总闸）

**定义**：系统级“是否允许说话”的最终裁决权，解决占用、冷却、用户说话抑制、重复抑制、强制抢占等。  
**输入**：candidate speech attempt +（可选）scene_hash / user_speaking / owner 等  
**输出**：`(allowed: bool, reason: str)` +（必须可观测）lock_owner/cooldown 状态等

---

## 2. 主链必须经过的 gate 顺序（Phase-002 hard gate）

后续最小治理骨架（Phase-002）必须满足以下顺序（任一环节不得绕过）：

1. **candidate text produced**（候选文本产生）
2. **speakable guard applied**（Speakable Guard）
3. **speech gate decision**（SpeechGate 最终裁决）
4. **expiry/priority/cancel/suppress checks**（输出治理检查：过期/优先级/取消/抑制）
5. **output plane submit**（`VoiceOutputPlane.submit(SpeechRequest)`）
6. **provider health / dependency readiness gate**（provider 健康与依赖就绪门）
7. **tts/playback execution**（TTS/播放执行；Phase-002 可保持 dry-run）

**允许的接线位置（解决 hard blocker #2）**：

- **Option A（推荐）**：SpeechGate 在 `VoiceOutputPlane.submit(...)` 内部统一裁决并发出观测。
- **Option B**：SpeechGate 在 submit helper（如 `_maybe_submit_real_output_v1`）中裁决，且必须保证所有 submit 路径都经过该裁决（禁止旁路 submit）。

---

## 3. 观测与审计要求（最小）

为避免“gate 存在但不生效”，必须满足：

- **Guard decision 可观测**：至少落入 JSONL envelope 或白盒字段：
  - `guard_allowed / guard_reason / guard_profile / text_len_before/after`
- **SpeechGate decision 可观测**：
  - `gate_allowed / gate_reason / lock_owner / cooldown_until / dedup_key(scene_hash)`
- **real_tts_invoked 审计硬字段**：
  - Phase-002 必须提供链级字段 `real_tts_invoked: bool`（即使保持 dry-run，也必须明确记录为 false）

---

## 4. 静态验证规则（Phase-001-Fix 的验收）

本阶段静态 verifier 必须检查：

- `SpeechGate` 实现存在（代码可定位）
- `SpeechRequest` / `VoiceOutputPlane` / `dispatch_voice_final_text` / `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 可定位
- `guard_v1_speakable_text`：
  - 若代码中存在同名实现 → 记录为 present
  - 若不存在 → 必须在本合同中显式声明“当前缺失/由替代方案承载”，且 verifier 将其记录为 blocker（不允许假装存在）
- SpeechGate 主链接线：
  - 若检测到接线证据 → 记录为 detected
  - 若检测不到 → 必须在本合同中明确 “Phase-002 必须强制接入（required）”，并在 verifier 输出中标记为 required

---

## 5. Verifier 约定标记（供静态工具使用）

为便于静态 verifier 做“合同存在性”校验，本合同提供以下标记常量（只用于扫描，不影响运行时）：

- `ALIGNMENT_CONTRACT_V0`
- `GUARD_V1_SPEAKABLE_TEXT_STATUS: missing_or_replaced`
- `SPEECH_GATE_MAINLINE_WIRING_REQUIRED: true`

---

## 6. 与 Minimal Controlled Output Definition 的关系

本合同在 `Minimal-Runtime-Integration-Controlled-Output-Definition-v1` 中被作为 **只读上游合同** 引用。  
即使进入后续 text-only controlled output trial，本合同仍不授权真实 TTS、真实音频播放或绕过 `source_chain` 的直接输出。

