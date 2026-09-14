# Luna — Evaluation: STC Sampling Guidance Policy v1

见 [LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md](../midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md)。

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_stc_sampling_guidance_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
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
```

## 验证

```bash
python3 tools/evaluation/midplatform/verify_stc_sampling_guidance_policy_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0
```
