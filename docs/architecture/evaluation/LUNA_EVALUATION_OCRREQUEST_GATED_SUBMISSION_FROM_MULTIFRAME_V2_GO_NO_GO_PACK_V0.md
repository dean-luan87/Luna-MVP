# OCRRequest Gated Submission from Multiframe v2 GO/NO_GO Pack v0

## GO

- 5 adjusted crop intake；bridge OCR；`direct_provider_bypass=false`
- 每条调用有 `ocrrequest_reference_multiframe_v2_id`
- v1/v2 对比报告生成；不生成 EP / Semantic；blocker 未解除
- `verify_ocrrequest_gated_submission_from_multiframe_v2` = GO

## CONDITIONAL_GO

- v2 仍全 empty，但 `user_guidance_recovery_recommended=true` 且 boundary/trace 完整
- 部分 provider error，但无越界

## NO_GO

- direct bypass / mock text / full-frame OCR / 写事实 / 解除 blocker / 生成 EP 或 Semantic / SV rerun / TTS 或用户引导 runtime action
