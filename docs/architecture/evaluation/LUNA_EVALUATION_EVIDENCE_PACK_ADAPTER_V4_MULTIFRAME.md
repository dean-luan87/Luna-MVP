# Luna — Evaluation: Evidence Pack Adapter v4 Multiframe

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_evidence_pack_adapter_v4_multiframe.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v4_multiframe_smoke_v0 \
  --multiframe-ocr-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_multiframe_v1_smoke_v0 \
  --multiframe-crop-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/multiframe_crop_execution_dryrun_v1_smoke_v0 \
  --text-region-tracklet-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/text_region_tracklet_dryrun_v1_smoke_v0 \
  --better-frame-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/better_frame_extraction_dryrun_v1_smoke_v0 \
  --multiframe-merge-proposal-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/multiframe_merge_proposal_v1_smoke_v0 \
  --source-validation-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/source_validation_v2_after_ep_v3_smoke_v0 \
  --semantic-v3-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/semantic_candidate_v3_bbox_expansion_aware_smoke_v0 \
  --evidence-pack-v3-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v3_bbox_expansion_smoke_v0 \
  --ocrrequest-gated-submission-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_roi_v2_bbox_expansion_smoke_v0 \
  --roi-ocrrequest-reference-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_to_ocrrequest_reference_v2_bbox_expansion_smoke_v0 \
  --roi-crop-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_execution_dryrun_v2_bbox_expansion_smoke_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --worldmodel-unresolved-slot-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_evidence_pack_adapter_v4_multiframe.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v4_multiframe_smoke_v0
```
