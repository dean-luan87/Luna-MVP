# LUNA — MidPlatform OCR Bridge Upstream Input Test Matrix v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002-Fix**

## Scope

只覆盖 Bridge-002 skeleton 的上游离线输入解析与候选产出边界。

## Test matrix（Upstream evidence path）

1) `yolo_ocr_bridge_root`
- 输入可解析：`per_sample_yolo_ocr_bridge_results.json` 可读
- 生成：`midplatform_ocr_evidence_inputs.json` / `scene_delta_control_results.json` / `filter_results.json`
- 生成：`midplatform_text_extraction_candidates.json` / `world_context_evidence_candidates.json` / `ambient_context_candidates.json`
- 生成：`midplatform_ocr_bridge_trace.jsonl` / `midplatform_ocr_bridge_replay.jsonl` / `midplatform_ocr_bridge_whitebox.jsonl`
- 不生成：`semantic_summary`（必须为 null 或不存在）、不生成 `navigation_action`（必须为 null）
- 不触发：无真实世界模型写入、无 runtime / 下游调用

2) `ocr_benchmark_root`
- 输入可解析：`raw_outputs/<provider_id>/ocr_sample_*.json` 可读
- 生成：同上（evidence/delta/filter/candidate/trace 三类产物齐全）
- 不生成：同上（semantic_summary / navigation_action / runtime）

