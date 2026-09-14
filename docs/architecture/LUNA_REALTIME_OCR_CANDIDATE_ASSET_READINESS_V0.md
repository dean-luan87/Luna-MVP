# LUNA — Realtime OCR Candidate Asset Readiness v0

## Phase

- **Phase-ModelOCR-006E**

## Purpose

Each realtime candidate must emit a **provider asset report** (`provider_asset_reports/*.json`) describing:

- `provider_id`, `model_config_id`, `provider_kind`
- `dependency_ready`
- `model_assets_status`: `pinned_local` | `cache_detected` | `auto_downloaded` | `missing` | `not_required`
- `model_asset_paths` and `model_asset_hashes` (or `hash_unavailable_reason`)
- `reproducibility_risk`
- `requires_network_at_runtime`

## Candidate-specific notes

| Candidate | Typical asset posture |
|-----------|------------------------|
| **rapidocr_current** | ONNX inside `rapidocr-onnxruntime` site-packages — **cache_detected**, reproducibility risk until copied/pinned in-repo |
| **rapidocr_ppocrv4_mobile** | Same bundled v4 ONNX — explicit paths for audit |
| **rapidocr_ppocrv5_mobile** | Expects files per `configs/models/ocr/rapidocr_ppocrv5_mobile_manifest_v0.json` — **missing** until user drops ONNX |
| **easyocr** | Weights may download on first run — **reproducibility_risk**, network may be required once |
| **tesseract** | System binary + `pytesseract` — **not_required** model files; hash N/A |

## Policy

First-run **auto-download** must be **logged**; default OCR must **not** be implied. Pin hashes when moving toward production comparison.
