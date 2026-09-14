# Luna — Evaluation: Source Validation v2 after EP v3

**Phase**：`Phase-Source-Validation-v2-after-EP-v3-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_source_validation_v2_after_ep_v3.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/source_validation_v2_after_ep_v3_smoke_v0 \
  --semantic-v3-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/semantic_candidate_v3_bbox_expansion_aware_smoke_v0 \
  --evidence-pack-v3-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v3_bbox_expansion_smoke_v0 \
  --ocrrequest-gated-submission-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_roi_v2_bbox_expansion_smoke_v0 \
  --roi-ocrrequest-reference-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_to_ocrrequest_reference_v2_bbox_expansion_smoke_v0 \
  --roi-crop-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_execution_dryrun_v2_bbox_expansion_smoke_v0 \
  --roi-bbox-expansion-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_bbox_expansion_proposal_v1_smoke_v0 \
  --roi-crop-diversity-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_crop_diversity_check_v1_smoke_v0 \
  --roi-ocr-quality-diagnosis-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/roi_ocr_quality_diagnosis_v1_smoke_v0 \
  --semantic-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/semantic_candidate_v2_roiaware_smoke_v0 \
  --evidence-pack-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v2_roiref_smoke_v0 \
  --linebox-sq-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 \
  --mixed-batch-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/mixed_video_poster_batch_smoke_v2_gated_path_only_v0 \
  --worldmodel-unresolved-slot-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_unresolved_observation_slot_contract_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_source_validation_v2_after_ep_v3.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/source_validation_v2_after_ep_v3_smoke_v0
```

## GO / NO_GO

见 [LUNA_EVALUATION_SOURCE_VALIDATION_V2_AFTER_EP_V3_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_SOURCE_VALIDATION_V2_AFTER_EP_V3_GO_NO_GO_PACK_V0.md)
