# LUNA — PaddleOCR Adapter Skeleton v0

## Phase

- **Phase-ModelOCR-004B**
- Scope: adapter skeleton + dependency readiness + fail-closed; **no benchmark**.

## Goal

Build a PaddleOCR raw-text adapter entry that:
- reads manifest + pinned weights status,
- checks dependency readiness,
- fails closed when not ready,
- preserves fallback candidates.

## Components

- `capabilities/model_ocr/paddleocr_adapter_v0.py`
- `tools/check_paddleocr_dependency_readiness_v0.py`
- `tools/smoke_paddleocr_adapter_skeleton_v0.py`
- `tools/verify_paddleocr_adapter_skeleton_v0.py`

## Hard boundaries

- raw text only; no semantic interpretation.
- no downstream invocation.
- no execute/TTS (`allows_execute_now=false`, `real_tts_invoked=false`).
- cls missing => `orientation_support=false`, `rotated_text_handling=not_claimed`.
- dependency missing => `fail_closed=true`, no OCR inference.

## Adapter contract (skeleton)

- `provider_id`: `paddleocr_ppocrv5_lightweight_v0`
- `model_config_id`: `paddleocr_ppocrv5_lightweight_zh_en_v0`
- `ocr_runtime_mode`: `local_paddleocr_pinned_partial`
- `fallback_candidates`: `rapidocr_onnxruntime_v0`, `macos_vision_ocr_system_v0`

## CLI

```bash
python3 tools/smoke_paddleocr_adapter_skeleton_v0.py \
  --manifest configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json \
  --output-root logs/paddleocr_adapter_skeleton_004b_<timestamp> \
  --check-only
```

Optional init-only (never benchmark):

```bash
python3 tools/smoke_paddleocr_adapter_skeleton_v0.py \
  --manifest configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json \
  --output-root logs/paddleocr_adapter_skeleton_004b_<timestamp> \
  --init-only
```
