# LUNA — OCR Raw Text Benchmark Runner v0

## Phase

- **Phase-ModelOCR-005**

## Tool

- `tools/run_ocr_raw_text_benchmark_v0.py`

## Inputs

- `--providers rapidocr,macos_vision,paddleocr`
- `--dataset-manifest datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json`
- `--output-root logs/ocr_raw_text_benchmark_005_<timestamp>`

## Behavior

- Runs each provider independently.
- Provider failure is recorded as not_available; no fake success.
- No semantic interpretation.
- No downstream invocation.

## Output structure

- `ocr_benchmark_summary.json`
- `provider_summaries/*.json`
- `per_sample_comparison.json`
- `raw_outputs/<provider>/*.json`
- `metric_tables/accuracy_metrics.json`
- `metric_tables/latency_metrics.json`
- `metric_tables/bbox_metrics.json`
- `trace/*.jsonl`
- `replay/*.jsonl`
- `whitebox/*.jsonl`
- `benchmark_notes.md`

## Reuse

- RapidOCR: `rapidocr_adapter_v0.py`
- macOS Vision: `macos_vision_ocr_adapter_v0.py`
- PaddleOCR: `paddleocr_adapter_v0.py` (004B skeleton contract)
