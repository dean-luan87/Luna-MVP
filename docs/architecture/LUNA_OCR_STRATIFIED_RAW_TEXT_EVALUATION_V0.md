# LUNA — OCR Stratified Raw Text Evaluation v0

## Phase

- **Phase-ModelOCR-005A**

## Purpose

- Reuse unified runner and report stratified raw-text metrics.
- No semantic interpretation and no downstream invocation.

## Stratified outputs

- `metrics_by_expected_text_type`
- `metrics_by_difficulty_level`
- `metrics_by_visual_condition`
- `metrics_by_language_type`

## Core metrics

- accuracy: exact/normalized/CER/WER + language-specific accuracy
- bbox: present_rate/iou_avg/precision/recall/f1
- latency: avg/p50/p95/fps
- governance: semantic/nav leakage must remain zero
