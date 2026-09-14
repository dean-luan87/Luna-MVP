# Evaluation — Luna Basic Functional Loop Stabilization Plan v1

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_luna_basic_functional_loop_stabilization_plan_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/luna_basic_functional_loop_stabilization_plan_v1_smoke_v0 \
  --ocr-mainline-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_governance_closure_v1_smoke_v0 \
  --worldmodel-framework-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/worldmodel_lookup_for_reading_framework_v1_smoke_v0 \
  --software-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_software_mainline_closure_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --vision-capture-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_governance_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --user-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_guidance_recovery_runtime_dryrun_v1_smoke_v0 \
  --voice-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_runtime_dryrun_v1_smoke_v0 \
  --vop-adapter-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_output_plane_adapter_for_guidance_v1_smoke_v0 \
  --hardware-adapter-stub-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_runtime_adapter_implementation_stub_v1_smoke_v0 \
  --realvideo-frame-sample-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0 \
  --regression-route-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0

python3 tools/evaluation/midplatform/verify_luna_basic_functional_loop_stabilization_plan_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/luna_basic_functional_loop_stabilization_plan_v1_smoke_v0
```

## GO/NO-GO Pack

[LUNA_EVALUATION_LUNA_BASIC_FUNCTIONAL_LOOP_STABILIZATION_PLAN_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_LUNA_BASIC_FUNCTIONAL_LOOP_STABILIZATION_PLAN_V1_GO_NO_GO_PACK_V0.md)
