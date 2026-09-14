# LUNA — Realtime OCR Candidate Benchmark v0

## Phase

- **Phase-ModelOCR-006E**

## Scope

Execute **raw-text-only** benchmarks for the **five realtime-track** candidates on the frozen **30-sample** GT (`datasets/ocr_raw_text_benchmark_v0/`). **No** default OCR provider selection, **no** downstream integration, **no** complex-layout branch stacks in this phase.

## Candidates (in scope)

| Key | Description |
|-----|-------------|
| `rapidocr_current` | RapidOCR default (bundled ONNX in `rapidocr-onnxruntime`) |
| `rapidocr_ppocrv4_mobile_onnx` | Explicit PP-OCRv4 mobile det/rec/cls paths (bundled package models) |
| `rapidocr_ppocrv5_mobile_onnx` | PP-OCRv5 mobile ONNX under `models/ocr/rapidocr_ppocrv5_mobile/` (optional until pinned) |
| `easyocr` | EasyOCR multilingual comparison (`pip install easyocr`) |
| `tesseract` | System Tesseract + `pytesseract` classic baseline |

## Out of scope (006E)

- PaddleOCR, macOS Vision, Surya, docTR, PaddleOCR-VL, DeepSeek-OCR / OCR2.

## Tooling

- Runner: `tools/run_realtime_ocr_candidate_benchmark_v0.py`
- Verifier: `tools/verify_realtime_ocr_candidate_benchmark_v0.py`

## Boundaries

Raw text candidates only; governance flags off; trace/replay/whitebox emitted per provider; model asset reports recorded per candidate.
