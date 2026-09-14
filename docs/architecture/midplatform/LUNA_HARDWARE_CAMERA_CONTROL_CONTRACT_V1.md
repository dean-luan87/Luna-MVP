# Luna — Hardware Camera Control Contract v1

**Phase**：`Hardware-Camera-Control-Contract-v1-001`  
**性质**：contract-only；定义 camera control request / capability report / fallback，不调用硬件

## 契约范围

| 能力 | 表达 |
|------|------|
| static capture | `STATIC_CAPTURE_REQUEST` |
| zoom / autofocus / exposure / stabilization | future capability request |
| hardware unknown | `capability_unknown_allowed=true` |
| 失败回退 | user guidance / external assistance / System Health |

## 对接

- **输入**：RRD 26 条 static capture handoff → 26 条 `scr_*` request candidates  
- **输出决策**：`READY_FOR_HARDWARE_CAMERA_RUNTIME_DRYRUN_LATER`  
- **后续**：Hardware-Camera-Control-Runtime-DryRun-v1 或 Assisted-Static-Reading-GuardedTrial-v1

## 前置

[LUNA_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/hardware_camera_control_contract_v1.py`  
- `tools/evaluation/midplatform/run_hardware_camera_control_contract_v1.py`  
- `tools/evaluation/midplatform/verify_hardware_camera_control_contract_v1.py`

## 评测

[LUNA_EVALUATION_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md](../evaluation/LUNA_EVALUATION_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md)
