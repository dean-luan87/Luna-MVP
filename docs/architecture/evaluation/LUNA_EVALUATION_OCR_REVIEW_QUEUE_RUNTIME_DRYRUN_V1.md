# Luna — Evaluation: OCR Review Queue Runtime DryRun v1

**Phase**：`Phase-OCR-Review-Queue-Runtime-DryRun-v1-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_ocr_review_queue_runtime_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_review_queue_runtime_dryrun_v1_smoke_v0 \
  --review-policy-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_review_policy_v1_smoke_v0 \
  --semantic-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_generator_v1_smoke_v0 \
  --adapter-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --worldmodel-unresolved-slot-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_ocr_review_queue_runtime_dryrun_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_review_queue_runtime_dryrun_v1_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCR_REVIEW_QUEUE_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md)
