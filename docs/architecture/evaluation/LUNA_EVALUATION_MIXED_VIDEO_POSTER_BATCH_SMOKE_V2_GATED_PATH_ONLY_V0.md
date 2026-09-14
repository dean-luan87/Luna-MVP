# Luna — Evaluation: Mixed Video Poster Batch Smoke v2 Gated Path Only

**Phase**：`Phase-Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_mixed_video_poster_batch_smoke_v2_gated_path_only_v0.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --fixtures-root /Users/luanlei/Desktop/Luna-Workspace-Min/fixtures \
  --mixed-batch-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --readability-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/realvideo_ocr_readability_governance_smoke_v0 \
  --evidence-pack-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_spatiotemporal_semantic_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_mixed_video_poster_batch_smoke_v2_gated_path_only_v0.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_MIXED_VIDEO_POSTER_BATCH_SMOKE_V2_GATED_PATH_ONLY_GO_NO_GO_PACK_V0.md)
