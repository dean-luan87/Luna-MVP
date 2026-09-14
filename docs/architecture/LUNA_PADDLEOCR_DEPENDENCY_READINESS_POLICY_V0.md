# LUNA — PaddleOCR Dependency Readiness Policy v0

## Phase

- **Phase-ModelOCR-004B**

## Required dependency probe

- `paddle`
- `paddleocr`
- `PIL`
- `cv2`
- `numpy`

All probe results must be recorded as `ok|missing`.

## Readiness rules

1. det/rec must be present under pinned paths.
2. cls is optional; when missing, mark optional + not-claimed orientation.
3. `model_files_manifest_v0.json` must exist.
4. if dependency missing OR required weight missing => **fail-closed**.

## Fail-closed behavior

- `provider_available=false`
- `fail_closed=true`
- `raw_text_candidates=[]`
- `readiness_status=not_ready|partial`
- no benchmark, no semantic output, no downstream.

## Fallback invariants

Fallback candidates must stay:
- `rapidocr_onnxruntime_v0`
- `macos_vision_ocr_system_v0`

Removing either is a 004B verifier failure.
