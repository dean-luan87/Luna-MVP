# Luna — Hardware Camera Runtime Adapter Contract v1

**Phase**：`Hardware-Camera-Runtime-Adapter-Contract-v1-001`  
**性质**：adapter interface + 9 method schemas + error taxonomy；非 implementation

## 9 Required Methods

open_camera · close_camera · capture_frame · request_zoom · request_autofocus · request_exposure_adjustment · request_stabilization · get_capability_report · get_health_status

## 决策

**Final**：`READY_FOR_ADAPTER_IMPLEMENTATION_OR_GUARDEDTRIAL_PRECHECK`  
**GuardedTrial**：`guardedtrial_allowed_now=false`（blockers: adapter_implementation_missing, real_permission_state_unknown）

## 前置

[LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md](./LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md)

## 实现

- `capabilities/midplatform/hardware_camera_runtime_adapter_contract_v1.py`  
- `tools/evaluation/midplatform/run_hardware_camera_runtime_adapter_contract_v1.py`  
- `tools/evaluation/midplatform/verify_hardware_camera_runtime_adapter_contract_v1.py`

## Stub 已实现

[LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_IMPLEMENTATION_STUB_V1.md](./LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_IMPLEMENTATION_STUB_V1.md) — `STUB_READY_SOFTWARE_BOUNDARY_CLOSED`；硬件链可冻结。

## 建议下一 phase

- **Return-To-Software-Mainline**（推荐）  
- `Hardware-Camera-Control-GuardedTrial-Precheck-v1`  
- `Hardware-Camera-Runtime-Adapter-RealImplementation-v1`
