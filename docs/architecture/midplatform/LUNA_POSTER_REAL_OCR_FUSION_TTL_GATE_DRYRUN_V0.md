# Luna — Poster Real OCR Fusion TTL Gate DryRun v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001`

## 目的

对 Poster fusion **review queue** 中 pending fusion candidate 执行 **TTL gate dry-run**。仅评估商业/促销/时间文本的 TTL 风险与未来写入前置条件。

## 原则

- TTL gate 是**评估门**，不是批准门
- `ttl_gate_evaluated=true` 允许；`ttl_gate_passed` 不得直接产生 `write_allowed`
- `price_or_promo_area` 与 `time_location_area` 强制进入 TTL gate
- 全部 `fact_status=not_fact`；`write_allowed=false`；`approval_status=not_approved`
- 不重跑 OCR；不写 MidPlatform / Scene Delta / WorldModel

## 实现

- Capability：`capabilities/midplatform/poster_real_ocr_fusion_ttl_gate_dryrun_v0.py`
- Runner：`tools/evaluation/midplatform/run_poster_real_ocr_fusion_ttl_gate_dryrun_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_poster_real_ocr_fusion_ttl_gate_dryrun_v0.py`

## 评测

[LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_V0.md)

## 建议下一跳

**Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001** — 见 [LUNA_POSTER_REAL_OCR_FUSION_POLICY_GATE_DRYRUN_V0.md](./LUNA_POSTER_REAL_OCR_FUSION_POLICY_GATE_DRYRUN_V0.md)

**Poster-Real-OCR-Fusion-Gate-Chain-Closure-001**（policy gate 之后；先收口门控链，勿立即 Scene Delta）
