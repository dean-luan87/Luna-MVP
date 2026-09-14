# LUNA — Realtime OCR Candidate Benchmark Retry After Asset Fix v0

## Phase

- **Phase-ModelOCR-006E** (re-run after **006E-Fix**)

## Output root (authoritative for this closure)

- `logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`

## Run status (all five candidates)

| Provider key | run_status |
|--------------|------------|
| `rapidocr_current` | success |
| `rapidocr_ppocrv4_mobile_onnx` | success |
| `rapidocr_ppocrv5_mobile_onnx` | success |
| `easyocr` | success |
| `tesseract` | success |

## Verifier

- **verdict:** **GO** (`verify_realtime_ocr_candidate_benchmark_v0.py`)  
- **governance:** leakage 0; `default_ocr_provider_set=false`

## Metric highlights (30-sample GT, illustrative)

| Provider | text_exact_match_rate | avg_latency_ms | bbox_iou_avg |
|----------|----------------------|----------------|--------------|
| rapidocr_current | 0.2 | ~117 | ~0.279 |
| rapidocr_ppocrv4_mobile | 0.2 | ~113 | ~0.279 |
| rapidocr_ppocrv5_mobile | 0.2 | ~119 | ~0.117 |
| easyocr | 0.0 | ~693 | ~0.103 |
| tesseract | 0.0 | ~216 | ~0.062 |

**Interpretation:** Horizontal comparison is now **valid**; default provider remains **undecided** — EasyOCR/Tesseract show low exact match on this GT; v5 ONNX changes bbox/duplicate behaviour vs v4 baseline.

## Next step

Eligible to open **provider decision review** only as a **review** — still **no** default OCR until product thresholds are met.
