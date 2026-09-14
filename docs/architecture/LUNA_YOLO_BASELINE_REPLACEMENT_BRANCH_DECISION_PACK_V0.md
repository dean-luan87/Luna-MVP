# LUNA — YOLO Baseline Replacement Branch Decision Pack v0 (Phase-ModelPerception-011)

## Decision
### Result
**GO**（进入 Phase-ModelPerception-012：YOLO Default Offline Perception Source Policy v0）

### Scope of GO
- **GO 仅适用于**：Option A / phone_local 的 **offline evaluation 默认 perception candidate source** 选择。
- **不包含**：任何 runtime/controlled_live/full trial/动作执行/真实播报的授权或接入。

## Why (evidence summary)
基于 005–010 的证据矩阵（见 `docs/architecture/LUNA_YOLO_BASELINE_REPLACEMENT_EVIDENCE_MATRIX_V0.md`）：
- 005 证明 YOLO enabled shadow 相对 baseline/mock 存在可复核 detection 增量（invoked_count=3；detection_count_total=39）。
- 006 证明 YOLO shadow 输出可作为 PerceptionEval 替代输入，且五类 signals 完整、unsupported capabilities 诚实 not_available、candidate-only 与边界成立。
- 007–009 证明可安全桥接到 SceneTask/Fusion/Output 的离线候选层，保持 source attribution、timing/priority/suppression、no-real-TTS、零泄漏。
- 010 证明端到端离线候选链路闭合：
  - chain complete=1.0
  - schema valid=1.0
  - yolo source traceability all stages=1.0
  - candidate-only & no-real-TTS=1.0
  - leakage=0
  - evidence boundary=1.0
  - pending_real_sidewalk_run true=1.0

## Critical fix acknowledged (not “doc-only”)
010 初跑曾因 `pending_real_sidewalk_run` 未在 006 产物中传递导致 **NO_GO**，已修复并加入硬断言；该修复属于真实边界缺口修补。

## Hard boundaries (must remain)
- 不进入真实 runtime
- 不进入 controlled_live_stream / full controlled trial
- 不执行导航动作、不真实播报、不触发真实 TTS
- 不扩 Option A
- 不开启默认路径（runtime）
- 不关闭 `pending_real_sidewalk_run`
- 不声称 depth/OCR/dynamic/collision risk 能力

## Hard blockers
- `[]`

## Soft follow-ups
- torch.hub reproducibility 风险：后续需 pinned weights/deps。
- SceneContext gates 未 fully runtime enforce：保持治理要求，不得被绕过。
- fusion/output policy 仍为最小规则 v0：后续需扩展策略与更多样本覆盖。

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-012：YOLO Default Offline Perception Source Policy v0**
  - 目标：把“离线默认源选择”写成明确 policy（可开关、可回退、可审计），且不触及 runtime。

