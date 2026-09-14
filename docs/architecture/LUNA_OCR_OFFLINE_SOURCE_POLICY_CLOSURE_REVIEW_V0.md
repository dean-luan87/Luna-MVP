# LUNA — OCR Offline Source Policy Closure Review v0

## Phase

- **Phase-ModelOCR-010** — closes the **008 → 009 → 010** line for **offline** OCR default source policy.

## Frozen policy identity

- **source_policy_id:** `ocr_default_offline_raw_text_source_policy_v0`

## Frozen default offline source chain (policy v0)

1. `rapidocr_ppocrv4_mobile_onnx`
2. `rapidocr_current`
3. `macos_vision_ocr_system_v0`
4. `not_available`

**Excluded from default chain:** EasyOCR, PaddleOCR (current config), PP-OCRv5 mobile ONNX, Tesseract default chain, complex-layout / OCR-VL stacks (per **008**).

## What 008 delivered

- Written policy, selection/fallback rules, audit requirements, disable/rollback — **no code default**.

## What 009 delivered

- `capabilities/model_ocr/offline_source_policy_v0.py` — selector + probe.
- `tools/run_ocr_raw_text_benchmark_v0.py` — `--source-policy` integration; per-sample + summary audit fields.
- **Evidence:** normal selects PP-OCRv4 mobile path; fallback selects `rapidocr_current` when v4 disabled.

## What 010 delivers

- **Regression** over 009 roots; **closure** documents; **capability matrix**; **boundary register**; **baseline** record; **future branches** list.
- **Still no** product runtime default OCR change.

## Status label

- **OCR offline source policy — `closed_v0` (documentation + offline tooling)** as of Phase-010 acceptance.
