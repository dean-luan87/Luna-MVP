# Evaluation — Poster TestBoard Track B Closure v0

**Phase**：`Phase-Poster-TestBoard-Closure-001`

## 输入根（默认）

| 输入 | 路径 |
|------|------|
| Poster layout governance | `_eval_out/poster_layout_segmentation_governance_smoke_v0/` |
| Poster region OCR plan | `_eval_out/poster_region_ocr_plan_stub_smoke_v0/` |
| Poster visual symbol evidence | `_eval_out/poster_visual_symbol_evidence_stub_smoke_v0/` |
| Poster reference-only | `_eval_out/cross_modal_poster_ocr_reference_only_v0/` |
| Metrics collector | `_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0/` |
| Simulation Lab harness | `_eval_out/simulation_lab_minimal_harness_v0/developer_full/` |

## 输出根

`_eval_out/poster_testboard_track_b_closure_v0/`

## 运行（人工）

```bash
python3 tools/evaluation/midplatform/run_poster_testboard_track_b_closure_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --poster-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_layout_segmentation_governance_smoke_v0 \
  --poster-region-ocr-plan-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_region_ocr_plan_stub_smoke_v0 \
  --poster-visual-symbol-evidence-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_visual_symbol_evidence_stub_smoke_v0 \
  --poster-reference-only-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_poster_ocr_reference_only_v0 \
  --metrics-collector-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_poster_testboard_track_b_closure_v0.py \
  --closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0
```

**不** 运行 OCR、QR、品牌、视觉符号库、fusion 或写事实层。
