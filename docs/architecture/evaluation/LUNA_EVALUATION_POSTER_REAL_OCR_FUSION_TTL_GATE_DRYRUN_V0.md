# Luna — Evaluation: Poster Real OCR Fusion TTL Gate DryRun v0

**Phase**：`Phase-Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001`

## 运行

```bash
python3 tools/evaluation/midplatform/run_poster_real_ocr_fusion_ttl_gate_dryrun_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_ttl_gate_dryrun_smoke_v0 \
  --poster-fusion-review-queue-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_review_queue_smoke_v0 \
  --poster-fusion-candidate-dryrun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_candidate_dryrun_smoke_v0 \
  --poster-reference-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_reference_closure_smoke_v0 \
  --poster-readonly-consumer-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_readonly_consumer_smoke_v0 \
  --benchmark-real-values-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-lab-harness-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_poster_real_ocr_fusion_ttl_gate_dryrun_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_real_ocr_fusion_ttl_gate_dryrun_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_POSTER_REAL_OCR_FUSION_TTL_GATE_DRYRUN_GO_NO_GO_PACK_V0.md)
