# LUNA — OCR Offline Source Policy Integration Test Matrix v0

## Phase

- **Phase-ModelOCR-009** — verified by `tools/verify_ocr_offline_source_policy_v0.py`

## Selector tests (synthetic registry)

| ID | Case | Expect |
|----|------|--------|
| A | Normal | `provider_selected=rapidocr_ppocrv4_mobile_onnx`, `fallback_used=false` |
| B | `--disable-rapidocr-ppocrv4` | `provider_selected=rapidocr_current`, `fallback_used=true`, reason contains `disabled` |
| C | v4 registry unhealthy | `rapidocr_current`, `fallback_used=true`, `rapidocr_ppocrv4_unavailable` |
| D | v4 + current unhealthy | `macos_vision_ocr_system_v0` |
| E | All Rapid + Vision unhealthy | `not_available` |
| F | `disable_ocr_policy` | `policy_applied=false`, `not_available` |
| G | `controlled_live_stream=true` | Policy not applied / blocked |
| H | `semantic_interpretation_enabled=true` | Blocked / `not_available` |
| I | Forbidden providers | EasyOCR / Tesseract / etc. **never** returned as selected for synthetic happy path |
| J | Audit keys | `selection_audit` contains required governance + schema fields |

## Benchmark artifact tests (optional flags)

| ID | Input | Expect in `ocr_benchmark_summary.json` |
|----|-------|----------------------------------------|
| N | `--normal-root` | `provider_selected=rapidocr_ppocrv4_mobile_onnx`, `fallback_used=false` |
| Fb | `--fallback-root` (with `--disable-rapidocr-ppocrv4` run) | `provider_selected=rapidocr_current`, `fallback_used=true`, `fallback_reason` contains `rapidocr_ppocrv4_disabled` |

## Explicit provider mode regression

| ID | Command pattern | Expect |
|----|-----------------|--------|
| L | No `--source-policy`, default `--providers` | Three-way benchmark as before 009; no `source_policy_id` in summary |
