# Luna Evaluation — Static Reading Task Scene Context Policy v1

**Phase**：`Static-Reading-Task-Scene-Context-Policy-v1-001`

## Smoke 输出

`_eval_out/static_reading_task_scene_context_policy_v1_smoke_v0/`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_static_reading_task_scene_context_policy_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_policy_v1_smoke_v0 \
  --readable-region-policy-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_guidance_policy_v1_smoke_v0 \
  --information-source-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_information_source_localization_policy_v1_smoke_v0 \
  --assisted-static-reading-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/assisted_static_reading_runtime_dryrun_v1_smoke_v0 \
  --assisted-static-reading-mode-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/assisted_static_reading_mode_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_governance_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-sampling-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --voice-output-plane-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_static_reading_task_scene_context_policy_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_reading_task_scene_context_policy_v1_smoke_v0
```

## GO pack

[LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_STATIC_READING_TASK_SCENE_CONTEXT_POLICY_V1_GO_NO_GO_PACK_V0.md)
