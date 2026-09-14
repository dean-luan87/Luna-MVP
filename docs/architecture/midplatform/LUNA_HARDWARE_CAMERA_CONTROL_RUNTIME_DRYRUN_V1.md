# Luna — Hardware Camera Control Runtime DryRun v1

**Phase**：`Hardware-Camera-Control-Runtime-DryRun-v1-001`  
**性质**：hardware unknown 下消费 contract；阻断 runtime camera/OCR；生成 fallback + GuardedTrial readiness

## 决策

**Final**：`BLOCK_RUNTIME_CAMERA_ACTION_PREPARE_GUARDEDTRIAL_OR_FALLBACK`

- 26 static capture request candidates **保留**
- 8 类 hardware action **allowed_now=false**
- OCRRequest future gate **仍阻断**

## 前置

[LUNA_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md](./LUNA_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md)

## 实现

- `capabilities/midplatform/hardware_camera_control_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/run_hardware_camera_control_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/verify_hardware_camera_control_runtime_dryrun_v1.py`

## 建议下一 phase

- `Hardware-Camera-Control-GuardedTrial-v1`
- [LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md](./LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md)（已实现）
