# Evaluation — Vision Capture Runtime DryRun v1

**Phase**：`Vision-Capture-Runtime-DryRun-v1-001`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_vision_capture_runtime_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_governance_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-sampling-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --user-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_guidance_recovery_policy_v1_smoke_v0 \
  --ocr-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_multiframe_v2_smoke_v0 \
  --multiframe-crop-v2-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/multiframe_crop_execution_dryrun_v2_textdetector_adjusted_smoke_v0 \
  --bbox-adjustment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/bbox_adjustment_proposal_v2_multiframe_smoke_v0 \
  --text-detector-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/text_detector_dryrun_v1_smoke_v0 \
  --crop-quality-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/crop_quality_diagnosis_v2_multiframe_smoke_v0 \
  --evidence-pack-v4-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/evidence_pack_adapter_v4_multiframe_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_vision_capture_runtime_dryrun_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0
```

## GO/NO_GO

[LUNA_EVALUATION_VISION_CAPTURE_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VISION_CAPTURE_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md)
