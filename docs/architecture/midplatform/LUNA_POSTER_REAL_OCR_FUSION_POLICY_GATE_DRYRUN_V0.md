# Luna — Poster Real OCR Fusion Policy Gate DryRun v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001`

## 目的

对 Poster real OCR **fusion candidate** 执行 **policy gate dry-run**。仅评估是否满足进入后续 Scene Delta candidate dry-run 的策略条件。

## 原则

- Policy gate 是**策略评估门**，不是批准门
- TTL gate 当前 `hold_for_review`，policy gate 默认亦 `hold_for_review`
- `scene_delta_candidate_allowed=false`；全部 `write_allowed=false`
- 不重跑 OCR；不写 MidPlatform / Scene Delta / WorldModel

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_fusion_policy_gate_dryrun_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_fusion_policy_gate_dryrun_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_fusion_policy_gate_dryrun_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_POLICY_GATE_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_POLICY_GATE_DRYRUN_V0.md)

## 建议下一跳

**Phase-Poster-Real-OCR-Fusion-Gate-Chain-Closure-001** — 见 [LUNA_POSTER_REAL_OCR_FUSION_GATE_CHAIN_CLOSURE_V0.md](./LUNA_POSTER_REAL_OCR_FUSION_GATE_CHAIN_CLOSURE_V0.md)
