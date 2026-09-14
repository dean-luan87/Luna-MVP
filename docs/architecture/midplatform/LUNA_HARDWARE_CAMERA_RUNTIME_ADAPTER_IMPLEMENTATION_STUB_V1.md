# Luna — Hardware Camera Runtime Adapter Implementation Stub v1

**Phase**：`Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001`  
**性质**：contract 对齐的 9-method stub；非 real adapter、非 camera 调用

## 一句话

补齐 Adapter Contract 的接口壳子，默认返回 `blocked_stub_only` / `not_captured` / `unknown` / `stub_only`；验证中台边界与 no-write；**硬件链路可冻结**。

## 9 Stub Methods

`open_camera` · `close_camera` · `capture_frame` · `request_zoom` · `request_autofocus` · `request_exposure_adjustment` · `request_stabilization` · `get_capability_report` · `get_health_status`

## 决策

**Final**：`STUB_READY_SOFTWARE_BOUNDARY_CLOSED`  
**GuardedTrial**：`guardedtrial_allowed_now=false`（blockers: real_adapter_missing, real_camera_disabled, permission_state_unknown, hardware_profile_not_verified）  
**OCRRequest**：`ocrrequest_eligible_now=false`

## 前置

[LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_CONTRACT_V1.md](./LUNA_HARDWARE_CAMERA_RUNTIME_ADAPTER_CONTRACT_V1.md)

## 实现

- `capabilities/midplatform/hardware_camera_runtime_adapter_stub_v1.py`（9 methods）  
- `capabilities/midplatform/hardware_camera_runtime_adapter_implementation_stub_v1.py`（smoke 产物生成）  
- `tools/evaluation/midplatform/run_hardware_camera_runtime_adapter_implementation_stub_v1.py`  
- `tools/evaluation/midplatform/verify_hardware_camera_runtime_adapter_implementation_stub_v1.py`

## 建议下一 phase

- **Return-To-Software-Mainline**（推荐，冻结硬件链）  
- `Hardware-Camera-Control-GuardedTrial-Precheck-v1`  
- `Hardware-Camera-Runtime-Adapter-RealImplementation-v1`（外部硬件人员）

## 软件主线接续

硬件链已冻结。下一软件治理契约：[LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md](./LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md)
