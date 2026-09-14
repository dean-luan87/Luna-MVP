# LUNA — OCR Provider Comparison Matrix v0

## Phase

- **Phase-ModelOCR-005**

## Providers in scope

- `rapidocr_onnxruntime_v0`
- `macos_vision_ocr_system_v0`
- `paddleocr_ppocrv5_lightweight_v0`

## Comparison dimensions

- Raw text accuracy (exact/normalized/CER/WER)
- BBox/Confidence availability and quality
- Latency/throughput
- Governance leakage = 0 requirement
- Observability completeness

## PaddleOCR boundary note

Current Paddle state:
- `det=present`
- `rec=present`
- `cls=missing_optional`
- `orientation_support=false`
- `rotated_text_handling=not_claimed`

Benchmark must record:
- `rotated_text_samples_not_claimed=true`
- `orientation_sensitive_cases=excluded_or_marked_not_claimed`
