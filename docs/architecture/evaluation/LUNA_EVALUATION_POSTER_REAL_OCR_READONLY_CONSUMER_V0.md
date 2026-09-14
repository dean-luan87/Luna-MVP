# Luna — Evaluation: Poster Real OCR ReadOnly Consumer v0

**Phase**：`Phase-Poster-Real-OCR-ReadOnly-Consumer-001`

## 运行

```bash
python3 tools/evaluation/ocr/run_poster_real_ocr_readonly_consumer_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_readonly_consumer_smoke_v0 \
  --poster-real-ocr-gated-execution-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_gated_execution_smoke_v0 \
  --poster-reference-only-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_poster_ocr_reference_only_v0 \
  --poster-track-b-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_testboard_track_b_closure_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/ocr/verify_poster_real_ocr_readonly_consumer_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_readonly_consumer_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_POSTER_REAL_OCR_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_POSTER_REAL_OCR_READONLY_CONSUMER_GO_NO_GO_PACK_V0.md)
