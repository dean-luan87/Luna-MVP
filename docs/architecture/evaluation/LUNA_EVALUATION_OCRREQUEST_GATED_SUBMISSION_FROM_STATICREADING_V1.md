# Evaluation — OCRRequest Gated Submission from StaticReading v1

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/ocr/run_ocrrequest_gated_submission_from_staticreading_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_staticreading_v1_smoke_v0 \
  --memory-handoff-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/confirmed_text_evidence_memory_handoff_dryrun_v1_smoke_v0 \
  --memory-governance-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/confirmed_text_evidence_memory_governance_contract_v1_smoke_v0 \
  --hardware-adapter-stub-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_runtime_adapter_implementation_stub_v1_smoke_v0 \
  --hardware-adapter-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_runtime_adapter_contract_v1_smoke_v0 \
  --hardware-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_control_runtime_dryrun_v1_smoke_v0 \
  --rrd-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_runtime_dryrun_v1_smoke_v0 \
  --isrc-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_runtime_dryrun_v1_smoke_v0 \
  --tsc-reevaluation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_reevaluation_dryrun_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-sampling-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/ocr/verify_ocrrequest_gated_submission_from_staticreading_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocrrequest_gated_submission_from_staticreading_v1_smoke_v0
```

## GO/NO-GO Pack

[LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_STATICREADING_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_OCRREQUEST_GATED_SUBMISSION_FROM_STATICREADING_V1_GO_NO_GO_PACK_V0.md)
