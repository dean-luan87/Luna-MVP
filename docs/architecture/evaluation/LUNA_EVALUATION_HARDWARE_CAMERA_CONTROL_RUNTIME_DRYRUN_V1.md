# Evaluation — Hardware Camera Control Runtime DryRun v1

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_hardware_camera_control_runtime_dryrun_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_control_runtime_dryrun_v1_smoke_v0 \
  --hardware-contract-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_control_contract_v1_smoke_v0 \
  --rrd-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/static_readable_region_discovery_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-governance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_governance_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --assisted-static-reading-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/assisted_static_reading_runtime_dryrun_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_hardware_camera_control_runtime_dryrun_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/hardware_camera_control_runtime_dryrun_v1_smoke_v0
```

## GO/NO-GO Pack

[LUNA_EVALUATION_HARDWARE_CAMERA_CONTROL_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_HARDWARE_CAMERA_CONTROL_RUNTIME_DRYRUN_V1_GO_NO_GO_PACK_V0.md)
