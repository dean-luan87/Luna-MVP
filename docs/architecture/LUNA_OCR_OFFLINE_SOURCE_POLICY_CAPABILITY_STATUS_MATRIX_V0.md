# LUNA — OCR Offline Source Policy Capability Status Matrix v0

## Phase

- **Phase-ModelOCR-010** — snapshot after **008 / 009 / 010** closure.

| Capability | Status | Notes |
|------------|--------|--------|
| Policy defined (008) | **done** | `LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md` |
| Selector implemented | **done** | `offline_source_policy_v0.py` |
| Offline benchmark integrated | **done** | `--source-policy` on `run_ocr_raw_text_benchmark_v0.py` |
| Normal path evidenced | **done** | 009 normal root |
| Fallback path evidenced | **done** | 009 fallback root |
| Regression tooling | **done** | `run_ocr_offline_source_policy_regression_v0.py` |
| Regression verified | **done** | `verify_ocr_offline_source_policy_regression_v0.py` |
| **Product runtime default OCR** | **not_allowed** | Explicitly out of 008–010 scope |
| YOLO integration | **not_done** | Future optional phase |
| Mid-platform integration | **not_done** | Future optional phase |
| Complex layout OCR branch | **not_done** | Separate charter |
| GT expansion | **ongoing** | Soft follow-up from earlier phases |
| Asset pinning hardening | **ongoing** | Soft follow-up |
| Provider health monitoring | **not_done** | Align with MidPlatform-Monitoring-001 later |
