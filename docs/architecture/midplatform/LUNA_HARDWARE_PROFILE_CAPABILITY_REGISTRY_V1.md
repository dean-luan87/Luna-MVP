# Luna — Hardware Profile Capability Registry v1

**Phase**：`Hardware-Profile-Capability-Registry-v1-001`  
**性质**：registry schema + minimal unknown profile + adapter placeholder；不探测硬件

## 产出

- `hardware_profile_schema_v1` / `camera_capability_registry_schema_v1`  
- `device_registry_schema_v1` / `sensor_registry_schema_v1`  
- `hardware_capability_status_enum_v1`（available / unknown / unsupported / degraded / stale / runtime_adapter_missing 等）  
- `hardware_minimal_unknown_profile_v1`（`usable_for_runtime_action=false`）  
- `hardware_camera_runtime_adapter_placeholder_v1`（`implementation_available=false`）

**Final**：`READY_FOR_PROFILE_REGISTRY_REVIEW_OR_ADAPTER_IMPLEMENTATION`  
**GuardedTrial**：`guardedtrial_allowed_now=false`（blockers: capability_registry_missing, runtime_adapter_missing）

## 前置

[LUNA_HARDWARE_CAMERA_CONTROL_RUNTIME_DRYRUN_V1.md](./LUNA_HARDWARE_CAMERA_CONTROL_RUNTIME_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/hardware_profile_capability_registry_v1.py`  
- `tools/evaluation/midplatform/run_hardware_profile_capability_registry_v1.py`  
- `tools/evaluation/midplatform/verify_hardware_profile_capability_registry_v1.py`

## 建议下一 phase

- [LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_CONTRACT_V1.md](./LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_CONTRACT_V1.md)（已实现）
