# LUNA — OCR Offline Source Policy Regression Baseline v0

## Phase

- **Phase-ModelOCR-010** — frozen **closed_v0** regression baseline for OCR offline source policy.

## Evidence roots (009)

| Role | Path |
|------|------|
| Normal | `logs/ocr_offline_source_policy_009_normal_20260429_124053` |
| Fallback | `logs/ocr_offline_source_policy_009_fallback_20260429_124053` |

## Expected selection outcomes

| Run | `provider_selected` | `fallback_used` | `fallback_reason` |
|-----|---------------------|-----------------|-------------------|
| Normal | `rapidocr_ppocrv4_mobile_onnx` | `false` | `null` |
| Fallback (`--disable-rapidocr-ppocrv4`) | `rapidocr_current` | `true` | `rapidocr_ppocrv4_disabled` |

## Policy identity (must match)

- `source_policy_id` = `ocr_default_offline_raw_text_source_policy_v0`
- `policy_applied` = `true` on successful policy-mode runs

## Hard gates (no drift)

- Selected providers and `fallback_reason` as above.
- `governance_leakage` = `0`.
- Forbidden providers not selected (EasyOCR, PaddleOCR current, PP-OCRv5 mobile ONNX, Tesseract in default chain).
- Required audit fields present; trace/replay/whitebox present.

## Allowed drift

- Text accuracy, CER/WER, latency, exact match rate, bbox IoU — **not** regression gates for 010.

## Regression output baseline (010)

- Example: `logs/ocr_offline_source_policy_regression_010_20260429_124628`  
- Contains `ocr_offline_source_policy_regression_summary.json` with embedded hard-gate results.
