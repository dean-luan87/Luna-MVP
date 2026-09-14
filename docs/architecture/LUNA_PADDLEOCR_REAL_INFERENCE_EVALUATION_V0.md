# LUNA — PaddleOCR Real Inference Evaluation v0

## Phase

- **Phase-ModelOCR-006A**

## Scope

- PaddleOCR real raw-text inference on the same 30-sample GT dataset.
- Raw text only; no semantic interpretation; no downstream invocation.

## Inputs

- dataset manifest: `datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json`
- same image/frame inputs as 005B baseline.

## Outputs

- `paddleocr_real_inference_summary.json`
- `per_sample_paddleocr_results.json`
- trace/replay/whitebox artifacts
