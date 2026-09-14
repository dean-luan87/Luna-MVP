# LUNA — YOLO Baseline Replacement Scope Policy v0 (Phase-ModelPerception-011)

## Policy statement
允许将 **YOLO shadow perception** 设为 **Option A / phone_local 的离线评测链（offline evaluation）默认 perception candidate source**。

该“替代（replacement）”**仅限离线评测默认源**，不授予任何 runtime 权限、不改变真实主链行为。

## Allowed scope (explicit allow)
- **Allowed**: offline evaluation / shadow evaluation
  - FieldBatch（phone_local archives）
  - PerceptionEval（candidate-only）
  - SceneTask/Fusion/Output 的离线桥接评测（candidate-only）
- **Allowed**: 将 YOLO shadow 作为离线评测默认 perception candidate source（仍可随时切回 baseline/mock）

## Forbidden scope (explicit deny)
- **Deny**: runtime replacement（任何真实主链 / 默认路径）
- **Deny**: controlled_live_stream
- **Deny**: full controlled trial
- **Deny**: 真实用户开放测试
- **Deny**: 真实 TTS 发声（real_tts_invoked 必须保持 false）
- **Deny**: 导航动作执行 / 任何 execute authority
- **Deny**: 关闭或改写 `pending_real_sidewalk_run`
- **Deny**: 改写 `evidence_type`（必须保持 phone_local_controlled_capture）
- **Deny**: 夸大能力（不得声称 depth/OCR/dynamic/collision risk 已验证）

## Required invariants (hard)
在“离线默认源替代”后，必须持续满足：
- candidate-only：allows_execute_now=false（跨所有下游候选）
- no-real-TTS：real_tts_invoked=false
- safety leakage totals=0（execute/default-on/release-retry-reopen/side-effects/forbidden semantics）
- evidence boundary 全部保持：
  - controlled_live_stream=false
  - phone_local_capture=true
  - pending_real_sidewalk_run=true

## Soft follow-ups (not blockers)
- torch.hub reproducibility 风险需要后续 pinned weights/deps
- SceneContext gates 尚未 fully runtime enforce（保持“不可跳过”的治理要求）

