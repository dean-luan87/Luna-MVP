# LUNA Evaluation Tools — OCR Provider Benchmark Registry v0 (Phase-EvaluationTools-Foundation-001)

## Purpose

为后续 RapidOCR / PaddleOCR / CnOCR 横向对照预留统一登记（evaluation-only）：

- provider_id / family
- 允许的 eval modes（single/batch/stress）
- 支持的 metrics（cer/recall/garbled/latency…）

## Important boundary

该 registry **只用于 evaluation**：

- 不得修改 runtime provider registry
- 不得自动影响主线 provider 选择

## Schema (entry)

参见 `capabilities/evaluation/ocr/ocr_provider_benchmark_registry_v0.py`。

