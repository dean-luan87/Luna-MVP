# LUNA — OCR Offline Source Policy Integration Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-009** — *OCR Offline Source Policy Integration v0*

## GO

All true:

- Policy selector implemented and probed from local adapters (`offline_source_policy_v0.py`).
- Offline benchmark accepts `--source-policy ocr_default_offline_raw_text_source_policy_v0` and disable flags.
- **Normal** evidence run selects **PP-OCRv4 mobile** path; **fallback** run selects **`rapidocr_current`** when v4 is disabled.
- Summary + per-sample outputs include **policy / audit** fields; `governance_leakage=0` in verifier.
- Legacy explicit `--providers` mode **unchanged** when `--source-policy` omitted.
- **No** product runtime default OCR change; **no** YOLO / mid-platform / downstream wiring.

**Verdict:** **GO** (see verifier + benchmark roots in integration doc).

## CONDITIONAL_GO

- Asset `model_config_id` / hashes still partially null in probe-only audit — acceptable; track under reproducibility soft follow-up.

## NO_GO

- Runtime default OCR switched in this phase.
- Default chain falls through to EasyOCR / PaddleOCR / Tesseract / complex providers.
- Explicit provider mode broken.
- Missing audit fields on policy runs.

## Recommended next phase

- **Phase-ModelOCR-010 — OCR Offline Source Policy Regression & Closure v0**

## Example evidence roots

- `logs/ocr_offline_source_policy_009_normal_20260429_124053`
- `logs/ocr_offline_source_policy_009_fallback_20260429_124053`
