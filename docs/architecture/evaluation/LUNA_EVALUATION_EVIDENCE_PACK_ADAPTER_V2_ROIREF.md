# Luna — Evaluation: Evidence Pack Adapter v2 ROIRef

**Phase**：`Phase-Evidence-Pack-Adapter-v2-ROIRef-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_evidence_pack_adapter_v2_roiref.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v2_roiref_smoke_v0 \
  --roi-ocr-gated-submission-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_roi_v1_smoke_v0 \
  --roi-ocrrequest-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_to_ocrrequest_reference_v1_smoke_v0 \
  --roi-crop-rerun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_execution_dryrun_v1_rerun_better_frames_smoke_v0 \
  --better-frame-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/better_frame_selection_runtime_v1_smoke_v0 \
  --roi-retry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_retry_proposal_runtime_v1_smoke_v0 \
  --source-validation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_source_validation_dryrun_v1_smoke_v0 \
  --adapter-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --review-queue-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_review_queue_runtime_dryrun_v1_smoke_v0 \
  --review-policy-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_review_policy_v1_smoke_v0 \
  --semantic-v1-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_semantic_candidate_generator_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_evidence_pack_adapter_v2_roiref.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v2_roiref_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V2_ROIREF_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_EVIDENCE_PACK_ADAPTER_V2_ROIREF_GO_NO_GO_PACK_V0.md)
