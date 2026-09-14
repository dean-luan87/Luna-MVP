# Luna — Evaluation ROI Crop Diversity Check v1

**Phase**：`Phase-ROI-Crop-Diversity-Check-v1-001`

## Smoke 命令

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_roi_crop_diversity_check_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_diversity_check_v1_smoke_v0 \
  --roi-ocr-quality-diagnosis-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_ocr_quality_diagnosis_v1_smoke_v0 \
  --semantic-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/semantic_candidate_v2_roiaware_smoke_v0 \
  --evidence-pack-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v2_roiref_smoke_v0 \
  --roi-ocr-gated-submission-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_roi_v1_smoke_v0 \
  --roi-ocrrequest-reference-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_to_ocrrequest_reference_v1_smoke_v0 \
  --roi-crop-rerun-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_execution_dryrun_v1_rerun_better_frames_smoke_v0 \
  --better-frame-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/better_frame_selection_runtime_v1_smoke_v0 \
  --roi-retry-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_retry_proposal_runtime_v1_smoke_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_roi_crop_diversity_check_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_diversity_check_v1_smoke_v0
```

## 产物

输出目录 `_eval_out/roi_crop_diversity_check_v1_smoke_v0/`：summary、intake matrix、rule matrix、bbox/frame/linebox/dimension/proposal 报告、diversity score、duplicate groups、risk decision、future fix、boundary、source chain、metrics、benchmark/health link、no-write、simulation、non-claims、followups、audit、verifier report。

## GO / NO_GO

见 [LUNA_EVALUATION_ROI_CROP_DIVERSITY_CHECK_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_ROI_CROP_DIVERSITY_CHECK_V1_GO_NO_GO_PACK_V0.md)
