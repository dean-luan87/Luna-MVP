# LUNA — Realtime Provider Recommendation Matrix v0

## Phase

- **Phase-ModelOCR-007**

## Recommendation levels (taxonomy)

| Level ID | Meaning |
|----------|---------|
| `RECOMMENDED_REALTIME_PRIMARY_CANDIDATE` | First choice for future realtime OCR **policy** (not code default yet) |
| `RECOMMENDED_REALTIME_SECONDARY_CANDIDATE` | Equivalent/alternate primary; choose one in policy |
| `FALLBACK_OR_COMPARISON_ONLY` | System or baseline; not primary realtime OCR |
| `NOT_RECOMMENDED_FOR_REALTIME_DEFAULT` | Explicitly exclude from default realtime selection |
| `COMPLEX_BRANCH_ONLY` | Layout / document / long-text / OCR-VL track |
| `FUTURE_REVIEW_REQUIRED` | Needs new evidence before promotion |

## Matrix (initial fill — Phase-007)

| provider_id / line | Recommendation level | Notes |
|--------------------|------------------------|--------|
| `rapidocr_ppocrv4_mobile_onnx_v0` | **RECOMMENDED_REALTIME_PRIMARY_CANDIDATE** | Explicit ONNX paths; ~113 ms/frame; bbox_iou ~0.279; same accuracy as current |
| `rapidocr_onnxruntime_v0` (`rapidocr_current`) | **RECOMMENDED_REALTIME_SECONDARY_CANDIDATE** | ~117 ms/frame; equivalent to v4 mobile in practice |
| `rapidocr_ppocrv5_mobile_onnx_v0` | **FUTURE_REVIEW_REQUIRED** | No accuracy gain; bbox_iou ~0.117; **community ONNX** — not official audit chain |
| `easyocr_multilingual_v0` | **NOT_RECOMMENDED_FOR_REALTIME_DEFAULT** | exact 0.0; ~693 ms/frame on 30-sample GT |
| `tesseract_cli_baseline_v0` | **FALLBACK_OR_COMPARISON_ONLY** / **NOT_RECOMMENDED_FOR_REALTIME_DEFAULT** | Classic baseline; zh/natural scene weak on GT |
| `macos_vision_ocr_system_v0` | **FALLBACK_OR_COMPARISON_ONLY** | System comparator; not realtime primary |
| `paddleocr_ppocrv5_lightweight_v0` (current config) | **COMPLEX_BRANCH_ONLY** / **NOT_RECOMMENDED_FOR_REALTIME_DEFAULT** | Offline/complex; latency & audit block realtime default |

## Complex branch (not in realtime default matrix)

| Stack | Level |
|-------|--------|
| Surya OCR | `COMPLEX_BRANCH_ONLY` |
| docTR | `COMPLEX_BRANCH_ONLY` |
| PaddleOCR-VL / DeepSeek-OCR | `COMPLEX_BRANCH_ONLY` / future |

## Benchmark reference

- `logs/realtime_ocr_candidate_benchmark_006e_fix_20260429_120908`
