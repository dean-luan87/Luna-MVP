# Luna — Poster Real OCR Fusion TTL Gate DryRun GO/NO_GO Pack v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001`

## GO

- TTL gate dry-run 产物完整；verifier=GO
- `price_or_promo_area`、`time_location_area` 均被识别并 `hold_for_review`
- `ttl_gate_passed_count=0`；`ttl_gate_hold_count=1`
- approval / write / Scene Delta / WorldModel 全禁止
- no-write boundary 通过

## CONDITIONAL_GO

- TTL 文本为空但 gate/policy/boundary/audit 完整
- 无越界行为

## NO_GO

- TTL 被批准或 `write_allowed=true`
- 自动批准、fusion commit、Scene Delta candidate
- WorldModel write readiness claim
- 写事实层、benchmark/provider comparison claim
- 改 routing；audit 缺失
