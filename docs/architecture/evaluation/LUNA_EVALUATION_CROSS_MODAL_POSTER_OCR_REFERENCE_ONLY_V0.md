# Evaluation — CrossModal Poster OCR ReferenceOnly v0

**Phase**：`Phase-CrossModal-Poster-OCR-ReferenceOnly-001`

## 输入根（默认）

| 输入 | 路径 |
|------|------|
| Poster layout governance | `_eval_out/poster_layout_segmentation_governance_smoke_v0/` |
| Poster region OCR plan | `_eval_out/poster_region_ocr_plan_stub_smoke_v0/` |
| Poster visual symbol evidence | `_eval_out/poster_visual_symbol_evidence_stub_smoke_v0/` |
| Metrics collector | `_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0/` |
| Simulation Lab harness | `_eval_out/simulation_lab_minimal_harness_v0/developer_full/` |

## 工具

- Runner：`tools/evaluation/midplatform/run_cross_modal_poster_ocr_reference_only_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_cross_modal_poster_ocr_reference_only_v0.py`

## 运行（人工）

```bash
python3 tools/evaluation/midplatform/run_cross_modal_poster_ocr_reference_only_v0.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_poster_ocr_reference_only_v0 \
  --bootstrap-inputs

python3 tools/evaluation/midplatform/verify_cross_modal_poster_ocr_reference_only_v0.py \
  --reference-only-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_poster_ocr_reference_only_v0
```

`--bootstrap-inputs` 仅在缺少前置 smoke 产物时使用；**不** 运行 OCR。
