# Luna Evaluation — Voice Output Plane Adapter for Guidance v1

**Phase**：`Voice-Output-Plane-Adapter-for-Guidance-v1-001`

## Smoke 输出

`_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0/`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_voice_output_plane_adapter_for_guidance_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0 \
  --voice-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_runtime_dryrun_v1_smoke_v0 \
  --voice-guidance-template-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_template_v1_smoke_v0 \
  --user-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_guidance_recovery_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_voice_output_plane_adapter_for_guidance_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0
```

## GO pack

[LUNA_EVALUATION_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1_GO_NO_GO_PACK_V0.md)
